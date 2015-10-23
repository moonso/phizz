from query_hpo import get_database
import pytest

SCHEMA = 'tests/fixtures/schema.sql'

def test_get_database_no_schema():
    """docstring for test_database"""
    #Should provide a schema
    with pytest.raises(IOError):
        connection = get_database(":memory:")

def test_get_database():
    """docstring for test_database"""
    
    connection = get_database(":memory:", SCHEMA)
    assert connection