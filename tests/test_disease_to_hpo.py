def test_if_exists(mim_terms):
    """docstring for test_parse_lines"""
    mim_ids = set()
    for disease in mim_terms:
        mim_ids.add(disease['mim_number'])
    
    assert 600920 in mim_ids

def test_hpo_terms(mim_terms):
    """docstring for test_hpo_terms"""
    hpo_terms = set()
    for disease in mim_terms:
        hpo_terms.add(disease['hpo_id'])
    
    for term in [767,3042,5280,1363,772,1195,2987]:
        assert term in hpo_terms

def test_keys(mim_terms):
    """docstring for test_check_dict"""

    mim_ids = set()
    for disease in mim_terms:
        mim_ids.add(disease['mim_number'])

    assert mim_ids == set([615206,613376,600920])

def test_gene_symbol(mim_terms):
    """docstring for test_check_dict"""

    mim_ids = set()
    for disease in mim_terms:
        if disease['mim_number'] == 600920:
            assert disease['hgnc_symbol'] == 'SCARF2'
