import os
import uuid
from typing import Any, Optional, List, Type
from uuid import uuid4, UUID

from attr import define, field

import typing_utils
from .. import Version, datasets, models, errors, backend, catalogs


class CheckpointArtefact(backend.artefacts.Artefact):
    unique_id: uuid.UUID
    version: Version
    model_path: str
    parent: Optional["ModelCheckpoint"]
    use_case: "models.MlUseCase"
    training_batch: datasets.DatasetBatch
    output_catalog: "catalogs.DataCatalog"
    input_catalog: "catalogs.DataCatalog"

    class Meta:
        artefact_type_name = "model_checkpoint"
        schema = {
            "type": "object",
            "properties": {
                "uuid": {
                    "type": "string",
                    "description": "the uuid of the checkpoint"
                },
                "version": {
                    "type": "string",
                    "description": "the version of the checkpoint"
                },
                "model_bytes_path": {
                    "type": "string",
                    "description": "the path of the model bytes"
                },
                "output_catalog": catalogs.DataCatalog.get_catalog_json_schema(),
                "input_catalog": catalogs.DataCatalog.get_catalog_json_schema(),
            },
            "required": [
                "model_bytes_path",
                "version",
                "uuid",
                "output_catalog",
                "input_catalog"
            ]
        }

    def __init__(
            self,
            unique_id: uuid.UUID,
            version: Version,
            model_path: str,
            output_catalog: "catalogs.DataCatalog",
            input_catalog: "catalogs.DataCatalog",
            parent: Optional["ModelCheckpoint"],
            use_case: "models.MlUseCase",
            training_batch: datasets.DatasetBatch
    ):
        self.unique_id = unique_id
        self.version = version
        self.model_path = model_path
        self.parent = parent
        self.training_batch = training_batch
        self.use_case = use_case
        self.output_catalog = output_catalog
        self.input_catalog = input_catalog
        super().__init__()

    def artefact_json(self) -> typing_utils.JSON:
        return {
            "uuid": str(self.unique_id),
            "version": self.version.to_version_string(),
            "model_bytes_path": self.model_path,
            "output_catalog": self.output_catalog.to_json(),
            "input_catalog": self.input_catalog.to_json()
        }

    @classmethod
    def from_artefact_json(cls, artefact_json: typing_utils.JSON) -> "CheckpointArtefact":
        # TODO batch relationship
        return cls(
            unique_id=uuid.UUID(artefact_json["artefact_data"]["uuid"]),
            version=Version.from_version_string(artefact_json["artefact_data"]["version"]),
            model_path=artefact_json["artefact_data"]["model_bytes_path"],
            parent=None,
            use_case=cls._reload_use_case_from_relationship_json(artefact_json["parents"]),
            training_batch=cls._reload_dataset_batch_from_relationship_json(artefact_json["parents"]),
            output_catalog=catalogs.DataCatalog.from_json(artefact_json["artefact_data"]["output_catalog"]),
            input_catalog=catalogs.DataCatalog.from_json(artefact_json["artefact_data"]["input_catalog"])
        )

    @classmethod
    def _reload_dataset_batch_from_relationship_json(
            cls, checkpoint_relationship_jsons: List[typing_utils.JSON]
    ) -> "datasets.DatasetBatch":
        batch_id = cls.extract_artefact_from_singleton_relationship(checkpoint_relationship_jsons, "checkpoint_dataset_batch")
        return datasets.DatasetStore.get_batch_from_id(batch_id)

    @classmethod
    def _reload_use_case_from_relationship_json(cls, checkpoint_relationship_jsons: List[typing_utils.JSON]) -> "models.MlUseCase":
        use_case_id = cls.extract_artefact_from_singleton_relationship(checkpoint_relationship_jsons, "checkpoint_use_case")
        return models.ModelStore.get_use_case_from_id(use_case_id=use_case_id)

    def get_relationships(self):
        return [
            backend.artefacts.Relationship(
                relationship_type="checkpoint_use_case",
                parent=self.use_case.artefact,
                child=self
            ),
            backend.artefacts.Relationship(
                relationship_type="checkpoint_dataset_batch",
                parent=self.training_batch.artefact,
                child=self
            )
        ]

    def to_checkpoint(self, serializer: "models.ModelSerializer") -> "ModelCheckpoint":
        with open(self.model_path, "rb") as model_bytes:
            model = serializer.from_bytes(model_bytes=model_bytes.read())
        # TODO handle the uuid thing
        return ModelCheckpoint(
            dataset_batch=self.training_batch,
            use_case=self.use_case,
            version=Version.from_version_string(self.version),
            model=model
        )


@define
class ModelCheckpoint:
    """
    A model checkpoint is the metadata of saved model.
    """

    # TODO save the batch relationship
    # TODO input_catalog inside the artefacts
    dataset_batch: datasets.DatasetBatch
    use_case: "models.MLUseCase"
    version: Version
    model: Optional[Any]
    output_catalog: catalogs.DataCatalog
    input_catalog: catalogs.DataCatalog

    parent_checkpoint: Optional["ModelCheckpoint"] = None
    _uuid: UUID = field(init=False, factory=uuid4)
    _artefact: Optional[CheckpointArtefact] = field(init=False, default=None)

    def __attrs_post_init__(self):
        if not self.input_catalog.includes(self.dataset_batch.output_catalog):
            # TODO better error
            raise errors.DataValidationError("model inputs are not included in the dataset's output.")

    @classmethod
    def from_artefact(cls, checkpoint_artefact: CheckpointArtefact) -> "ModelCheckpoint":
        # TODO add the dataset batch
        checkpoint = cls(
            dataset_batch=checkpoint_artefact.training_batch,
            use_case=checkpoint_artefact.use_case,
            version=checkpoint_artefact.version,
            model=None,
            parent_checkpoint=None,
            output_catalog=checkpoint_artefact.output_catalog,
            input_catalog=checkpoint_artefact.input_catalog
        )
        checkpoint.artefact = checkpoint_artefact
        return checkpoint

    @property
    def artefact(self) -> CheckpointArtefact:
        if self._artefact is None:
            self._artefact = self._to_artefact()
        return self._artefact

    @artefact.setter
    def artefact(self, artefact: CheckpointArtefact):
        self._uuid = artefact.unique_id
        self._artefact = artefact

    def _to_artefact(self) -> CheckpointArtefact:
        return CheckpointArtefact(
            unique_id=self.uuid,
            version=self.version,
            model_path=self.path,
            parent=self.parent_checkpoint,
            training_batch=self.dataset_batch,
            use_case=self.use_case,
            output_catalog=self.output_catalog,
            input_catalog=self.input_catalog
        )

    @property
    def loaded(self) -> bool:
        return self.model is not None

    @property
    def uuid(self) -> UUID:
        return self._uuid

    @property
    def path(self) -> str:
        return f"/tmp/jeyn_models/{self.use_case.name}/{self.uuid}"

    def save_model_object(self, serializer: models.ModelSerializer):
        model_bytes = serializer.to_bytes(self.model)
        # TODO use dapr blob storage api.
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "wb") as model_file:
            model_file.write(model_bytes)
