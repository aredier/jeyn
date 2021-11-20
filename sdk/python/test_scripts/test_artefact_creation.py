import dapr
import time

from jeyn import core

time.sleep(20)

schema = core.ArtefactSchema(
    json_schema={
        "type": "object",
        "properties": {
            "price": {"type": "number"},
            "name": {"type": "string"}
        }
    },
    schema_name="test_schema_14"
)

artefact = core.Artefact(
    schema=schema,
    json_data={"price": .75, "name": "coca-cola"}
)
schema.validate(artefact)
artefact.validate_data_client_side()

saved_artefact = artefact.save()

with dapr.clients.DaprClient() as client:
    client.shutdown()
