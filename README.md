# Jeyn

Welcome to jeyn, jeyn is an open source framework that aims at providing an infrastructure
for production ML applications and give everything a DS team needs to be
able to hit the ground running with as little dev-ops knowledge as possible.


As of writting jeyn is still in its infency and very much not ready to be used in any
kind of production context.

## contributing to jeyn.
jeyn is based on 2 major open source technologies:
- dapr: a framework that abstracts cloud implementation to be able to have the same code or architecture
  running in different setps with a change of configuration
- Argo: to run your machine learning workflows.

## getting started. 

To deply jeyn, you will need to have dapr installed and initialized:

```
dapr init
```

then you can deploy the artefact store and the workflow controller using the dapr cli:
```
dapr run --app-id artefact_store --app-port 8000 --dapr-http-port 3500 python manage.py runserver 8000
dapr run --app-id workflow_controller --app-port 8001 --dapr-http-port 3501 python manage.py runserver 8001
```

then you can simply test your integration with by curling  http://localhost:3501/v1.0/invoke/artefact_store/method/api/related_view
and you should  have an output similar to this: 
```
{
  "message": "this is still the artefact store",
  "relate_message": "b'{\"message\":\"this is the workflow controller\"}'"
}
```