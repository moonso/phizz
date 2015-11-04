from phizz.utils import query_hpo
import pytest

def test_query_term():
    """docstring for query_term"""
    term = 'HP:0000002'
    result = query_hpo([term])
    hpo_dict = result[0]
    assert hpo_dict['hpo_term'] == term
    assert hpo_dict['description'] == 'Abnormality of body height'

def test_query_wrong_term():
    """docstring for query_term"""
    term = 'HPO'
    with pytest.raises(ValueError):
        result = query_hpo([term])

def test_query_non_existing_term():
    """docstring for query_term"""
    term = 'HP:0000001'
    result = query_hpo([term])
    assert result == []
