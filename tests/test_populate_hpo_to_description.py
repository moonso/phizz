import sqlite3
from query_hpo import populate_hpo_to_gene

schema_filename = "tests/fixtures/schema.sql"

class TestPopulate:
    """Test to populate a hpo to phenotype db"""
    
    def setup(self):
        """Setup an in memory sqlite database"""
        self.conn = sqlite3.connect(':memory:')
        with open(schema_filename, 'rt') as f:
                schema = f.read()
                print(schema)
        self.conn.executescript(schema)
        
        hpo_dict = {
            1459:{
                'description': "1-3 toe syndactyly",
                'genes': set(['GLI3'])
            },
            6088:{
                'description': "1-5 finger complete cutaneous syndactyly",
                'genes': set(['LMBR1', 'GLI3'])
            }
        }
        
        disease_terms = {
            186200: 6088,
            
        }
        
        populate_hpo_to_gene(self.conn, hpo_dict)
        self.cursor = self.conn.cursor()
    
    def teardown(self):
        self.conn.close()
    
    def test_get_description(self):
        """docstring for test_get_description"""
        self.cursor.execute("select hpo_name from hpo_to_gene where hpo_id = '1459'")
        
        for result in self.cursor.fetone():
            assert result[0] == "1-3 toe syndactyly"