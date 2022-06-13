import abc

from typing import Optional, List, Dict, Any, Type

import attr

import jeyn
import typing_utils
from jeyn import Version, datasets, backend, catalogs


class DatasetFormulaArtefact(backend.artefacts.Artefact):
    class Meta:
        artefact_type_name = "dataset_formula"
        schema = {
            "type": "object",
            "properties": {
                "formula_name": {
                    "type": "string",
                    "description": "name of the formula"
                },
                "formula_type": {
                    "type": "string",
                    "description": "precise type of formula to use"
                },
                "output_catalog": catalogs.DataCatalog.get_catalog_json_schema(),
                "formula_kwargs": {
                    "type": "object",
                    "description": "more arguments when initializing"
                }
            }
        }

    def __init__(
            self, name: str, formula_type: str, formula_kwargs: Dict[str, Any], output_catalog: "catalogs.DataCatalog"
    ):
        self.name = name
        self.formula_type = formula_type
        self.formula_kwargs = formula_kwargs
        self.output_catalog = output_catalog

    def artefact_json(self) -> typing_utils.JSON:
        return {
            "formula_name": self.name,
            "formula_type": self.formula_type,
            "output_catalog": self.output_catalog.to_json(),
            "formula_kwargs": self.formula_kwargs
        }

    @classmethod
    def from_artefact_json(cls, artefact_json: typing_utils.JSON) -> " backend.artefacts.Artefact":
        return cls(
            name=artefact_json["artefact_data"]["formula_name"],
            formula_type=artefact_json["artefact_data"]["formula_type"],
            formula_kwargs=artefact_json["artefact_data"]["formula_kwargs"],
            output_catalog=catalogs.DataCatalog.from_json(artefact_json["artefact_data"]["output_catalog"])
        )

    def get_relationships(self) -> List["backend.artefacts.Relationship"]:
        return []


@attr.define
class DatasetFormula(abc.ABC):
    """
    a dataset formulas are a dataset's recipe. Whereas most academic papers are
    based on static datasets for reproducibility purposes, a lot of real world examples
    are dynamic and building a production ML pipeline means being able to get new batches of
    the same dataset.

    In practice DatasetFormulas allow you to create new batches/instances of a dataset to
    fine-tune or train your models on.
    """

    formula_name: str
    version: Optional[Version]
    output_catalog: "jeyn.catalogs.DataCatalog"
    _artefact: "DatasetFormulaArtefact" = attr.field(default=None, init=False)

    @property
    def artefact(self):
        if self._artefact is None:
            self._artefact = self.to_artefact()
        return self._artefact

    @property
    def formula_kwargs(self):
        return {}

    @property
    @abc.abstractmethod
    def batch_type(self) -> Type["datasets.DatasetBatch"]:
        pass

    @abc.abstractmethod
    def get_new_batch(self) -> datasets.DatasetBatch:
        pass

    def to_artefact(self) -> "DatasetFormulaArtefact":
        return DatasetFormulaArtefact(
            name=self.formula_name,
            formula_type=self.__class__.__name__,
            formula_kwargs=self.formula_kwargs,
            output_catalog=self.output_catalog
        )

    @classmethod
    def from_artefact(cls, formula_artefact: "DatasetFormulaArtefact") -> "DatasetFormula":
        artefact_object = cls(
            formula_name=formula_artefact.name,
            version=None,
            output_catalog=formula_artefact.output_catalog,
            **formula_artefact.formula_kwargs
        )
        artefact_object._artefact = formula_artefact
        return artefact_object

    def save(self):
        self.artefact.save()
