import abc
import json
from typing import List, Any, Dict

import requests

from .. import errors, constants, artefacts
import typing_utils


class Artefact(abc.ABC):
    _artefact_id: int = None
    _meta: artefacts.ArtefactClassMeta = None

    def __init_subclass__(cls, **kwargs):
        if cls._meta is not None:
            raise errors.MetaCreationError("`_meta` attribute was set explicitly, you probably want to define a Meta "
                                           "class instead")
        cls._meta = cls._generate_metadata()
        cls._meta.save_type_if_needed(check=True)

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
        return cls.from_artefact_json(artefact_json=response.json())

    @classmethod
    @abc.abstractmethod
    def from_artefact_json(cls, artefact_json: typing_utils.JSON) -> "Artefact":
        pass

    @property
    def is_saved(self):
        return self._artefact_id is not None

    @property
    def artefact_id(self) -> int:
        return self._artefact_id

    @abc.abstractmethod
    def artefact_json(self) -> typing_utils.JSON:
        pass

    @abc.abstractmethod
    def get_relationships(self) -> List["artefacts.Relationship"]:
        pass

    def update(self):
        pass

    def save(self):
        self._save_artefact()
        self._save_relationships()

    def generate_db_json(self) -> typing_utils.JSON:
        type_route = f"{constants.store_route}/api/artefact-type/{self._meta.artefact_type_name}/"
        return {
            "artefact_type_reference": self._meta.artefact_type_name,
            "artefact_data": json.dumps(self.artefact_json()),
        }

    @classmethod
    def extract_artefact_from_singleton_relationship(
            cls, relationship_jsons: List[typing_utils.JSON], relationship_type
    ):
        """
        extracts the artefact from the relationship jsons of an artefact corresponding to a relationship type that
        should be unique. For instance if you want to extract the unique dataset batch that was used to trained a model,
        to get the unique formula of a dataset and so on.
        """
        use_case_artefact_ids = [
            relationship["parent"]
            for relationship in relationship_jsons
            if relationship["relationship_type"] == relationship_type
        ]
        if len(use_case_artefact_ids) == 0:
            raise errors.LoadingError(f"checkpoint has no relationship of type <{relationship_type}>,"
                                      f" backend data seems corrupt.")
        if len(use_case_artefact_ids) > 1:
            raise errors.LoadingError(f"checkpoint seems to have several relationship of type <{relationship_type}>, "
                                      f"backend data seems corrupt.")
        return use_case_artefact_ids[0]

    @staticmethod
    def _build_query_string(query_dict: Dict[str, Any]) -> str:
        return "&".join(f"artefact_data__{k}={v}" for k, v in query_dict.items() if v is not None)

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

    def _save_artefact(self):
        response = requests.post(f"{constants.store_route}/api/artefact/", data=self.generate_db_json())
        response.raise_for_status()
        response_json = response.json()
        self._artefact_id = response_json["id"]

    def _save_relationships(self):
        for relationship in self.get_relationships():
            relationship.save()


