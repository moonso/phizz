import sqlite3
from phizz.database import (populate_hpo, populate_disease, get_cursor)
from phizz.log import configure_stream

configure_stream(level="DEBUG")

schema_filename = "tests/fixtures/schema.sql"


def test_populate_hpo(connection, hpo_terms, mim_terms):
    """docstring for test_populate_hpo"""
    populate_hpo(
        connection=connection, 
        hpo_terms=hpo_terms, 
    )

    cursor = get_cursor(connection=connection)
    
    cursor.execute("SELECT * from hpo where hpo_id = '1459'")

    for row in cursor.fetchmany():
        assert row['description'] == "1-3 toe syndactyly"
        assert row['name'] == "HP:0001459"
    

def test_get_hpo_from_omim(connection, hpo_terms, mim_terms):
    """docstring for test_get_description"""
    populate_disease(
        connection=connection, 
        disease_terms=mim_terms, 
    )

    cursor = get_cursor(connection=connection)

    cursor.execute("SELECT * FROM disease WHERE mim_nr = '600920'")
    
    hpo_ids = set()
    for row in cursor.fetchall():
        hpo_ids.add(row['mim_hpo'])

    assert hpo_ids == set([767, 3042,5280,1363,772,1195,2987])

