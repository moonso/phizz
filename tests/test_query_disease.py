from phizz.utils import query_disease

import pytest

def test_query_disease(database):
    """docstring for query_term"""
    term = 'OMIM:600920'
    result = query_disease([term], connection=database)
    
    cursor = database.cursor()
    
    hpo_terms = set()
    for res in result:
        hpo_terms.add(res['hpo_term'])
    
    assert "HP:0000767" in hpo_terms
    assert "HP:0003042" in hpo_terms

def test_query_wrong_term(database):
    """docstring for query_term"""
    term = 'MIM'
    with pytest.raises(ValueError):
        result = query_disease([term], connection=database)

def test_query_non_existing_term(database):
    """docstring for query_term"""
    term = 'OMIM:1'
    result = query_disease([term], connection=database)
    assert result == []
