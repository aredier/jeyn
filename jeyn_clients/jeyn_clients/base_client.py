import requests


class Client:

    def __init__(self, service: str, port=3500):
        self.service_name = service
        self.dapr_port = port

    def _format_url(self, method: str) -> str:
        return f"http://localhost:{self.dapr_port}/v1.0/invoke/{self.service_name}/method/{method}"

    def _process_response(self, response: requests.Response):
        response.raise_for_status()
        return response.json()

    def post(self, method, json):
        request_url = self._format_url(method)
        response = requests.post(request_url, json=json)
        return self._process_response(response)

    def get(self, method):
        request_url = self._format_url(method)
        response = requests.get(request_url)
        return self._process_response(response)

    def put(self, method, json):
        request_url = self._format_url(method)
        response = requests.put(request_url, json=json)
        return self._process_response(response)

    def patch(self, method, json):
        request_url = self._format_url(method)
        response = requests.post(request_url, json=json)
        return self._process_response(response)
