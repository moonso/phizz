import sqlite3
from phizz.database import (populate_genes, get_cursor)
from phizz.log import configure_stream


def test_populate_genes(connection, genes):
    populate_genes(
        connection=connection, 
        genes=genes, 
    )

    cursor = get_cursor(connection=connection)
    
    cursor.execute("SELECT * from gene where ensembl_id = 'ENSG00000070814'")

    for row in cursor.fetchmany():
        assert row['hgnc_symbol'] == "TCOF1"
    

