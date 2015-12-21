from phizz.utils import query_hpo
import pytest

def test_query_term(database):
    """docstring for query_term"""
    term = 'HP:0003295'
    result = query_hpo([term], connection=database)
    hpo_dict = result[0]
    assert hpo_dict['hpo_term'] == term
    assert hpo_dict['description'] == 'Impaired FSH and LH secretion'

def test_query_wrong_term(database):
    """docstring for query_term"""
    term = 'HPO'
    with pytest.raises(ValueError):
        result = query_hpo([term], connection=database)

def test_query_non_existing_term(database):
    """docstring for query_term"""
    term = 'HP:0000001'
    result = query_hpo([term], connection=database)
    assert result == []
