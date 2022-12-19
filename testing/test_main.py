import boto3
from main import root
from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app
from helper_sagemaker import list_endpoints
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
                "photo": ("testpics/pic1.jpg", open("testpics/pic1.jpg", "rb"), "image/jpeg")
            },
        )

        assert response.status_code == 200
    else:
        warnings.warn(Warning("endpoint is not live, can't test properly"))
        assert True


def test_draw_boxes():
    client = TestClient(app)

    if "faster-rcnn" in list_endpoints():
        response = client.post(
            "/draw_boxes",
            files={
                "photo": ("testpics/pic1.jpg", open("testpics/pic1.jpg", "rb"), "image/jpeg")
            },
        )

        assert response.status_code == 200
    else:
        warnings.warn(Warning("endpoint is not live, can't test properly"))
        assert True



