from phizz.utils import query_gene
import pytest

def test_query_ensembl_id(database):
    ensembl_id = 'ENSG00000070814'
    hgnc_symbol = 'TCOF1'
    result = query_gene(ensembl_id=ensembl_id, connection=database)
    gene = result[0]
    assert gene['ensembl_id'] == ensembl_id
    assert gene['hgnc_symbol'] == hgnc_symbol

def test_query_ensembl_id(database):
    ensembl_id = 'ENSG00000070814'
    hgnc_symbol = 'TCOF1'
    result = query_gene(hgnc_symbol=hgnc_symbol, connection=database)
    gene = result[0]
    assert gene['ensembl_id'] == ensembl_id
    assert gene['hgnc_symbol'] == hgnc_symbol

def test_query_no_term(database):
    """docstring for query_term"""
    with pytest.raises(SyntaxError):
        result = query_gene(connection=database)

def test_query_wrong_term(database):
    """docstring for query_term"""
    term = 'HPO'
    with pytest.raises(ValueError):
        result = query_gene(term, connection=database)

def test_query_non_existing_term(database):
    """docstring for query_term"""
    term = 'ENSG00000000004'
    result = query_gene(term, connection=database)
    assert result == []
