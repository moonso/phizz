import os
import pkg_resources
import phizz

resource_package = os.path.join(os.path.abspath(phizz.__name__), 'resources')

disease_to_genes_path = os.path.join(
    resource_package, 
    'ALL_SOURCES_ALL_FREQUENCIES_diseases_to_genes_to_phenotypes.txt.gz'
)
phenotype_to_genes_path = os.path.join(
    resource_package, 
    'ALL_SOURCES_ALL_FREQUENCIES_phenotype_to_genes.txt.gz'
)
schema_path = os.path.join(
    resource_package, 
    'schema.sql'
)
phizz_db = os.path.join(
    resource_package, 
    'phizz.db'
)
# disease_to_genes_file = pkg_resources.resource_string(
#     resource_package,
#     disease_to_genes_path
# )
# phenotype_to_genes_file = pkg_resources.resource_string(
#     resource_package,
#     phenotype_to_genes_path
# )
# schema_file = pkg_resources.resource_string(
#     resource_package,
#     schema_path
# )

config_file = os.path.join(resource_package, "config.ini")
