import logging
import gzip

from codecs import getreader

from phizz.utils import (parse_phenotypes, parse_diseases, parse_genes)

from .constants import (disease_to_genes_path, phenotypes_path, genes_path,
                        schema_path)

from . import (populate_hpo, populate_disease, populate_genes)

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

    logger.info("Fetching genes file")
    genes = getreader('utf-8')(
        gzip.open(genes_path), errors='replace')
    
    logger.info("Parsing phenotypes to gene file")    
    phenotypes = parse_phenotypes(phenotype_to_genes)
    logger.info("Parsing disease to gene file")    
    diseases = parse_diseases(disease_to_genes)
    logger.info("Parsing genes  file")    
    genes = parse_genes(genes)
    

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

    logger.info("Populating gene table")    
    populate_genes(
        connection=connection, 
        genes=genes
    )
    logger.debug("Gene table populated")
    