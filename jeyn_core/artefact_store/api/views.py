import json

from rest_framework.views import APIView, Response
from dapr.clients import DaprClient


class DummyView(APIView):

    def get(self, request):
        return Response(data={"message": "this is the artefact store"})


class DummyConnectedView(APIView):

    def get(self, request):

        with DaprClient() as client:
            return Response(data={
                "message": "this is still the artefact store",
                "relate_message": str(client.invoke_method(
                    'workflow-controller',
                    '/api/dummy_view',
                    data=''
                ).data)
            })

