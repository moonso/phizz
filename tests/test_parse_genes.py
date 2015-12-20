
def test_number(genes):
    gene_list = []
    for gene in genes:
        gene_list.append(gene)
    assert len(gene_list) == 4


def test_lacking_info(genes):
    gene_list = []
    for gene in genes:
        if gene['ensembl_id'] == "ENSG00000227890":
            assert gene['start'] == '203044020'
            assert gene['stop'] == '203044694'
            assert 'description' in gene
            assert gene['hgnc_symbol'] == 'PSMA2P3'
            assert 'hi_score' not in gene

def test_lacking_hi_score(genes):
    gene_list = []
    for gene in genes:
        if gene['ensembl_id'] == "ENSG00000126653":
            assert gene['hgnc_symbol'] == 'NSRP1'
            assert gene['hi_score'] == ''
            assert gene['constraint_score'] == '2.9732792450519'

