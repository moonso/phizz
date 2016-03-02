from phizz.utils import query_gene_symbol
import pytest

def test_query_ensembl_id():
    chrom = '11'
    start = 121008681
    stop = 121008681
    result = query_gene_symbol(chrom, start, stop)
    assert result == ['TECTA']
