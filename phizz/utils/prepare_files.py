"""Functions to prepare infiles from different sources to phizz format"""
import os
import sys
import logging
import gzip
import logging
from codecs import open

import click

from phizz.log import configure_stream

from phizz.utils import parse_genes

configure_stream('INFO')

logger = logging.getLogger(__name__)

def uniqify_phenotypes(lines):
    """Produce a new resource with phenotypes and descriptions
    
        Args:
            lines (Iterator): The lines of the file
        
        Returns:
            hpo_terms(generator(dict)): The hpoterms
    """
    hpo_terms = {}
    for line in lines:
        if not line.startswith('#'):
            line = line.rstrip().split('\t')
            hpo_id = line[0]
            description = line[1]
            hpo_terms[hpo_id] = description
    return hpo_terms

def get_hi_scores(lines):
    """Return a generator with hi scores
    
        Args:
            lines (Iterator): The lines of the file
        
        Yields:
            hi_scores(tuple(hgnc_id, hi_score))
    
    """
    for i, line in enumerate(lines):
        #First line is the header
        if i > 0:
            line = line.rstrip().split('\t')
            info = line[3].split('|')
            hgnc_id = info[0]
            hi_score = info[1]
            result = {hgnc_id: hi_score}
            yield (hgnc_id, hi_score)

def get_constraint_scores(lines):
    """Return a generator with exac constraint scores
    
        Args:
            lines (Iterator): The lines of the file
        
        Yields:
            constraint_scores(tuple(hgnc_id, constraint_scores))
    
    """
    for i, line in enumerate(lines):
        #First line is the header
        if i > 0:
            line = line.rstrip().split('\t')
            info = line[3].split('|')
            hgnc_id = line[1]
            constraint_score = line[-1]
            
            yield (hgnc_id, constraint_score)

def parse_ensembl_header(line):
    """Parse an ensembl header line
    
        Args:
            line(str): A line with header info
        
        Returns:
            position_info(dict): A dictionary that tells what position
                                 the different columns have
    """
    position_info = {}
    line = line.lstrip('#').rstrip().split('\t')
    for i,info in enumerate(line):
        if 'hromosome' in info:
            position_info['chrom'] = i
        elif 'Start' in info:
            position_info['start'] = i
        elif 'End' in info:
            position_info['stop'] = i
        elif 'Ensembl Gene ID' in info:
            position_info['geneid'] = i
        elif 'Description' in info:
            position_info['description'] = i
        elif 'HGNC symbol' in info:
            position_info['hgnc_symbol'] = i
        elif 'HGNC ID' in info:
            position_info['hgnc_id'] = i
            
    return position_info

def parse_ensembl_genes(lines):
    """Parse a file from ENSEMBL with gene information
    
        This file was produced from ensembl biomart
        
        Args:
            lines (Iterator): The lines of the file
        
        Returns:
            genes(dict): A dictionary with HGNC id:s as keys and other info 
                        as values
    """
    genes = {}
    # Since the order of the columns could differ we need to parse the 
    #header first
    position_info = {}
    for i,line in enumerate(lines):
        if i == 0:
            position_info = parse_ensembl_header(line)
        else:
            line = line.rstrip().split('\t')
            gene_info = {}
            
            chrom_pos = position_info.get('chrom')
            if chrom_pos != None:
                if len(line) > chrom_pos:
                    gene_info['chrom'] = line[chrom_pos]
            
            start_pos = position_info.get('start')
            if start_pos != None:
                if len(line) > start_pos:
                    gene_info['start'] = line[start_pos]
            
            stop_pos = position_info.get('stop')
            if stop_pos != None:
                if len(line) > stop_pos:
                    gene_info['stop'] = line[stop_pos]
            
            id_pos = position_info.get('geneid')
            if id_pos != None:
                if len(line) > id_pos:
                    gene_info['ensembl_id'] = line[id_pos]
            
            desc_pos = position_info.get('description')
            if desc_pos != None:
                if len(line) > desc_pos:
                    description = line[desc_pos].split('[')
                    gene_info['description'] = description[0]

            hgnc_id_pos = position_info.get('hgnc_id')            
            if hgnc_id_pos != None:
                if len(line) > hgnc_id_pos:
                    hgnc_id = line[hgnc_id_pos]
                    gene_info['hgnc_id'] = hgnc_id

            hgnc_pos = position_info.get('hgnc_symbol')            
            hgnc_symbol = None
            if hgnc_pos != None:
                if len(line) > hgnc_pos:
                    hgnc_symbol = line[hgnc_pos]
            
            if hgnc_symbol:
                genes[hgnc_symbol] = gene_info
            else:
                if 'unknown' in genes:
                    genes['unknown'].append(gene_info)
                else:
                    genes['unknown'] = [gene_info]
    return genes


