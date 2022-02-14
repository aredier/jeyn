from typing import Protocol


class ModelSerializer(Protocol):
    """
    A protocol for model serializer object.
    handles converting a machine learning model to and from bytes and is used
    to build
    """