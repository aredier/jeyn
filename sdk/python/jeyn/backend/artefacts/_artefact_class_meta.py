import requests

from backend import typing, constants


class ArtefactClassMeta:
    artefact_type_name: str
    schema: typing.JSON

    def __init__(self, schema: typing.JSON, artefact_type_name: str):
        self.schema = schema
        self.artefact_type_name = artefact_type_name

    def save_type_if_needed(self, check: bool = True):
        response = requests.get(f"{constants.store_route}/api/artefact-type/{self.artefact_type_name}/")
        if response.status_code == 404:
            self.save_type()
            return
        response.raise_for_status()
        if check:
            self._check_type_data(response.json())
        self._update_with_remote_artefact_type(response.json())

    def _update_with_remote_artefact_type(self, remote_artefact_type_json: typing.JSON):
        # TODO
        pass

    def _check_type_data(self, response_json: typing.JSON):
        pass

    def save_type(self):
        response = requests.post(f"{constants.store_route}/api/artefact-type/", json=self.to_json())
        response.raise_for_status()

    def to_json(self) -> typing.JSON:
        return {
            "schema": self.schema,
            "type_name": self.artefact_type_name
        }