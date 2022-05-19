import abc
import json
from typing import List, Any, Dict

import requests

from .. import errors, typing, constants, artefacts


class Artefact(abc.ABC):
    _artefact_id = int
    _meta: artefacts.ArtefactClassMeta = None

    def __init_subclass__(cls, **kwargs):
        if cls._meta is not None:
            raise errors.MetaCreationError("`_meta` attribute was set explicitly, you probably want to define a Meta "
                                           "class instead")
        cls._meta = cls._generate_metadata()
        cls._meta.save_type_if_needed(check=True)

    @property
    def is_saved(self):
        return self._artefact_id is not None

    @property
    def artefact_id(self) -> int:
        return self._artefact_id

    @abc.abstractmethod
    def artefact_json(self) -> typing.JSON:
        pass

    @classmethod
    @abc.abstractmethod
    def from_artefact_json(cls, artefact_json: typing.JSON) -> "Artefact":
        pass

    @abc.abstractmethod
    def get_relationships(self) -> List["artefacts.Relationship"]:
        pass

    @classmethod
    def _generate_metadata(cls) -> "artefacts.ArtefactClassMeta":
        if not hasattr(cls, "Meta"):
            raise errors.ArtefactMetaError(f"no Meta class found for artefact {cls.__name__}")
        if not isinstance(cls.Meta, type):
            raise errors.ArtefactMetaError(f"the Meta class attribute must be a python type")
        return artefacts.ArtefactClassMeta(
            schema=getattr(cls.Meta, "schema"),
            artefact_type_name=getattr(cls.Meta, "artefact_type_name", cls.__name__)
        )

    @classmethod
    def get(cls, **kwargs) -> List["Artefact"]:
        response = requests.get(f"{constants.store_route}/api/artefact/query/?{cls._build_query_string(kwargs)}")
        response.raise_for_status()
        result = []
        for artefact_json in response.json():
            artefact_object = cls.from_artefact_json(artefact_json)
            artefact_object._artefact_id = artefact_json["id"]
            result.append(artefact_object)

        return result

    @classmethod
    def get_from_id(cls, artefact_id: int) -> "Artefact":
        response = requests.get(f"{constants.store_route}/api/artefact/{artefact_id}")
        response.raise_for_status()
        return cls.from_artefact_json(response.json())

    @staticmethod
    def _build_query_string(query_dict: Dict[str, Any]) -> str:
        return "&".join(f"artefact_data__{k}={v}" for k, v in query_dict.items())

    def update(self):
        pass

    def save(self):
        self._save_artefact()
        self._save_relationships()

    def _save_artefact(self):
        response = requests.post(f"{constants.store_route}/api/artefact/", data=self.generate_db_json())
        response.raise_for_status()
        response_json = response.json()
        self._artefact_id = response_json["id"]

    def _save_relationships(self):
        for relationship in self.get_relationships():
            relationship.save()

    def generate_db_json(self) -> typing.JSON:
        type_route = f"{constants.store_route}/api/artefact-type/{self._meta.artefact_type_name}/"
        return {
            "artefact_type_reference": self._meta.artefact_type_name,
            "artefact_data": json.dumps(self.artefact_json()),
        }

