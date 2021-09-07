from rest_framework import serializers

from . import models


class ArtefactSchemaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ArtefactSchema
        fields = [
            "id", "name", "artefacts"
        ]


class ArtefactSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Artefact
        fields = [
            "id", "schema", "value"
        ]
