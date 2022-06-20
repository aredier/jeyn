from typing import Optional

import attr

import typing_utils
from ... import errors, datasets


@attr.define
class GenericBatch(datasets.DatasetBatch):
    """
    batch class when a specific batch is of unknown class so it can still be used to retrieve certain metadata.
    """

    batch_kwargs: typing_utils.JSON
    formula_artefact: "datasets.DatasetFormulaArtefact"

    @property
    def output_catalog(self) -> "catalogs.DataCatalog":
        return self.formula_artefact.output_catalog

    @classmethod
    def from_json(cls, formula: Optional["datasets.DatasetFormula"],
                  batch_kwargs: typing_utils.JSON) -> "datasets.DatasetBatch":
        if formula is not None:
            raise errors.LoadingError(
                "if formula is known use the formula's batch type rather than the generic batch type"
            )
        formula_artefact = datasets.DatasetFormulaArtefact.from_artefact_json(batch_kwargs.pop("formula_artefact_json"))
        return cls(batch_kwargs=batch_kwargs, formula=None, formula_artefact=formula_artefact)

    @classmethod
    def from_artefact(
            cls, formula: Optional["datasets.DatasetFormula"], artefact: "datasets.BatchArtefact"
    ) -> "DatasetBatch":
        return cls(
            batch_kwargs=artefact.batch_kwargs,
            formula=None,
            formula_artefact=artefact.formula
        )

    def get_batch_kwargs(self) -> typing_utils.JSON:
        return self.batch_kwargs
