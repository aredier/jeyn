import json
from typing import Iterable

import requests

from jeyn import core, errors


class ArtefactFactory:
    """
    factory for artefacts that allows you to create artefacts
    from other objects and/or query artefacts from their persisted state
     in the artefact service
    """

    @classmethod
    def get_artefact_from_id(cls, artefact_id: int) -> "core.Artefact":
        # TODO dapr get
        pass

    @classmethod
    def get_all_artefacts_for_schema(cls, schema: "core.ArtefactSchema") -> Iterable["core.Artefact"]:
        # TODO dapr get
        pass

    @classmethod
    def from_http_response(cls, response: requests.Response) -> "core.Artefact":
        """
        creates an artefact from an http response to the artefact service
        Args:
            response: the python response of the call

        Returns: the corresponding artefact if it exists

        """
        response.raise_for_status()
        response_json = response.json()
        return core.Artefact(
            schema=response_json["artefact_class"],
            json_data=response_json["artefact_data"]
        )

    @classmethod
    def convert_object_to_artefact(cls, convertible_object: "core.ArtefactConvertibleObject") -> "core.Artefact":
        """
        converts an object that follows the ArtefactConvertibleObject protocol to an artefact. If object does
        not adhere to the protocol, this will raise a DataConversion error
        Args:
            convertible_object: object that is convertible

        Returns: converted artefact

        """
        if not isinstance(convertible_object, core.ArtefactConvertibleObject):
            raise errors.DataConversionError(
                f"cannot convert {object} to Artefact it does not seem to adhere to the"
                f" ArtefactConvertibleObject protocol"
            )
        return convertible_object.convert_to_artefact()
