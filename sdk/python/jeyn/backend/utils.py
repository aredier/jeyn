from requests import Response


def django_raise_for_status(response: Response) -> None:
    if response.status_code == 400:
        print(response.json())
    response.raise_for_status()