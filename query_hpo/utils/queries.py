import logging
import sqlite3
from query_hpo.database import get_database

logger = logging.getLogger(__name__)

def query_hpo(hpo_terms, database=None):
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
    connection = get_database(path_to_database=database)
    
    connection.row_factory = sqlite3.Row
    
    cursor = connection.cursor()
    
    answer = []
    
    for hpo_term in hpo_terms:
        try:
            hpo_term = int(hpo_term.lstrip('HP:'))
        except ValueError as e:
            logger.error("{0} is not a valid HPO term".format(hpo_term))
            raise e
        
        cursor.execute("SELECT * FROM hpo WHERE hpo_id = '{0}'".format(hpo_term))
        
        for row in cursor.fetchall():
            answer.append({
                'hpo_term': row['name'],
                'description': row['description']
            })
    
    return answer

def query_disease(disease_terms, database=None):
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
    connection = get_database(path_to_database=database)
    
    connection.row_factory = sqlite3.Row
    
    cursor = connection.cursor()
    
    answer = []
    
    for disease_term in disease_terms:
        disease_term = int(disease_term.lstrip('OMIM:'))
        cursor.execute("SELECT * FROM disease WHERE mim_nr = '{0}'".format(disease_term))
        
        for row in cursor.fetchall():
            
            answer.append({
                'hpo_term': row['name'],
                'description': row['description']
            })
    
    return answer
    