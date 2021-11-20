import pytest
from typing import Type

from jeyn.core import ArtefactConvertibleObject, ArtefactFactory, Artefact
from jeyn.errors import DataConversionError


@pytest.fixture
def fake_artefact_convertible_cls(fake_artefact) -> Type[ArtefactConvertibleObject]:
    class FakeArtefactConvertible:
        def __init__(self):
            self._artefact = fake_artefact

        def convert_to_artefact(self) -> "core.Artefact":
            return self._artefact
    return FakeArtefactConvertible


def test_isinstance(fake_artefact_convertible_cls):
    assert isinstance(fake_artefact_convertible_cls(), ArtefactConvertibleObject)


def test_conversion_normal(fake_artefact_convertible_cls):
    assert isinstance(
        ArtefactFactory.convert_object_to_artefact(fake_artefact_convertible_cls()),
        Artefact
    )


def test_conversion_error():
    class FakeNonConvertible:
        pass
    with pytest.raises(DataConversionError):
        ArtefactFactory.convert_object_to_artefact(FakeNonConvertible())
