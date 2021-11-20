FROM python:3.10-buster

COPY ./requirements.txt /src/app/requirements.txt

RUN pip install -r /src/app/requirements.txt

COPY ./ /src/app

WORKDIR /src/app

RUN python setup.py install

CMD ["python", "test_scripts/test_artefact_creation.py"]

