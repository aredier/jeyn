import json

from rest_framework.views import APIView, Response

import requests

from api.dummy_workflow.hello_world import dummy_workflow


class DummyView(APIView):
    def get(self, request):
        return Response(data={"message": "this is the workflow controller"})


class SubmitterView(APIView):
    _url: str = 'https://argo-server.argo:2746/api/v1/workflows/argo'

    def get(self, request):
        output = requests.get(self._url, verify=False).json()
        return Response(data={"message": output})

    def post(self, request):
        workflow_to_submit = dummy_workflow
        output = requests.post(self._url, data=json.dumps(workflow_to_submit), verify=False).json()
        return Response(data={"message": output})
