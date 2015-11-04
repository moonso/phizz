from phizz.utils import query_disease
import pytest

def test_query_disease():
    """docstring for query_term"""
    term = 'OMIM:614300'
    result = query_disease([term])
    hpo_dict = result[0]
    assert hpo_dict['hpo_term'] == "HP:0000256"
    assert hpo_dict['description'] == 'Macrocephaly'

def test_query_wrong_term():
    """docstring for query_term"""
    term = 'MIM'
    with pytest.raises(ValueError):
        result = query_disease([term])

def test_query_non_existing_term():
    """docstring for query_term"""
    term = 'OMIM:1'
    result = query_disease([term])
    assert result == []
