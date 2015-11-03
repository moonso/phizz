import os
import gzip
import logging
from codecs import open, getreader

import click

logger = logging.getLogger(__name__)


def parse_phenotype_to_genes(lines):
    """Pare phenotype to genes
    
        Go through the file and return a dictionary with hpo terms as key
        and a dictionary with {description:text, genes:set([list_of_genes])}
        
        Args:
            lines (Iterator): The lines of the file
        
        Returns:
            hpo_terms (dict): A hpo dict described above
    """
    
    hpo_terms = {}
    
    for line in lines:
        if not line.startswith('#'):
            line = line.rstrip().split('\t')
            name = line[0]
            logger.debug("Parsing hpo term {0}".format(name))
            hpo_term = int(name.lstrip('HP:'))
            description = line[1]
            logger.debug("Found description {0}".format(description))
            gene_id = line[2]
            gene_name = line[3]
            if hpo_term in hpo_terms:
                hpo_terms[hpo_term]['genes'].add(gene_name)
            else:
                hpo_terms[hpo_term] = {
                    'name': name,
                    'description' : description,
                    'genes' : set([gene_name])
                    }
    
    return hpo_terms

def parse_disease_to_hpo(lines):
    """Parse disease to phenotype
    
        Build a dictionary with mim number as key
    """
    disease_to_hpo = {}
    
    for line in lines:
        if not (line.startswith('#') or line.startswith('ORPHAN')):
            line = line.split('\t')
            mim_number = int(line[0].lstrip('OMIM:'))
            logger.debug("Found mim number {0}".format(mim_number))
            hpo_id = int(line[3].lstrip('HP:'))
            logger.debug("Found hpo term {0} for mim number {1}".format(
                hpo_id, mim_number))
            
            if mim_number in disease_to_hpo:
                disease_to_hpo[mim_number].add(hpo_id)
            else:
                disease_to_hpo[mim_number] = set([hpo_id])
    
    return disease_to_hpo

