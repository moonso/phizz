try:
    import cPickle as pickle
except:
    import pickle

import pkg_resources
import phizz

resource_package = phizz.__name__

gene_db_file = pkg_resources.resource_filename(
    resource_package,
    "resources/genes.db"
)

with open(gene_db_file, 'rb') as f:
    GENE_DB = pickle.load(f)

from .parse_resource import (parse_phenotypes, parse_diseases, parse_genes)
from .queries import (query_hpo, query_disease, query_gene, query_gene_symbol)
from .build_gene_trees import build_gene_trees

