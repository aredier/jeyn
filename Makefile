setup:
	dapr run --app-id prefect --app-port 3000 --dapr-http-port 3500 python prefect_app.py

test:
	python runtest.py