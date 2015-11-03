from query_hpo.utils import parse_disease_to_hpo

LINES = [
    "#Format: diseaseId<tab>gene-symbol<tab>gene-id(entrez)<tab>HPO-ID<tab>HPO-term-name",
    "OMIM:600920\tSCARF2\t91179\tHP:0000767\tPectus excavatum",
    "OMIM:600920\tSCARF2\t91179\tHP:0003042\tElbow dislocation",
    "OMIM:600920\tSCARF2\t91179\tHP:0005280\tDepressed nasal bridge",
    "OMIM:600920\tSCARF2\t91179\tHP:0001363\tCraniosynostosis",
    "OMIM:600920\tSCARF2\t91179\tHP:0000772\tAbnormality of the ribs",
    "OMIM:600920\tSCARF2\t91179\tHP:0001195\tSingle umbilical artery",
    "OMIM:600920\tSCARF2\t91179\tHP:0002987\tElbow flexion contracture",
    "OMIM:613376\tHSPB3\t8988\tHP:0000006\tAutosomal dominant inheritance",
    "OMIM:613376\tHSPB3\t8988\tHP:0002355\tDifficulty walking",
    "OMIM:613376\tHSPB3\t8988\tHP:0002600\tHyporeflexia of lower limbs",
    "OMIM:613376\tHSPB3\t8988\tHP:0003445\tEMG: neuropathic changes",
    "OMIM:613376\tHSPB3\t8988\tHP:0009830\tPeripheral neuropathy",
    "OMIM:613376\tHSPB3\t8988\tHP:0003376\tSteppage gait",
    "OMIM:613376\tHSPB3\t8988\tHP:0009053\tDistal lower limb muscle weakness",
    "OMIM:613376\tHSPB3\t8988\tHP:0008959\tDistal upper limb muscle weakness",
    "OMIM:613376\tHSPB3\t8988\tHP:0002522\tAreflexia of lower limbs",
    "OMIM:613376\tHSPB3\t8988\tHP:0003677\tSlow progression",
    "OMIM:613376\tHSPB3\t8988\tHP:0003202\tSkeletal muscle atrophy",
    "OMIM:615206\tCARD11\t84433\tHP:0004313\tDecreased antibody level in blood",
    "OMIM:615206\tCARD11\t84433\tHP:0003593\tInfantile onset",
    "OMIM:615206\tCARD11\t84433\tHP:0002205\tRecurrent respiratory infections",
    "OMIM:615206\tCARD11\t84433\tHP:0002721\tImmunodeficiency",
    "OMIM:615206\tCARD11\t84433\tHP:0000007\tAutosomal recessive inheritance",
]

HPO_DICT = parse_disease_to_hpo(LINES)


def test_if_exists():
    """docstring for test_parse_lines"""
    assert 600920 in HPO_DICT

def test_hpo_terms():
    """docstring for test_hpo_terms"""
    assert HPO_DICT[600920] == set([
        767,3042,5280,1363,772,1195,2987])

def test_keys():
    """docstring for test_check_dict"""
    assert set(HPO_DICT.keys()) == set([615206,613376,600920])
