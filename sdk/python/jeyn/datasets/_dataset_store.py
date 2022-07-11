import operator
from typing import Optional, Type, List, Union

import backend.artefacts
from jeyn import datasets, errors, Version


class DatasetStore:
    """
    connection to the remote dataset store that allows the user to
    load formulas or batches.
    """

    def get_fromula(
            self,
            formula_cls: Type[datasets.DatasetFormula],
            name: Optional[str] = None,
            version: Optional[Union[str, Version]] = None
    ):
        version = Version.from_version_string(version) if isinstance(version,str) else version
        formula_artefacts = datasets.DatasetFormulaArtefact.get(
            formula_name=name, version=version.to_json() if version is not None else None
        )
        if len(formula_artefacts) == 0:
            return None
        if len(formula_artefacts) > 1:
            return formula_cls.from_artefact(
                sorted(formula_artefacts, key=operator.attrgetter("version"))[-1]
            )
        return formula_cls.from_artefact(formula_artefacts[0])

    def _get_formula_batch_relation_jsons(self, formula):
        if not formula.artefact.is_saved:
            raise errors.LoadingError(
                f"cannot load {formula.formula_name}'s batches since it does not seem saved yet."
            )
        formula_child_relations = backend.artefacts.Relationship.get_artefact_children_json(formula.artefact)
        return [
            relation for relation in formula_child_relations
            if relation["relationship_type"] == "batch_formula"
        ]

    def get_formula_batches(self, formula: datasets.DatasetFormula) -> List[datasets.DatasetBatch]:
        return [
            formula.batch_type.from_artefact(formula=formula, artefact=datasets.BatchArtefact.get_from_id(batch["child"]))
            for batch in self._get_formula_batch_relation_jsons(formula)
        ]

    def get_latest_formula_batch(self, formula: datasets.DatasetFormula) -> datasets.DatasetBatch:
        batches = self.get_formula_batches(formula)
        if len(batches) == 0:
            return None

        latest_batch = max(batches, key=operator.attrgetter("batch_epoch"))
        return latest_batch

    def save_batch(self, batch: datasets.DatasetBatch):
        batch_artefact = batch.artefact
        batch_artefact.save()

    @classmethod
    def get_batch_from_id(cls, batch_id: int) -> "datasets.batches.GenericBatch":
        batch_artefact = datasets.BatchArtefact.get_from_id(batch_id)
        return datasets.batches.GenericBatch.from_artefact(formula=None, artefact=batch_artefact)


