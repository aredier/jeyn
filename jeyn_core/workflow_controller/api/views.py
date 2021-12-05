import json
import os

from dapr.clients import DaprClient
from rest_framework.views import APIView, Response

import requests

from api.dummy_workflow.hello_world import dummy_workflow


class DaprConfigurationView(APIView):
    def get(self, request):
        subscriptions = [
            {
                "pubsubname": "pubsub",
                "topic": "topic_name",
                "route": "api/topic_name"
            }
        ]
        return Response(data=json.dumps(subscriptions))


class SubmitterView(APIView):
    _url: str = 'https://argo-server.argo:2746/api/v1/workflows/argo'

    def get(self, request):
        output = requests.get(self._url, verify=False).json()
        return Response(data={"message": output})

    def post(self, request):
        workflow_to_submit = dummy_workflow
        output = requests.post(self._url, data=json.dumps(workflow_to_submit), verify=False).json()
        return Response(data={"message": output})


class SubscriberView(APIView):
    def post(self, request):
        status = {
            "status": "SUCCESS"
        }
        return Response(data=json.dumps(status))

