import abc
from typing import Any, Type

from jeyn import catalogs


class CatalogValidator(abc.ABC):
    """
    a catalog validator's job is to validate an actual piece
    of data that is specific to an ml stack (for instance a `pd.DataFrame` instance).
    It will check the data for this specific implementation against the abstract definition of
    a Jeyn catalog.

    """

    @abc.abstractmethod
    def validate(self, data_piece: Any, data_catalog: Type["catalogs.DataCatalog"]) -> None:
        pass
