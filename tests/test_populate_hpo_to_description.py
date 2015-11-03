import sqlite3
from query_hpo.database import populate_hpo, populate_disease
from query_hpo.log import configure_stream

configure_stream(level="DEBUG")

schema_filename = "tests/fixtures/schema.sql"



class TestPopulate:
    """Test to populate a hpo to phenotype db"""
    
    def setup(self):
        """Setup an in memory sqlite database"""
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        with open(schema_filename, 'rt') as f:
                schema = f.read()
        
        self.conn.executescript(schema)
        
        hpo_dict = {
            1459:{
                'name': "HP:0001459",
                'description': "1-3 toe syndactyly",
                'genes': set(['GLI3'])
            },
            6088:{
                'name': "HP:0001459",
                'description': "1-5 finger complete cutaneous syndactyly",
                'genes': set(['LMBR1', 'GLI3'])
            }
        }
        
        disease_terms = {
            600920: set([1459, 6088])
        }
        
        populate_hpo(
            connection=self.conn, 
            hpo_terms=hpo_dict, 
        )
        
        populate_disease(
            connection=self.conn, 
            disease_terms=disease_terms
            
        )
        
        self.cursor = self.conn.cursor()
    
    def teardown(self):
        self.conn.close()
    
    def test_get_description(self):
        """docstring for test_get_description"""
        self.cursor.execute("select * from hpo where hpo_id = '1459'")
        
        for row in self.cursor.fetchmany():
            assert row['description'] == "1-3 toe syndactyly"
            assert row['name'] == "HP:0001459"
    
    def test_get_hpo_from_omim(self):
        """docstring for test_get_description"""
        
        self.cursor.execute("SELECT * FROM disease WHERE mim_nr = '600920'")
        hpo_ids = set()
        for row in self.cursor.fetchall():
            hpo_ids.add(row['mim_hpo'])

        assert hpo_ids == set([1459,6088])