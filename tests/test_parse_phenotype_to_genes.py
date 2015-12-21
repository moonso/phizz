
from phizz.utils import parse_phenotypes


def test_first_term(hpo_terms):
    for term in hpo_terms:
        assert term['hpo_id'] == 3295
        assert term['name'] == "HP:0003295"
        assert term['description'] == "Impaired FSH and LH secretion"
        break

def test_multiple_term(hpo_terms):
    terms = set()
    for term in hpo_terms:
        terms.add(term['hpo_id'])
    assert len(terms) == 24

