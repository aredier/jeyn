from rest_framework import serializers

from . import models


class PipelineDefinitionSerializer(serializers.ModelSerializer):

    class Meta:
        models = models.PipelineDefinition
        fields = ("name")


class PipelineExecutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PipelineExecution
        fields = ("definition", "start_time", "end_time")