@click.command()
@click.argument('infile',
    type=click.Path(exists=True)
)
@click.option('-h', '--hi_scores',
    type=click.Path(exists=True),
    help='File with haploinsufficiency scores'
)
@click.option('-c', '--constraint_scores',
    type=click.Path(exists=True),
    help='File with Exac constraint scores'
)
@click.option('-m', '--mode',
    type=click.Choice(['genes', 'uniqify', 'phenotype', 'disease']),
    default='genes',
)
@click.option('-o', '--outfile',
    type=click.Path(exists=False),
)
def cli(infile, mode, hi_scores, constraint_scores, outfile):
    """docstring for cli"""
    from pprint import pprint as pp
    genes = {}
    file_name, file_extension = os.path.splitext(infile)
    if file_extension == '.gz':
        logger.debug("File is zipped")
        file_handle = gzip.open(infile)
    else:
        file_handle = open(infile, mode='r', encoding='utf-8', errors='replace')
    
    if outfile:
        out_handle = gzip.open(outfile, 'wb')
    
    if 'genes' in mode:
        genes = parse_ensembl_genes(file_handle)
    
    elif mode == 'uniqify':
        #This is for making unique phenotypes
        result = uniqify_phenotypes(file_handle)
        header = '#HPOID\tDescription'
        if outfile:
            out_handle.write(header)
        else:
            print(header)
        
        for hpo_id in result:
            print_line = "{0}\t{1}".format(hpo_id, result[hpo_id])
            if outfile:
                out_handle.write(print_line+"\n")
            else:
                print(print_line)
        if outfile:
            out_handle.close()
    
    elif mode == 'phenotype':
        for phenotype in parse_phenotypes(file_handle):
            pp(phenotype)
    
    elif mode == 'disease':
        for disease in parse_diseases(file_handle):
            pp(disease)

    if hi_scores:
        file_name, file_extension = os.path.splitext(hi_scores)
        if file_extension == '.gz':
            logger.debug("File is zipped")
            hi_handle = gzip.open(hi_scores)
        else:
            hi_handle = open(hi_scores, mode='r', encoding='utf-8', errors='replace')
        for res in get_hi_scores(hi_handle):
            hgnc_id = res[0]
            hi_score = res[1]
            if hgnc_id in genes:
                genes[hgnc_id]['hi_score'] = hi_score

    if constraint_scores:
        file_name, file_extension = os.path.splitext(constraint_scores)
        if file_extension == '.gz':
            logger.debug("File is zipped")
            constraint_handle = gzip.open(constraint_scores)
        else:
            constraint_handle = open(constraint_scores, mode='r', 
                                    encoding='utf-8', errors='replace')
        for res in get_constraint_scores(constraint_handle):
            hgnc_id = res[0]
            constraint_score = res[1]
            if hgnc_id in genes:
                genes[hgnc_id]['constraint_score'] = constraint_score
    
    header = "#chrom\tstart\tstop\tensembl_id\tdescription\thgnc_symbol\t"\
             "hgnc_id\thi_score\tconstraint_score"
    if outfile:
        out_handle.write(header + '\n')
    else:
        print(header)

    for hgnc_symbol in genes:
        if hgnc_symbol != 'unknown':
            gene_info = genes[hgnc_symbol]
            print_line = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}".format(
                gene_info.get('chrom', 'unknown'),
                gene_info.get('start', '0'),
                gene_info.get('stop', '0'),
                gene_info.get('ensembl_id', 'unknown'),
                gene_info.get('description', ''),
                hgnc_symbol,
                gene_info.get('hgnc_id', ''),
                gene_info.get('hi_score', ''),
                gene_info.get('constraint_score', ''),
            )
        if outfile:
            out_handle.write(print_line + '\n')
        else:
            print(print_line)

    unknown_genes = genes['unknown']
    for gene_info in unknown_genes:
        print_line = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}".format(
            gene_info.get('chrom', 'unknown'),
            gene_info.get('start', '0'),
            gene_info.get('stop', '0'),
            gene_info.get('ensembl_id', 'unknown'),
            gene_info.get('description', ''),
            '',
            '',
            '',
            ''
        )
        if outfile:
            out_handle.write(print_line + '\n')
        else:
            print(print_line)


if __name__ == '__main__':
    cli()

