import abc
import enum
from typing import List, Optional

import attr

import typing_utils
from jeyn import errors


class Dtypes(enum.Enum):
    INT32 = "int32"
    INT64 = "int64"
    FLOAT32 = "float32"
    FLOAT64 = "float64"
    STRING = "string"


@attr.define
class Feature(abc.ABC):
    """
    a feature is the abstract representation of an array/tensor that can
    be used in various machine learning components. Features are not linked to
    a specific mnl stack (np, tf, torch, ...) and does not provide concretions to
    hold specific data. They simply describe them.
    """

    dtype: Dtypes = attr.field()
    shape: List[int] = attr.field()
    name: Optional[str] = attr.field(default=None)

    @shape.validator
    def _validate_shape(self, attribute, value):
        for axis_size in value:
            if axis_size < -1:
                raise errors.DataValidationError(
                    f"cannot have a shape with dimension of size {axis_size} (full shape: {value}"
                )

    @staticmethod
    def get_feature_json_schema():
        return {
            "type": "object",
            "properties": {
                "dtype": {"type": "string"},
                "shape": {"type": "array", "items": {"type": "number"}},
                "name": {"type": "string"}
            },
            "required": [
                "dtype", "shape", "name"
            ]
        }

    def to_json(self) -> typing_utils.JSON:
        return {
            "dtype": self.dtype.value,
            "shape": self.shape,
            "name": self.name
        }

    @classmethod
    def from_json(cls, feature_json: typing_utils.JSON) -> "Feature":
        return cls(
            dtype=Dtypes(feature_json["dtype"]),
            shape = feature_json["shape"],
            name = feature_json["name"]
        )
