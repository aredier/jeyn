dummy_workflow = {
  "namespace": "argo",
  "serverDryRun": False,
     "workflow": {
      "metadata": {
        "generateName": "hello-world-",
        "namespace": "argo",
        "labels": {
          "workflows.argoproj.io/completed": "false"
         }
      },
     "spec": {
       "templates": [
        {
         "name": "whalesay",
         "arguments": {},
         "inputs": {},
         "outputs": {},
         "metadata": {},
         "container": {
          "name": "",
          "image": "docker/whalesay:latest",
          "command": [
            "cowsay"
          ],
          "args": [
            "hello world"
          ],
          "resources": {}
        }
      }
    ],
    "entrypoint": "whalesay",
    "arguments": {}
  }
}
}