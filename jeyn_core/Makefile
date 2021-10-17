.PHONY: build
build: artefact-store workflow-controller

.PHONY: artefact-store
artefact-store:
	$(MAKE) -C artefact_store build

.PHONY: workflow-controller
workflow-controller:
	$(MAKE) -C workflow_controller build

.PHONY: deploy
deploy:
	helm upgrade --install jeyn-core ./jeyn_core_charts

.PHONY: delete
delete:
	helm delete jeyn-core