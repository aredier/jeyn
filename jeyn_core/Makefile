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
	helm upgrade --install jeyn-core ./jeyn_core_charts --set redis.auth.password==$(kubectl get secret --namespace "default" jeyn-core-redis -o jsonpath="{.data.redis-password}" | base64 --decode)

.PHONY: init
init:
	helm upgrade --install jeyn-core ./jeyn_core_charts

.PHONY: dry-run
dry-run:
	helm upgrade --install jeyn-core ./jeyn_core_charts --debug --dry-run

.PHONY: delete
delete:
	helm delete jeyn-core