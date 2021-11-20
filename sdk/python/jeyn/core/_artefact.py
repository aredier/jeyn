import json
from typing import Dict, Union, Optional, Any

import requests

from jeyn import constants, errors, core
from jeyn.core import _utils


# TODO add validation with pydentry
class Artefact:
    """
    An artefact is simply a piece of data that is persisted in the jeyn artefact-store.
    This artefact store will be the back bone on which more sofisticated and specialized services are based.
    For instance a model that can be persistent is converted to a model artefact to be saved.

    You should not subclass the Artefact class directly but rather use the ArtefactConvertibleObject class if
    you want to create python representations of specific artefacts
    """

    _schema: Union["core.ArtefactSchema", str]
    _json_data: Dict
    _validate_before_saving: bool
    _id: Optional[int] = None

    def __init__(self, schema: Union["core.ArtefactSchema", str], json_data: Dict, validate_before_saving: bool = True):
        self._schema = schema
        self._json_data = json_data
        self._validate_before_saving = validate_before_saving

    def set_id(self, id: int) -> None:
        """sets the db id of the artefact. If the id is already set, will raise a DataConsistencyError"""
        if self._id is not None:
            raise errors.DataConsistencyError(f"cannot reset id of an artefact. current id is {self._id}")
        self._id = id

    @property
    def id(self) -> Optional[int]:
        """db id of this artefact"""
        return self._id

    @property
    def json_data(self) -> Dict:
        """underlying data of the artefact"""
        return self._json_data

    def convert_to_artefact(self) -> "Artefact":
        """
        method that returns self to make sure Artefacts can be converted to artefacts
        """
        return self

    def get_schema(self) -> "core.ArtefactSchema":
        """method that gets the schema from the artefact service if not yet loaded and returns it"""
        if isinstance(self._schema, core.ArtefactSchema):
            return self._schema
        return core.ArtefactSchema.from_schema_name(self._schema)

    def validate_data_client_side(self) -> None:
        """helper method to validate this artefact client side"""
        self.get_schema().validate(self)

    def save(self) -> "Artefact":
        """
        persists this artefact in the artefact store, if allow_update is set to false,
        jeyn will raise a DataConsistencyError if an artefact with the same id exists.
        Jeyn might also raise a DataConsistencyError when trying to update an artefact with a different schema.
        """
        if self._validate_before_saving:
            self.validate_data_client_side()
        self.get_schema().save_if_not_exists()
        with _utils.DaprClient() as client:
            response = self._execute_http_post(client=client)
        return core.ArtefactFactory.from_http_response(response)

    def _execute_http_post(self, client: "_utils.DaprClient") -> "requests.Response":
        return client.post(
            constants.ARTEFACT_STORE_APP_ID, "api/artefacts/", self._request_json
        )

    @property
    def _request_json(self) -> Dict[str, Any]:
        """json of a post/put operation on the artefact store service"""
        return {
            "artefact_data": self.json_data,
            "artefact_class": self.get_schema().schema_name
        }

    def update(self) -> "Artefact":
        """updates the values of an already existing artefact"""
        if self.id is None:
            raise errors.DataConsistencyError("Artefact does not seem to be loaded from remote state, cannot update")
        if self._validate_before_saving:
            self.validate_data_client_side()
        with _utils.DaprClient() as client:
            response = self._execute_http_put(client=client)
        return core.ArtefactFactory.from_http_response(response)

    def _execute_http_put(self, client: "_utils.DaprClient") -> "requests.Response":
        return client.put(
            constants.ARTEFACT_STORE_APP_ID, f"api/artefacts/{self.id}", self._request_json
        )

    def delete(self) -> None:
        """deletes an artefact"""
        if self.id is None:
            raise errors.DataConsistencyError("Artefact does not seem to be loaded from remote state, cannot delete")
        with _utils.DaprClient() as client:
            client.delete(constants.ARTEFACT_STORE_APP_ID, f"app/artefacts/{self.id}", self._request_json)
