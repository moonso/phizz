import logging
import sqlite3
from phizz.database import get_database

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
        
        hpo_result = cursor.execute("SELECT * FROM hpo"\
                        " WHERE hpo_id = '{0}'".format(hpo_term)).fetchall()
        
        for row in hpo_result:
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
    cursor2 = connection.cursor()
    answer = []
    
    for disease_term in disease_terms:
        try:
            disease_term = int(disease_term.lstrip('OMIM:'))
        except ValueError as e:
            logger.error("{0} is not a valid OMIM term".format(disease_term))
            raise e
            
        disease_result = cursor.execute("SELECT * FROM disease WHERE"\
                            " mim_nr = '{0}'".format(disease_term)).fetchall()
        
        for row in disease_result:
            disease_hpo = row['mim_hpo']
            
            hpo_result = cursor.execute("SELECT * FROM hpo"\
                            " WHERE hpo_id = '{0}'".format(disease_hpo)).fetchall()
            
            for hpo_row in hpo_result:
                answer.append({
                    'hpo_term': hpo_row['name'],
                    'description': hpo_row['description']
                })
    
    return answer
    