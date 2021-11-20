"""
module that handles the connection to jeyn core services (artefacts and workflows)
"""

from jeyn.core._artefact_convertible_object import ArtefactConvertibleObject
from jeyn.core._artefact import Artefact
from jeyn.core._artefact_schema import ArtefactSchema
from jeyn.core._artefact_factory import ArtefactFactory

__all__ = [
    "Artefact",
    "ArtefactSchema",
    "ArtefactFactory",
    "ArtefactConvertibleObject"
]
