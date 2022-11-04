import boto3
from main import root
from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app
import warnings

def test_main():

    assert 200 == 200


def test_root():
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200


def test_labels():
    client = TestClient(app)

    if "faster-rcnn" in list_endpoints():
        response = client.post(
            "/labels",
            files={
                "photo": ("filename", open("testpics/pic1.jpg", "rb"), "image/jpeg")
            },
        )

        assert response.status_code == 200
    else:
        print("endpoint not live, can't test")
        warnings.warn(UserWarning("endpoint is not live, can't test properly"))
        assert True


def list_endpoints():

    client = boto3.client("sagemaker")

    response = client.list_endpoints()
    # responsedict = json.loads(response)

    endpoints = response["Endpoints"]

    n = len(endpoints)

    endpointnames = []
    for i in range(n):
        name = endpoints[i]["EndpointName"]
        endpointnames.append(name)
    return endpointnames
