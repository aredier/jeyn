from flask import Flask
from prefect import Flow, task

app = Flask("foo")


@task
def hello():
    return "hello"


@task
def world():
    return "world"


@task
def join(a, b):
    res = a + b
    return res


@app.route("/foo/")
def foo():
    with Flow("test") as flow:
        a = hello()
        b = world()
        res = join(a, b)

    flow.run()
    return "done"


app.run(port=3000)
