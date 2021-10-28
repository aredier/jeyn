from rest_framework import serializers

from . import models


class ArtefactClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ArtefactClass
        fields = ["class_name", "schema_definition"]


class ArtefactSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Artefact
        fields = ["artefact_data", "artefact_class"]
