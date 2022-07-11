import operator
from typing import Any, Dict, Type, Optional, List

import backend.artefacts
from jeyn import models, errors


class ModelStore:

    serializers = Dict[Type, models.ModelSerializer]
    # mapping of class names rather than the classes themselves to be able to find the right serializer from
    # metadata of a model checkpoint
    name_serializer_mapping = Dict[str, models.ModelSerializer]

    def __init__(self):
        self.serializers = {}
        self.serializers.update(self._get_default_serializers())
        self._regenerate_name_serializer_mapping()

    def _get_default_serializers(self) -> Dict[Type, models.ModelSerializer]:
        return {}

    def _regenerate_name_serializer_mapping(self):
        self.name_serializer_mapping = {
            serializer.__class__.__name__: serializer
            for serializer in self.serializers.values()
        }

    def register_serializer(self, object_type: Type, serializer: models.ModelSerializer):
        if not isinstance(serializer, models.ModelSerializer):
            raise errors.SerializationError(
                f"the provided serializer is of type {serializer.__class__.__name__} which does not implement"
                f" the `ModelSerializer` protocol"
            )
        self.serializers[object_type] = serializer

    def get_serializer(self, model: Any) -> Optional["models.ModelSerializer"]:
        serializer = self.serializers.get(model.__class__)
        if serializer is not None:
            return serializer
        return self._get_serializer_with_inheritance(model.__class__)

    def _get_serializer_with_inheritance(self, model_type: Type) -> Optional["models.ModelSerializer"]:
        for serializable_type, serializer in self.serializers.items():
            if issubclass(model_type, serializable_type):
                return serializer
        return None

    def save_use_case(self, use_case: "models.MlUseCase"):
        try:
            remote_use_case = self.get_use_case(name=use_case.name)
            use_case.update_with_remote(remote_use_case)
        except errors.LoadingError:
            use_case_artefact = use_case.artefact
            use_case_artefact.save()

    def save_checkpoint(self, checkpoint: "models.ModelCheckpoint") -> "models.ModelCheckpoint":
        if checkpoint.model is None:
            raise errors.SaveError(
                "cannot save model checkpoint, no model object was provided. You can set it with "
                "`checkpoint.model = my_model"
            )
        try:
            self._save_model_object(checkpoint)
        except Exception as error:
            raise errors.SaveError("error when saving model object data") from error
        checkpoint.artefact.save()
        return checkpoint

    def _save_model_object(self, checkpoint: "models.ModelCheckpoint"):
        serializer = self.get_serializer(checkpoint.model)
        if serializer is None:
            raise errors.SaveError(
                f"cannot save model of type {checkpoint.model.__class__.__name__}, no serializers provided"
            )
        checkpoint.save_model_object(serializer=serializer)

    def get_use_case(self, name: str) -> "models.MlUseCase":
        use_case_artefact_list: List["models.UseCaseArtefact"] = models.UseCaseArtefact.get(use_case_name=name)
        if len(use_case_artefact_list) == 0:
            raise errors.LoadingError(f"did not found any use case matching the name {name}")
        if len(use_case_artefact_list) > 1:
            raise errors.LoadingError(f"error loading the use case, found more than one use case with the name {name}")
        return models.MlUseCase.from_artefact(use_case_artefact_list[0])

    @classmethod
    def get_use_case_from_id(cls, use_case_id):
        use_case_artefact = models.UseCaseArtefact.get_from_id(artefact_id=use_case_id)
        return models.MlUseCase.from_artefact(use_case_artefact)

    @staticmethod
    def get_latest_use_case_checkpoint(use_case: "models.MlUseCase") -> "models.ModelCheckpoint":
        if not use_case.artefact.is_saved:
            raise errors.LoadingError(f"cannot load {use_case}'s checkpoints as it is not saved in the backend yet")
        use_case_child_relations = backend.artefacts.Relationship.get_artefact_children_json(use_case.artefact)
        all_checkpoint_relations = [
            relation for relation in use_case_child_relations
            if relation["relationship_type"] == "checkpoint_use_case"
        ]
        latest_checkpoint = max(all_checkpoint_relations, key=operator.itemgetter("creation_time"))
        return models.ModelCheckpoint.from_artefact(models.CheckpointArtefact.get_from_id(latest_checkpoint["child"]))

    @staticmethod
    def load_model_from_checkpoint(
            checkpoint: "models.ModelCheckpoint", serializer: "models.ModelSerializer"
    ) -> Any:
        with open(checkpoint.path, "rb") as checkpoint_file:
            return serializer.from_bytes(checkpoint_file.read())


