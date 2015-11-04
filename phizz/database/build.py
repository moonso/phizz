import logging
import gzip

from codecs import getreader

from phizz.utils import (parse_phenotype_to_genes, parse_disease_to_hpo)

from .constants import (disease_to_genes_path, phenotype_to_genes_path, 
schema_path)

from . import (populate_hpo, populate_disease)

logger = logging.getLogger(__name__)

def build_database(connection):
    """Build the hpo database
    
        Args:
            conn (sqlite3.connect): A database connection object
    """
    logger.info("Fetching disease to gene file")
    disease_to_genes = getreader('utf-8')(
        gzip.open(disease_to_genes_path), errors='replace')
    
    logger.info("Fetching phenotypes to gene file")
    phenotype_to_genes = getreader('utf-8')(
        gzip.open(phenotype_to_genes_path), errors='replace')
    
    logger.info("Parsning phenotypes to gene file")    
    phenotypes = parse_phenotype_to_genes(phenotype_to_genes)
    logger.info("Parsning disease to gene file")    
    diseases = parse_disease_to_hpo(disease_to_genes)
    

    logger.info("Populating hpo table")
    populate_hpo(
        connection=connection, 
        hpo_terms=phenotypes
    )
    logger.debug("Hpo table populated")
    
    logger.info("Populating disease table")    
    populate_disease(
        connection=connection, 
        disease_terms=diseases
    )
    logger.debug("Disease table populated")
    