from typing_extensions import Protocol, runtime_checkable

from jeyn import core


@runtime_checkable
class ArtefactConvertibleObject(Protocol):
    """abstract class for all object that can be converted to artefacts"""

    def convert_to_artefact(self) -> "core.Artefact":
        """converts this object to an artefact"""
        pass
