import os
import gzip
import logging
from codecs import open

import click

logger = logging.getLogger(__name__)

def parse_phenotypes(lines):
    """Pare phenotype file
    
        yield dicts with {
            'hpo_id': hpo_id(int),
            'name': hpo_name(str)
            'description: description(str)
        }
        
        Args:
            lines (Iterator): The lines of the file
        
        Yields:
            hpo_terms (dict): A hpo dict described above
    """
    
    hpo_term = {}
    
    for line in lines:
        if not line.startswith('#'):
            line = line.rstrip().split('\t')
            hpo_name = line[0]
            hpo_id = int(line[0].lstrip('HPO:'))
            logger.debug("Parsing hpo term {0}".format(hpo_id))
            description = line[1]
            logger.debug("Found description {0}".format(description))
            phenotype_info = {
                'hpo_id': hpo_id,
                'name': hpo_name,
                'description': description
            }
            yield phenotype_info

def parse_diseases(lines):
    """Parse disease to phenotype
    
        Build dictionaries with information about diseases
        
        Args:
            lines(iterator): The content of the disease file
        
        Yields:
            dict on the form described above
            
        
    """
    for line in lines:
        if not (line.startswith('#') or line.startswith('ORPHAN')):
            line = line.split('\t')
            mim_name = line[0]
            mim_number = int(line[0].lstrip('OMIM:'))
            logger.debug("Found omim disease {0}".format(mim_name))
            hgnc_symbol = line[1]
            hpo_id = int(line[3].lstrip('HP:'))
            logger.debug("Found hpo term {0} for mim number {1}".format(
                hpo_id, mim_number))
            
            disease_info = {
                'mim_name': mim_name,
                'mim_number': mim_number,
                'hgnc_symbol': hgnc_symbol,
                'hpo_id': hpo_id
            }
            yield disease_info

def parse_genes(lines):
    """Parse an ensembl file with genes
        
        Header should look like: 
        #chrom\tstart\tstop\tensembl_id\tdescription\thgnc_symbol\thi_score\t
         constraint_score
        
        Args:
            lines(iterator): The content of the genes file
    """
    genes = []
    header = []
    for line in lines:
        line = line.rstrip()
        if line.startswith('#'):
            header = line[1:].split('\t')
        else:
            yield dict(zip(header, line.split('\t')))
            
