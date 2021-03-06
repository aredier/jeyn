from typing import List, Optional, Any

import attr

from .. import backend, errors, typing_utils, catalogs, models, datasets


class UseCaseArtefact(backend.artefacts.Artefact):
    class Meta:
        artefact_type_name = "ml_use_case"
        schema = {
            "type": "object",
            "properties": {
                "use_case_name": {
                    "type": "string",
                    "description": "name of the use case"
                },
                "use_case_description": {
                    "type": "string",
                    "description": "description of the use case"
                }
            }
        }

    def __init__(self, use_case_name: str, use_case_description):
        self.use_case_name = use_case_name
        self.use_case_description = use_case_description

    def artefact_json(self) -> typing_utils.JSON:
        return {"use_case_name": self.use_case_name, "use_case_description": self.use_case_description}

    @classmethod
    def from_artefact_json(cls, artefact_json: typing_utils.JSON) -> "UseCaseArtefact":
        artefact_data = artefact_json["artefact_data"]
        return cls(
            use_case_name=artefact_data["use_case_name"],
            use_case_description=artefact_data["use_case_description"]
        )

    def get_relationships(self) -> List["backend.artefacts.Relationship"]:
        return []


@attr.define
class MlUseCase:
    name: str
    description: str
    _artefact: Optional["UseCaseArtefact"] = attr.field(init=False, default=None)

    @property
    def artefact(self) -> "UseCaseArtefact":
        if self._artefact is None:
            self._artefact = self._to_artefact()
        return self._artefact

    @artefact.setter
    def artefact(self, value):
        if self._artefact is not None:
            raise errors.InternalJeynError(
                "artefact is being set serveral times, only set the use_case's artefact once."
            )
        self._artefact = value

    @classmethod
    def from_artefact(cls, artefact: UseCaseArtefact) -> "MlUseCase":
        use_case = MlUseCase(
            name=artefact.use_case_name,
            description=artefact.use_case_description
        )
        use_case.artefact = artefact
        return use_case

    def update_with_remote(self, other: "MlUseCase"):
        self._check_compatibility(other)
        self._artefact = other.artefact

    def update_major(
            self,
            dataset: datasets.DatasetBatch,
            model: Any,
            input_catalog: Optional["catalogs.DataCatalog"] = None,
            output_catalog: Optional["catalogs.DataCatalog"] = None,
    ) -> "models.ModelCheckpoint":
        latest_checkpoint = models.ModelCheckpoint.get_latest_use_case_checkpoint(self)
        output_catalog = output_catalog or latest_checkpoint.output_catalog
        input_catalog = input_catalog or latest_checkpoint.input_catalog
        if not output_catalog.includes(latest_checkpoint):
            raise errors.ChangedCatalogError(
                "the new output catalog does not contain all the outputs from the previous version, use a major"
                "version update if you want to remove some outputs"
            )
        return models.ModelCheckpoint(
            dataset_batch=dataset,
            use_case=self,
            version=latest_checkpoint.version.update_major(),
            model=model,
            output_catalog=output_catalog,
            input_catalog=input_catalog,
        )

    def update_minor(
            self, dataset: datasets.DatasetBatch, model: Any, output_catalog: Optional["catalogs.DataCatalog"] = None
    ) -> "models.ModelCheckpoint":
        latest_checkpoint = models.ModelCheckpoint.get_latest_use_case_checkpoint(self)
        output_catalog = output_catalog or latest_checkpoint.output_catalog
        if not output_catalog.includes(latest_checkpoint):
            raise errors.ChangedCatalogError(
                "the new output catalog does not contain all the outputs from the previous version, use a major"
                "version update if you want to remove some outputs"
            )
        return models.ModelCheckpoint(
            dataset_batch=dataset,
            use_case=self,
            version=latest_checkpoint.version.update_major(),
            model=model,
            output_catalog=output_catalog,
            input_catalog=latest_checkpoint.input_catalog,
        )

    def update_patch(self, dataset: datasets.DatasetBatch, model: Any) -> "models.ModelCheckpoint":
        latest_checkpoint = models.ModelStore.get_latest_use_case_checkpoint(self)
        return models.ModelCheckpoint(
            dataset_batch=dataset,
            use_case=self,
            version=latest_checkpoint.version.update_major(),
            model=model,
            output_catalog=latest_checkpoint.output_catalog,
            input_catalog=latest_checkpoint.input_catalog,
        )

    def _to_artefact(self) -> "UseCaseArtefact":
        return UseCaseArtefact(
            use_case_name=self.name, use_case_description=self.description
        )

    def _check_compatibility(self, other: "MlUseCase"):
        # TODO implement
        pass
