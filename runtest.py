from jeyn_clients.base_client import Client

controller_client = Client(service="jeyn-controller")
artefact_client = Client(service="artefact-store", port=3501)


model_schema = artefact_client.post("artefact-schemas/", json={"name": "models"})

model_json = {
    "path": "foo",
    "name": "bar",
    "version": "0.0.1",
}

print(model_schema)


model_artefact = artefact_client.post("artefacts/", json={
    "value": model_json,
    "schema": model_schema["id"]
})
print(model_artefact)


service_version_response = controller_client.post("services/service-versions/", json={
    "model_id": model_artefact["id"]
})


print(service_version_response)
service_version_data = controller_client.post("services/services/", json={
    "name": "test",
    "deployed": True,
    "deployment_scheme": {
        service_version_response["id"]: 1.0
    }
})


print(controller_client.get("services/services/"))
