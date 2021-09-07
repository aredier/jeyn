from rest_framework import viewsets

from . import models, serializers


class ArtefactViewset(viewsets.ModelViewSet):

    queryset = models.Artefact.objects.all()
    serializer_class = serializers.ArtefactSerializer


class ArtefactSchemaViewset(viewsets.ModelViewSet):

    queryset = models.ArtefactSchema.objects.all()
    serializer_class = serializers.ArtefactSchemaSerializer
