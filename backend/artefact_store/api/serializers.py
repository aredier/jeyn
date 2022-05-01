from rest_framework import serializers

from . import models


class ArtefactTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ArtefactType
        fields = ["type_name", "schema"]


class RelationShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RelationShip
        fields = ("id", "parent", "child", "relationship_type")
        read_only_fields = ("creation_time",)


class ParentRelationShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RelationShip
        fields = [
            "id", "child", "relationship_type", "creation_time"
        ]


class ChildRelationShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RelationShip
        fields = [
            "id", "parent", "relationship_type", "creation_time"
        ]


class ArtefactSerializer(serializers.ModelSerializer):
    children = ParentRelationShipSerializer(many=True, read_only=True)
    parents = ChildRelationShipSerializer(many=True, read_only=True)

    class Meta:
        model = models.Artefact
        fields = [
            "id",
            "artefact_type_reference",
            "artefact_data",
            "children",
            "parents"
        ]
