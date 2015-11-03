from query_hpo.log import configure_stream

configure_stream(level="DEBUG")

from query_hpo.utils import parse_phenotype_to_genes

LINES = [
    "#Format: HPO-ID<tab>HPO-Name<tab>Gene-ID<tab>Gene-Name",
    "HP:0001459\t1-3 toe syndactyly\t2737\tGLI3",
    "HP:0006088\t1-5 finger complete cutaneous syndactyly\t64327\tLMBR1",
    "HP:0010708\t1-5 finger syndactyly\t64327\tLMBR1",
    "HP:0010713\t1-5 toe syndactyly\t2737\tGLI3",
    "HP:0000878\t11 pairs of ribs\t10013\tHDAC6",
    "HP:0000878\t11 pairs of ribs\t3930\tLBR",
    "HP:0000878\t11 pairs of ribs\t6662\tSOX9",
    "HP:0000878\t11 pairs of ribs\t100151683\tRNU4ATAC",
    "HP:0000878\t11 pairs of ribs\t545\tATR",
    "HP:0000878\t11 pairs of ribs\t6628\tSNRPB",
    "HP:0000878\t11 pairs of ribs\t6223\tRPS19",
    "HP:0000878\t11 pairs of ribs\t126792\tB3GALT6",
    "HP:0000878\t11 pairs of ribs\t2317\tFLNB",
    "HP:0001233\t2-3 finger syndactyly\t2255\tFGF10",
    "HP:0001233\t2-3 finger syndactyly\t2719\tGPC3",
    "HP:0001233\t2-3 finger syndactyly\t51057\tWDPCP",
    "HP:0001233\t2-3 finger syndactyly\t50964\tSOST",
    "HP:0001233\t2-3 finger syndactyly\t5307\tPITX1",
    "HP:0001233\t2-3 finger syndactyly\t2261\tFGFR3",
    "HP:0001233\t2-3 finger syndactyly\t2263\tFGFR2"
]

HPO_DICT = parse_phenotype_to_genes(LINES)

def test_first_term():
    """docstring for test_parse_lines"""
    
    entry = HPO_DICT[1459]
    assert len(entry['genes']) == 1
    assert entry['name'] == "HP:0001459"
    assert entry['description'] == "1-3 toe syndactyly"

def test_multiple_term():
    """docstring for test_parse_lines"""
    
    assert len(HPO_DICT[878]['genes']) == 9

