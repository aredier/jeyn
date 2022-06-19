from typing import Type, Dict, Optional

from .. import catalogs, typing_utils, errors


class DataCatalog:
    """
    a data catlog is the formal definition of an interface between two jeyn ml
    components. Catalogs can then be used to:
    - validate a piece of data is valid for a given interface.
    - two interfaces can work together.

    a catalog is composed of features that are defined in the class definition:

    >>> SimpleDatasetCatalog(DataCatalog):
    ...
    ...     X = Feature(shape=(-1, 45))
    ...     y = Feature(shape=(-1, 2))
    """

    _features: Dict[str, "catalogs.Feature"]

    def __init_subclass__(cls, **kwargs):
        cls._features = {}
        for class_attribute_name, class_attribute in cls.__dict__.items():
            if isinstance(class_attribute, catalogs.Feature):
                cls._add_feature(class_attribute_name, class_attribute)

    def __init__(self, features: Optional[Dict[str, "catalogs.Feature"]] = None):
        if self.__class__ is DataCatalog:
            if features is None:
                raise errors.DataValidationError(
                    "when instantiating a DataCatalog instance you need to explicitly define features."
                )
            self._features = {}
            for class_attribute_name, class_attribute in features.items():
                if isinstance(class_attribute, catalogs.Feature):
                    self._add_feature_to_instance(class_attribute_name, class_attribute)

    def _add_feature_to_instance(self, feature_name: str, feature: "catalogs.Feature"):
        if feature.name is None:
            feature.name = feature_name
        if feature.name in self._features:
            raise errors.DataValidationError(f"duplicate features with the name {feature.name}")
        self._features[feature.name] = feature

    @classmethod
    def _add_feature(cls, feature_name: str, feature: "catalogs.Feature"):
        if feature.name is None:
            feature.name = feature_name
        if feature.name in cls._features:
            raise errors.DataValidationError(f"duplicate features with the name {feature.name}")
        cls._features[feature.name] = feature

    def includes(cls, other: "DataCatalog") -> bool:
        """
        check wether another catalog is included in this catalog.

        >>> TrainingCatalog(DataCatalog):
        ...
        ...     X = DenseFeature(shape=(-1, 45))
        ...     y = DenseFeature(shape=(-1, 2))
        >>>
        >>> PredictCatalog(DataCatalog):
        ...
        ...     X = DenseFeature(shape=(-1, 45))
        >>>
        >>> TrainingCatalog.includes(PredictCatalog)
        True
        >>> PredictCatalog.includes(TrainingCatalog):
        False

        Args:
            other: the other catalog type to check compatibility with

        Returns: True if `other` is included `False` otherwise.
        """
        return True

    @staticmethod
    def get_catalog_json_schema() -> typing_utils.JSON:
        return {
            "type": "object",
            "properties": {
                "features": {
                    "type": "array",
                    "items": catalogs.Feature.get_feature_json_schema()
                }
            },
            "required": ["features"]
        }

    def to_json(self) -> typing_utils.JSON:
        return {
            "features": [feature.to_json() for feature_name, feature in self._features.items()]
        }

    @staticmethod
    def from_json(catalog_json: typing_utils.JSON) -> "DataCatalog":
        features = {}
        for feature_json in catalog_json["features"]:
            feature = catalogs.Feature.from_json(feature_json)
            features[feature.name] = feature
        return DataCatalog(features=features)
