import logging
from sqlite3 import OperationalError

logger = logging.getLogger(__name__)

def populate_hpo(connection, hpo_terms):
    """Populate the hpo database
    
        Args:
            connection (sqlite3.Connect): A connection object
            hpo_terms (dict): A HPO dict
    """
    
    for hpo_id in hpo_terms:
        logger.debug("Inserting {0} into hpo table".format(hpo_id))
        name = hpo_terms[hpo_id]['name']
        description = hpo_terms[hpo_id]['description'].replace("'", '')
        
        try:
            connection.execute("INSERT INTO hpo (hpo_id, name, description) "\
                "values ('{0}', '{1}', '{2}')".format(
                hpo_id, name, description))
        except OperationalError as e:
            logger.error("Bad entry {0} {1} {2}".format(
                hpo_id, name, description
            ))
            raise e
        
        logger.debug("Inserting done")
    
    connection.commit()

def populate_disease(connection, disease_terms):
    """Populate the disease database
    
        Args:
            connection (sqlite3.Connect): A connection object
            disease_terma (dict): A disease dict
    """
    
    i = 0
    for mim_nr in disease_terms:
        for mim_hpo in disease_terms[mim_nr]:
            i += 1
            logger.debug("Inserting mim term {0}, hpo_id:{1} into disease table".format(
                mim_nr, mim_hpo
            ))
            connection.execute("INSERT INTO disease (disease_id, mim_nr,"\
                " mim_hpo) values ('{0}', '{1}', '{2}')".format(
                    i, mim_nr, mim_hpo))
            logger.debug("Insertion done")
    connection.commit()
        