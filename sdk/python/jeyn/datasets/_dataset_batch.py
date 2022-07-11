import abc
import datetime as dt
from typing import Optional, List
from uuid import UUID, uuid4

import attr

import catalogs
import typing_utils
from .. import datasets, backend, errors


class BatchArtefact(backend.artefacts.Artefact):

    class Meta:
        artefact_type_name = "dataset_batch"
        schema = {
            "type": "object",
            "properties": {
                "batch_epoch": {
                    "type": "number",
                    "description": "epoch of the dataset batch"
                },
                "batch_kwargs": {
                    "type": "object",
                    "description": "extra args for batch initialisation"
                }
            }
        }

    def __init__(self,
                 formula_artefact: "datasets.DatasetFormulaArtefact",
                 batch_kwargs: typing_utils.JSON,
                 batch_epoch: Optional[int] = None,
                 ):
        self.formula = formula_artefact
        self.batch_epoch = batch_epoch or int(dt.datetime.utcnow().timestamp())
        self.batch_kwargs = batch_kwargs

    def artefact_json(self) -> typing_utils.JSON:
        return {"batch_epoch": self.batch_epoch, "batch_kwargs": self.batch_kwargs}

    def get_relationships(self) -> List["artefacts.Relationship"]:
        return [
            backend.artefacts.Relationship(parent=self.formula, child=self, relationship_type="batch_formula")
        ]

    @classmethod
    def from_artefact_json(cls, artefact_json: typing_utils.JSON) -> "Artefact":
        formula_id = cls.extract_artefact_from_singleton_relationship(
            relationship_jsons=artefact_json["parents"], relationship_type="batch_formula"
        )
        formula_artefact = datasets.DatasetFormulaArtefact.get_from_id(formula_id)
        return cls(
            formula_artefact=formula_artefact,
            batch_epoch=artefact_json["artefact_data"]["batch_epoch"],
            batch_kwargs=artefact_json["artefact_data"]["batch_kwargs"],
        )


@attr.define
class DatasetBatch(abc.ABC):
    """
    a dataset batch is a specific instance of a dataset formula.
    Whereas a formula is meant to allow new data to be queried and to
    version the way a dataset is generated for downstream users, dataset batches are built
    for reproducibility. A new instance of the same batch (reloaded from the store) should
    yield the same data.
    """

    formula: Optional["datasets.DatasetFormula"]
    # _uuid: UUID = attr.field(init=False, factory=uuid4)
    _artefact: Optional[BatchArtefact] = attr.field(init=False, default=None)

    @property
    def artefact(self) -> BatchArtefact:
        if self._artefact is None:
            self._artefact = self._to_artefact()
        return self._artefact

    @property
    def output_catalog(self) -> "catalogs.DataCatalog":
        if self.formula is None:
            raise errors.DataConsistencyError("cannot get output catalog since dataset formula is None")
        return self.formula.output_catalog

    @artefact.setter
    def artefact(self, artefact: BatchArtefact):
        self._artefact = artefact

    @property
    def batch_epoch(self) -> int:
        return self.artefact.batch_epoch

    @property
    def date_time(self) -> dt.datetime:
        return dt.datetime.utcfromtimestamp(self.batch_epoch)

    @classmethod
    @abc.abstractmethod
    def from_json(
            cls, formula: Optional["datasets.DatasetFormula"], batch_kwargs: typing_utils.JSON
    ) -> "datasets.DatasetBatch":
        pass

    @abc.abstractmethod
    def get_batch_kwargs(self) -> typing_utils.JSON:
        pass

    @classmethod
    def from_artefact(
            cls, formula: Optional["datasets.DatasetFormula"], artefact: "datasets.BatchArtefact"
    ) -> "DatasetBatch":
        return cls.from_json(formula=formula, batch_kwargs=artefact.batch_kwargs)

    def validate_schema(self):
        self.formula.schema.validate(self)

    def _to_artefact(self) -> "BatchArtefact":
        return BatchArtefact(
            formula_artefact=self.formula.artefact,
            batch_kwargs=self.get_batch_kwargs()
        )
