import sqlite3
import pytest
from phizz.database import (populate_hpo, populate_disease, get_database)
from phizz.utils import (parse_phenotypes, parse_diseases, parse_genes)

from phizz.log import configure_stream

logger = configure_stream(level="DEBUG")


SCHEMA = 'tests/fixtures/schema.sql'

@pytest.fixture(scope="function")
def mim_terms(request):
    """Get mim terms"""
    mim_lines = [
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
    return parse_diseases(mim_lines)

@pytest.fixture(scope="function")
def hpo_terms(request):
    """Get hpo terms"""
    hpo_lines = [
        "#Format: HPO-ID<tab>HPO-Name<tab>Gene-ID<tab>Gene-Name",
        "HP:0003295\tImpaired FSH and LH secretion",
        "HP:0003564\tFolate-dependent fragile site at Xq28",
        "HP:0003565\tElevated erythrocyte sedimentation rate",
        "HP:0003562\tAbnormal metaphyseal vascular invasion",
        "HP:0003563\tHypobetalipoproteinemia",
        "HP:0003292\tDecreased serum leptin",
        "HP:0003561\tBirth length less than 3rd percentile",
        "HP:0001403\tMacrovesicular hepatic steatosis",
        "HP:0003298\tSpina bifida occulta",
        "HP:0003296\tHyperthreoninuria",
        "HP:0003568\tDecreased glucosephosphate isomerase activity",
        "HP:0012393\tAllergy",
        "HP:0003297\tHyperlysinuria",
        "HP:0001153\tSeptate vagina",
        "HP:0001152\tSaccadic smooth pursuit",
        "HP:0030012\tAbnormal female reproductive system physiology",
        "HP:0003560\tMuscular dystrophy",
        "HP:0000767\tPectus excavatum",
        "HP:0003042\tElbow dislocation",
        "HP:0005280\tDepressed nasal bridge",
        "HP:0001363\tCraniosynostosis",
        "HP:0000772\tAbnormality of the ribs",
        "HP:0001195\tSingle umbilical artery",
        "HP:0002987\tElbow flexion contracture"
    ]
    return parse_phenotypes(hpo_lines)

@pytest.fixture(scope="function")
def genes(request):
    """Get hpo terms"""
    gene_lines = [
       "#Chrom\tStart\tEnd\tENSGID\tDescription\tHGNC_symbol",
       "13\t23551994\t23552136\tENSG00000223116\t\t",
       "13\t23708313\t23708703\tENSG00000233440\thigh mobility group AT-hook"\
       " 1 pseudogene 6 [Source:HGNC Symbol;Acc:19121]\tHMGA1P6",
       "13\t23726725\t23726825\tENSG00000207157\tRNA, Ro-associated Y3"\
       " pseudogene 4 [Source:HGNC Symbol;Acc:42488]\tRNY3P4",
       "13\t23743974\t23744736\tENSG00000229483\tlong intergenic non-protein"\
       " coding RNA 362 [Source:HGNC Symbol;Acc:42682]\tLINC00362",
       "13\t23791571\t23791673\tENSG00000252952\tRNA, U6 small nuclear 58,"\
       " pseudogene [Source:HGNC Symbol;Acc:42548]\tRNU6-58P",
    ]
    return parse_genes(gene_lines)


@pytest.fixture(scope='function')
def connection(request):
    """Return a connection to a database"""
    conn = get_database(":memory:", SCHEMA)
    def teardown():
        print('\n')
        logger.info('Closing connection')
        conn.close()
        logger.debug('Connection closed')
    request.addfinalizer(teardown)
    
    return conn


@pytest.fixture(scope='function')
def database(request, connection, hpo_terms, mim_terms):
    """Return a populated database"""
    
    populate_hpo(
        connection=connection, 
        hpo_terms=hpo_terms, 
    )
    
    populate_disease(
        connection=connection, 
        disease_terms=mim_terms
        
    )    
    return connection
    
