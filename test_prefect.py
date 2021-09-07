from prefect import Flow, task


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


with Flow("test") as flow:
    a = hello()
    b = world()
    res = join(a, b)

flow.run()

