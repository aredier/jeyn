import pytest

from jeyn.core import Artefact, ArtefactSchema


@pytest.fixture()
def fake_artefact_schema() -> ArtefactSchema:
    return ArtefactSchema(json_schema={
        "type": "object",
        "properties": {
            "foo": {"type": "number"},
        }
    },
        schema_name="fake")


@pytest.fixture()
def fake_artefact(fake_artefact_schema: ArtefactSchema) -> Artefact:
    return Artefact(
        schema=fake_artefact_schema,
        json_data={"foo": 42}
    )
