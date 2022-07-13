from rest_framework import viewsets

from . import serializers, models


class PipelineDefinitionViewset(viewsets.ModelViewSet):
    serializer_class = serializers.PipelineDefinitionSerializer
    queryset = models.PipelineDefinition.objects.all()


class PipelineExecutionViewset(viewsets.ModelViewSet):
    serializer_class = serializers.PipelineExecutionSerializer
    queryset = models.PipelineExecution.objects.all()