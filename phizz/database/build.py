import logging
import gzip

from codecs import getreader

from phizz.utils import (parse_phenotypes, parse_diseases)

from .constants import (disease_to_genes_path, phenotypes_path, 
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
    
    logger.info("Fetching phenotypes file")
    phenotype_to_genes = getreader('utf-8')(
        gzip.open(phenotypes_path), errors='replace')
    
    logger.info("Parsing phenotypes to gene file")    
    phenotypes = parse_phenotypes(phenotype_to_genes)
    logger.info("Parsning disease to gene file")    
    diseases = parse_diseases(disease_to_genes)
    

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
    