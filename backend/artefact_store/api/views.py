from rest_framework import viewsets, request, views, response

from . import serializers, models


class ArtefactTypeViewset(viewsets.ModelViewSet):
    serializer_class = serializers.ArtefactTypeSerializer
    queryset = models.ArtefactType.objects.all()


class ArtefactViewset(viewsets.ModelViewSet):
    serializer_class = serializers.ArtefactSerializer
    queryset = models.Artefact.objects.all()


class ArtefactQueryView(views.APIView):

    def get(self, request: request.Request):
        objects = models.Artefact.objects.filter(**{key: value for key, value in request.query_params.items()})
        artefacts = objects.all()
        serializer = serializers.ArtefactSerializer(artefacts, many=True)
        return response.Response(serializer.data)


class RelationshipViewset(viewsets.ModelViewSet):
    serializer_class = serializers.RelationShipSerializer
    queryset = models.RelationShip.objects.all()