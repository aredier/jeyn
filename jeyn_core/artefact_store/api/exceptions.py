from rest_framework import exceptions

from . import models


class ArtefactValidationError(exceptions.APIException):
    """error raised when an artefact is not valid"""

    _artefact_class: "models.ArtefactClass"
    status_code = 400
    default_code = "bad_request"
    default_detail = "request does not respect artefact definition contract"

    def __init__(self, artefact_class: "models.ArtefactClass"):
        self._artefact_class = artefact_class
        self.detail = f"request does not respect {artefact_class.class_name}'s schema contract"
