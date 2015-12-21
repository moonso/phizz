import logging
from sqlite3 import OperationalError

logger = logging.getLogger(__name__)

def populate_hpo(connection, hpo_terms):
    """Populate the hpo database
    
        Args:
            connection (sqlite3.Connect): A connection object
            hpo_terms (generator): HPO terms
    """
    
    for term in hpo_terms:
        name = term['name']
        hpo_id = term['hpo_id']
        description = term['description']
        
        logger.debug("Inserting {0} into hpo table".format(name))
        description = description.replace("'", '')
        
        try:
            connection.execute("INSERT INTO hpo (hpo_id, name, description) "\
                "values (?, ?, ?)", (hpo_id, name, description))
        except OperationalError as e:
            logger.error("Bad entry {0} {1} {2}".format(
                hpo_id, name, description
            ))
            raise e
        
    connection.commit()
    logger.debug("Hpo terms inserted")
    return
    

def populate_disease(connection, disease_terms):
    """Populate the disease database
    
        Args:
            connection (sqlite3.Connect): A connection object
            disease_terma (dict): A disease dict
    """
    
    i = 0
    for entry in disease_terms:
        i += 1
        mim_nr = entry['mim_number']
        mim_hpo = entry['hpo_id']
        hgnc_symbol = entry['hgnc_symbol']
        
        logger.debug("Inserting mim term: {0}, hpo_id:{1}, hgnc_symbol:{2}"\
        " into disease table".format(mim_nr, mim_hpo, hgnc_symbol))
        
        connection.execute("INSERT INTO disease (disease_id, mim_nr,"\
                " hgnc_symbol, mim_hpo) values (?,?,?,?)", (i, mim_nr, hgnc_symbol, mim_hpo))
        
    connection.commit()
    logger.debug("Insertion done")
    return

def populate_genes(connection, genes):
    """Populate the disease database
    
        Args:
            connection (sqlite3.Connect): A connection object
            genes (dict): A disease dict
    """
    
    i = 0
    for entry in genes:
        i += 1
        ensembl_id = entry['ensembl_id']
        hgnc_symbol = entry.get('hgnc_symbol')
        hgnc_id = entry.get('hgnc_id')
        description = entry.get('description')
        chrom = entry['chrom']
        start = int(entry['start'])
        stop = int(entry['stop'])
        hi_score = entry.get('hi_score')
        if hi_score:
            hi_score = float(hi_score)
        constraint_score = entry.get('constraint_score')
        if constraint_score:
            constraint_score = float(constraint_score)
        
        logger.debug("Inserting gene: {0} into gene table".format(ensembl_id))
        
        connection.execute("INSERT INTO gene (gene_id, ensembl_id, hgnc_symbol"\
                           ", hgnc_id, description, chrom, start, stop, hi_score,"\
                           " constraint_score) values (?,?,?,?,?,?,?,?,?,?)", 
                           (i, ensembl_id, hgnc_symbol, hgnc_id, description, chrom, 
                           start, stop, hi_score, constraint_score))
        
    connection.commit()
    logger.debug("Insertion done")
    return
