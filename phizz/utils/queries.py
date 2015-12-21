import logging
import sqlite3
from phizz.database import get_cursor

logger = logging.getLogger(__name__)

def query_hpo(hpo_terms, database=None, connection=None):
    """Query with hpo terms
    
        If no databse is given use the one that follows with package
        
        Args:
            hpo_terms (iterator): An iterator with hpo terms
            database (str): Path to database
        
        Returns:
            answer (list): A list of dictionaries where each dictionary 
            represents a hpo term on the form {'hpo_term': <hpo_term>,
            'description':<description>}
            
    """
    cursor = get_cursor(
        path_to_database=database, 
        connection=connection
    )
    
    answer = []
    
    for hpo_term in hpo_terms:
        try:
            hpo_term = int(hpo_term.lstrip('HP:'))
        except ValueError as e:
            logger.error("{0} is not a valid HPO term".format(hpo_term))
            raise e
        
        hpo_result = cursor.execute("SELECT * FROM hpo"\
                        " WHERE hpo_id = '{0}'".format(hpo_term)).fetchall()
        
        for row in hpo_result:
            answer.append({
                'hpo_term': row['name'],
                'description': row['description']
            })
    
    return answer

def query_disease(disease_terms, database=None, connection=None):
    """Query with diseae terms
    
        If no databse is given use the one that follows with package
        
        Args:
            hpo_terms (iterator): An iterator with hpo terms
            database (str): Path to database
        
        Returns:
            answer (list): A list of dictionaries where each dictionary 
            represents a hpo term on the form {'hpo_term': <hpo_term>,
            'description':<description>}
            
    """
    cursor = get_cursor(
        path_to_database=database, 
        connection=connection
    )
    
    answer = []
    
    for disease_term in disease_terms:
        try:
            disease_term = int(disease_term.lstrip('OMIM:'))
            logger.debug("Querying diseases with {0}".format(disease_term))
        except ValueError as e:
            logger.error("{0} is not a valid OMIM term".format(disease_term))
            raise e
            
        result = cursor.execute("SELECT hpo.name, hpo.description"\
                                " FROM hpo, disease WHERE"\
                                " hpo.hpo_id = disease.mim_hpo"\
                                " AND disease.mim_nr = ?", (str(disease_term),)).fetchall()
        
        for hpo_row in result:
            answer.append({
                'hpo_term': hpo_row['name'],
                'description': hpo_row['description']
            })
    
    return answer

def query_gene(ensembl_id=None, hgnc_symbol=None, database=None, connection=None):
    """Query with gene symbols, either hgnc or ensembl
    
        If no database is given use the one that follows with package
        
        Args:
            ensemb_id (str): A ensembl gene id
            hgnc_symbol (str): A hgnc symbol
            database (str): Path to database
        
        Returns:
            answer (iterator)
            
    """
    cursor = get_cursor(
        path_to_database=database, 
        connection=connection
    )
    
    result = []
    
    if not (ensembl_id or hgnc_symbol):
        raise SyntaxError("Use gene identifier to query")
    if ensembl_id:
        if not ensembl_id.startswith("ENSG"):
            raise ValueError("invalid format for ensemb id")
        logger.debug("Querying genes with ensembl id {0}".format(ensembl_id))
        
        result = cursor.execute("SELECT * FROM gene WHERE"\
                                " ensembl_id = ?" , (ensembl_id,)).fetchall()
    else:
        logger.debug("Querying genes with hgnc symbol {0}".format(hgnc_symbol))
        result = cursor.execute("SELECT * FROM gene WHERE"\
                                " hgnc_symbol = ?" , (hgnc_symbol,)).fetchall()
    return result
    