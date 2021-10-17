.PHONY: static-files
static-files:
	python manage.py collectstatic --no-input

.PHONY: docker
docker:
	docker build -t workflowcontroller -f Dockerfile .

.PHONY: build
build: static-files docker