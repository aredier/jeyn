import json

from rest_framework import viewsets, views
from dapr.clients import DaprClient

from . import models, serializers


class DummyView(views.APIView):

    def get(self, request):
        return views.Response(data={"message": "this is the artefact store"})


class DummyConnectedView(views.APIView):

    def get(self, request):

        with DaprClient() as client:
            return views.Response(data={
                "message": "this is still the artefact store",
                "relate_message": str(client.invoke_method(
                    'workflow-controller',
                    '/api/dummy_view',
                    data=''
                ).data)
            })


class ArtefactClassViewset(viewsets.ModelViewSet):
    serializer_class = serializers.ArtefactClassSerializer
    queryset = models.ArtefactClass.objects.all()


class ArtefactViewset(viewsets.ModelViewSet):
    serializer_class = serializers.ArtefactSerializer
    queryset = models.Artefact.objects.all()


