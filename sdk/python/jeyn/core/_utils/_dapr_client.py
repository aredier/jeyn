from typing import Optional, Any, Union

import requests
from dapr import clients


# this class is mainly needed because the stock dapr client does not pass over the
# http status codes of the requests which makes true rest logic hard to achieve

class DaprClient:
    """
    class to have a better tailored dapr client within jeyn
    The idea is to recode some apis if needed but  here is how it should be coded:
    * whenever possible use stock client
    * if possible reproduce as close to possible the OG API
    * add specialized methods for jeyn specific use cases.
    """
    _dapr_lib_client: Optional[clients.DaprClient]

    def __init__(self):
        self._dapr_lib_client = None

    def __enter__(self) -> clients.DaprClient:
        self._dapr_lib_client = clients.DaprClient().__enter__()
        return self

    def __exit__(self, *args, **kwargs) -> None:
        self._dapr_lib_client.__exit__(*args, **kwargs)
        self._dapr_lib_client = None

    @staticmethod
    def invoke_method(
            app_id: str,
            method_name: str,
            data: Any = None,
            http_verb: str = "GET"
    ) -> requests.Response:
        """
        invokes a method (route) in a given app in the jeyn system using the http protocol.

        Args:
            app_id: the id (usually the name of the app in snakecase) of the specific
                    jeyn app to contact
            method_name: the name of the method to call (this is the the route of
                         the app and not the http verb)
            data: the json serializable data to use in the request body if needed.
            http_verb: the verb to use when calling the specific dapr client

        Returns: the requests.Response object corresponding to the call.

        """

        return requests.request(
            method=http_verb,
            url=f"http://localhost:3500/v1.0/invoke/{app_id.strip('/')}/method/{method_name.lstrip('/')}",
            json=data
        )

    @staticmethod
    def get(app_id: str, method_name: str) -> requests.Response:
        """
        get request to a specific app of the jeyn system

        Args:
            app_id: the id (usually the name of the app in snakecase) of the specific
                    jeyn app to contact
            method_name: the name of the method to call (this is the the route of
                         the app and not the http verb)

        Returns: the requests.Response object corresponding to the call.
        """
        return DaprClient.invoke_method(app_id=app_id, method_name=method_name, data=None, http_verb="GET")

    @staticmethod
    def post(app_id: str, method_name: str, data: Any) -> requests.Response:
        """
        post request to a specific app of the jeyn system

        Args:
            app_id: the id (usually the name of the app in snake case) of the specific
                    jeyn app to contact
            method_name: the name of the method to call (this is the the route of
                         the app and not the http verb)
            data: json representation of the object to post

        Returns: the requests.Response object corresponding to the call.
        """
        return DaprClient.invoke_method(app_id=app_id, method_name=method_name, data=data, http_verb="POST")

    @staticmethod
    def put(app_id: str, method_name: str, data: Any) -> requests.Response:
        """
        put request to a specific app of the jeyn system

        Args:
            app_id: the id (usually the name of the app in snake case) of the specific
                    jeyn app to contact
            method_name: the name of the method to call (this is the the route of
                         the app and not the http verb)
            data: json representation of the object to put

        Returns: the requests.Response object corresponding to the call.
        """
        return DaprClient.invoke_method(app_id=app_id, method_name=method_name, data=data, http_verb="PUT")

    @staticmethod
    def delete(app_id: str, method_name: str) -> requests.Response:
        """
        delete request to a specific app of the jeyn system

        Args:
            app_id: the id (usually the name of the app in snake case) of the specific
                    jeyn app to contact
            method_name: the name of the method to call (this is the the route of
                         the app and not the http verb)

        Returns: the requests.Response object corresponding to the call.
        """
        return DaprClient.invoke_method(app_id=app_id, method_name=method_name, http_verb="DELETE")

    @staticmethod
    def patch(app_id: str, method_name: str, data: Any) -> requests.Response:
        """
        put request to a specific app of the jeyn system

        Args:
            app_id: the id (usually the name of the app in snake case) of the specific
                    jeyn app to contact
            method_name: the name of the method to call (this is the the route of
                         the app and not the http verb)
            data: json object corresponding to the patch query

        Returns: the requests.Response object corresponding to the call.
        """
        return DaprClient.invoke_method(app_id=app_id, method_name=method_name, data=data, http_verb="PATCH")
