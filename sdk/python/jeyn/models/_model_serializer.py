# TODO update python version
from typing_extensions import Protocol, runtime_checkable
from typing import Any


@runtime_checkable
class ModelSerializer(Protocol):
    """
    A protocol for model serializer object.
    handles converting a machine learning model to and from bytes and is used
    to build
    """

    def to_bytes(self, model_object: Any) -> bytes:
        pass

    def from_bytes(self, model_bytes: bytes) -> Any:
        pass

