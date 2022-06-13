"""
the catalogs module provides a way for users to create or infer different data interfaces between
jeyn components (datasets, models, ...). This cna allow jeyn to check for interface consistency and
raise potential problems early on.
"""

from ._data_catalog import DataCatalog
from ._feature import Feature, Dtypes
from ._validator import CatalogValidator

__all__ = [
    "DataCatalog", "Feature", "Dtypes", "CatalogValidator"

]
