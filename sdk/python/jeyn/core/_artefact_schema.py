import json
from typing import Dict, Any

import jsonschema
import requests

from jeyn import core, constants
from jeyn.core import _utils


class ArtefactSchema:
    """
    An artefact Schema is the definition of a type of artefact, using schemas allows you to set a contract
    for a data type to be shared accross differnt services and/or modules of your jeyn application(s).

    Jeyn itself defines schemas to support its basic services (TFModel, ...). But you can define you own using
    the jsonschema convention:

    >>> from jeyn.core import ArtefactSchema
    >>>
    >>>
    >>> schema = ArtefactSchema(
    ...     json_schema = {"type": "object", "properties": {"price": {"type": "number" }}}
    ...     schema_name = "my_first_schema"  # the name of this schema (unique)
    ... )

    Whenever persisting an Artefact, the artefact store will validate that the data you are trying to perisist
    satisfies it's schema's contract before saving it.
    """

    _json_schema: Dict
    _artefact_class_name: str

    def __init__(self, json_schema: Dict, schema_name: str):
        self._json_schema = json_schema
        self._artefact_class_name = schema_name

    @property
    def json_schema(self) -> Dict:
        return self._json_schema

    @property
    def schema_name(self) -> str:
        """name of the artefact class name in the artefact controller"""
        return self._artefact_class_name

    @property
    def json_data(self) -> Dict[str, Any]:
        return {
            "class_name": self._artefact_class_name,
            "schema_definition": self._json_schema
        }

    @classmethod
    def from_schema_name(cls, schema_name: str) -> "ArtefactSchema":
        """loads a schema definition from it's name by querying the
        remote artefact store"""
        with _utils.DaprClient() as client:
            response = client.get(
                app_id=constants.ARTEFACT_STORE_APP_ID,
                method_name=f"api/artefact-classes/{schema_name}",
            )
        response_json = json.loads(response.data)
        return cls(
            schema_name=schema_name,
            json_schema=response_json["schema_definition"]
        )

    def save_if_not_exists(self) -> None:
        with _utils.DaprClient() as client:
            get_response: requests.Response = client.get(
                app_id=constants.ARTEFACT_STORE_APP_ID,
                method_name=f"api/artefact-classes/{self._artefact_class_name}",
            )
            if get_response.status_code == 404:
                client.post(
                    app_id=constants.ARTEFACT_STORE_APP_ID,
                    method_name=f"api/artefact-classes/",
                    data=self.json_data,
                )
                return

            get_response.raise_for_status()

    def validate(self, artefact: "core.Artefact") -> None:
        jsonschema.validate(instance=artefact.json_data, schema=self.json_schema)
