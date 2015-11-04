from pkg_resources import get_distribution

__version__ = get_distribution("phizz").version

from phizz.utils import (query_hpo, query_disease)