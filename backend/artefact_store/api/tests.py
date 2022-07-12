import json
import base64
from typing import Dict, Any

from django.test import TestCase, Client

from . import models

# Create your tests here.

class TestArtefactQuery(TestCase):

    def setUp(self):
        models.ArtefactType.objects.create(
            type_name="lor_characters",
            schema={
                "type": "object",
                "proerties": {
                    "character_name": {"type": "string"},
                    "charater_race": {"type": "string"},
                    "character_armement": {
                        "type": "object",
                        "properties": {
                            "weapon_type": {"type": "string"},
                            "weapon_name": {"type": "string"},
                            "n_kills": {"type": "number"}
                        }
                    }
                },
                "required": [
                    "character_name",
                    "charater_race",
                    "character_armement"
                ]
            }
        )

    @staticmethod
    def _format_query(query_args: Dict[str, Any]) -> bytes:
        return base64.b64encode(json.dumps(query_args).encode("utf-8"))

    def test_simple_query(self):
        artefact_type = models.ArtefactType.objects.get(type_name="lor_characters")

        bilbo_json = {
            "character_name": "bilbo",
            "charater_race": "hobbit",
            "character_armement": {
                "weapon_type": "dagger",
                "weapon_name": "sting"
            }
        }

        bilbo = models.Artefact(artefact_type_reference=artefact_type, artefact_data = bilbo_json)
        bilbo.save()

        test_client = Client()
        response = test_client.get(
            "/api/artefact/query/",
            {
                "q": self._format_query({"artefact_data__character_name": "bilbo"})
            })
        assert response.status_code == 200
        response_json = response.json()
        assert len(response_json) == 1
        assert response_json[0]["artefact_data"] == bilbo_json


    def test_complex_query(self):
        artefact_type = models.ArtefactType.objects.get(type_name="lor_characters")

        bilbo_json = {
            "character_name": "bilbo",
            "charater_race": "hobbit",
            "character_armement": {
                "weapon_type": "dagger",
                "weapon_name": "sting",
                "n_kills": 2
            }
        }

        bilbo = models.Artefact(artefact_type_reference=artefact_type, artefact_data = bilbo_json)
        frodo_json = {
            "character_name": "frodo",
            "charater_race": "hobbit",
            "character_armement": {
                "weapon_type": "dagger",
                "weapon_name": "sting",
                "n_kills": 4
            }
        }
        frodo = models.Artefact(artefact_type_reference=artefact_type, artefact_data=frodo_json)
        bilbo.save()
        frodo.save()

        test_client = Client()
        response = test_client.get(
            "/api/artefact/query/",
            {"q": self._format_query(
                {
                    "artefact_data__character_armement__weapon_type": "dagger",
                    "artefact_data__character_armement__n_kills": 2
                }
            )}
        )
        assert response.status_code == 200
        response_json = response.json()
        assert len(response_json) == 1
        assert response_json[0]["artefact_data"] == bilbo_json


    def test_multi_query(self):
        artefact_type = models.ArtefactType.objects.get(type_name="lor_characters")

        bilbo_json = {
            "character_name": "bilbo",
            "charater_race": "hobbit",
            "character_armement": {
                "weapon_type": "dagger",
                "weapon_name": "sting"
            }
        }

        bilbo = models.Artefact(artefact_type_reference=artefact_type, artefact_data=bilbo_json)
        frodo_json = {
            "character_name": "frodo",
            "charater_race": "hobbit",
            "character_armement": {
                "weapon_type": "dagger",
                "weapon_name": "sting"
            }
        }
        frodo = models.Artefact(artefact_type_reference=artefact_type, artefact_data=frodo_json)
        bilbo.save()
        frodo.save()

        test_client = Client()
        response = test_client.get(
            "/api/artefact/query/",
            {"q": self._format_query(
                {"artefact_data__charater_race": "hobbit", "artefact_data__character_name": "bilbo"}
            )}
        )
        assert response.status_code == 200
        response_json = response.json()
        assert len(response_json) == 1
        assert response_json[0]["artefact_data"] == bilbo_json

        response = test_client.get(
            "/api/artefact/query/",
            {"q": self._format_query(
            {"artefact_data__charater_race": "elf", "artefact_data__character_name": "bilbo"}
            )}
        )
        assert response.status_code == 200
        response_json = response.json()
        assert len(response_json) == 0