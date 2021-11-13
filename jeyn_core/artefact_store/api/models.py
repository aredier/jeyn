
import jsonschema
# django stuff
from django.db import models
from rest_framework.renderers import JSONRenderer
# dapr stuff
from dapr.clients import DaprClient

from . import exceptions, serializers, constants

# Create your models here.


class ArtefactClass(models.Model):
    """
    model of an artefact class. An artefact class is the definition of a type of artefacts to be used within the jeyn
    system.

    when creating a new artefact class, a "artefact_class_created" event will be emited
    """
    class_name: str = models.CharField(max_length=60, primary_key=True)
    schema_definition: dict = models.JSONField()

    def save(self, **kwargs) -> None:
        try:
            super().save(**kwargs)
            self._trigger_save_success_event()
        except Exception as saving_error:
            self._trigger_save_failure_event()
            raise

    def _trigger_save_success_event(self) -> None:
        with DaprClient() as client:
            client.publish_event(
                pubsub_name=constants.PUB_SUB_NAME,
                topic_name=constants.PUB_SUB_TOPICS.ARTEFACT_CLASS_CREATED.value,
                data=self._serialize_to_json(),
            )

    def _trigger_save_failure_event(self) -> None:
        with DaprClient() as client:
            client.publish_event(
                pubsub_name=constants.PUB_SUB_NAME,
                topic_name=constants.PUB_SUB_TOPICS.ARTEFACT_CLASS_CREATION_FAILED.value,
                data=self._serialize_to_json(),
            )

    def _serialize_to_json(self) -> bytes:
        serialized = serializers.ArtefactClassSerializer(self)
        return JSONRenderer().render(serialized.data)


class Artefact(models.Model):
    """
    An artefact is any kind of state produced by a jeyn workflow or a jeyn module.
    """
    artefact_class: ArtefactClass = models.ForeignKey(ArtefactClass, on_delete=models.CASCADE)
    artefact_data: dict = models.JSONField()

    def save(self, **kwargs) -> None:
        self._validate_data()
        try:
            super().save(**kwargs)
            self._trigger_save_success_event()
        except Exception as saving_error:
            self._trigger_save_failure_event()
            raise

    def _validate_data(self) -> None:
        try:
            jsonschema.validate(instance=self.artefact_data, schema=self.artefact_class.schema_definition)
        except jsonschema.exceptions.ValidationError as e:
            raise exceptions.ArtefactValidationError(self.artefact_class) from e

    def _trigger_save_success_event(self) -> None:
        with DaprClient() as client:
            client.publish_event(
                pubsub_name=constants.PUB_SUB_NAME,
                topic_name=constants.PUB_SUB_TOPICS.ARTEFACT_CREATED.value,
                data=self._serialize_to_json(),
            )

    def _trigger_save_failure_event(self) -> None:

        with DaprClient() as client:
            client.publish_event(
                pubsub_name=constants.PUB_SUB_NAME,
                topic_name=constants.PUB_SUB_TOPICS.ARTEFACT_CREATED.value,
                data=self._serialize_to_json(),
            )

    def _serialize_to_json(self) -> bytes:
        serializer = serializers.ArtefactSerializer(self)
        return JSONRenderer().render(serializer)
