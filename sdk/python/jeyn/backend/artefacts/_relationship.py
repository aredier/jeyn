from typing import Optional

import attr
import requests

from backend import errors, constants, utils, artefacts


@attr.s
class Relationship:
    relationship_type: str = attr.field()
    parent: "Artefact" = attr.field()
    child: "Artefact" = attr.field()
    creation_time: Optional["str"] = attr.field(default=None)
    _id: Optional[int] = attr.field(init=False, default=None)

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @staticmethod
    def _check_artefact_is_saved(artefact: "Artefact"):
        if not artefact.is_saved:
            raise errors.RelationshipError("cannot create a relationship with not yet saved artefacts")

    def save(self):
        self._check_artefact_is_saved(self.parent)
        self._check_artefact_is_saved(self.child)
        response = requests.post(f"{constants.store_route}/api/artefact-relationship/", json=self.to_json())
        utils.django_raise_for_status(response)
        self.id = response.json()["id"]

    def to_json(self):
        return {
            "relationship_type": self.relationship_type,
            "child": self.child.artefact_id,
            "parent": self.parent.artefact_id
        }

    @classmethod
    def get_artefact_children_json(cls, artefact: "artefacts.Artefact"):
        """get all the children relationships of an artefact"""
        response = requests.get(f"{constants.store_route}/api/artefact/{artefact.artefact_id}")
        response.raise_for_status()
        result = []
        return response.json()["children"]
