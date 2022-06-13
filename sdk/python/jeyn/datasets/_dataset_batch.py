import abc
import datetime as dt
from typing import Optional, List
from uuid import UUID, uuid4

import attr

import typing_utils
from jeyn import datasets, backend


class BatchArtefact(backend.artefacts.Artefact):

    class Meta:
        artefact_type_name = "dataset_batch"
        schema = {
            "type": "object",
            "properties": {
                "batch_epoch": {
                    "type": "int",
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


@attr.define
class DatasetBatch(abc.ABC):
    """
    a dataset batch is a specific instance of a dataset formula.
    Whereas a formula is meant to allow new data to be queried and to
    version the way a dataset is generated for downstream users, dataset batches are built
    for reproducibility. A new instance of the same batch (reloaded from the store) should
    yield the same data.
    """

    formula: "datasets.DatasetFormula"
    _uuid: UUID = attr.field(init=False, factory=uuid4)

    def validate_schema(self):
        self.formula.schema.validate(self)

    @abc.abstractmethod
    def get_batch_kwargs(self) -> typing_utils.JSON:
        pass

    @classmethod
    @abc.abstractmethod
    def from_json(cls, batch_kwargs: typing_utils.JSON) -> "datasets.DatasetBatch":
        pass
