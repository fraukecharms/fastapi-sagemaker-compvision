import boto3
from helper_rekognition import process_response, draw_bounding_boxes
from PIL import Image, ImageDraw, ImageColor
from IPython.display import Image as ipImage
from IPython.display import display as ipdisplay
import os

def test_rekognition(testpic="testpics/pic4.png"):

    client = boto3.client("rekognition")

    with open(testpic, "rb") as photo:
        response = client.detect_labels(Image={"Bytes": photo.read()})

    print(response.keys())

    assert response['ResponseMetadata']['HTTPStatusCode'] == 200
    
    return response


def test_process_response():

    testpic = "testpics/pic4.png"

    client = boto3.client("rekognition")

    with open(testpic, "rb") as photo:
        response = client.detect_labels(Image={"Bytes": photo.read()})

    boxes = process_response(response)
    
    assert len(boxes) > 0




def test_draw_bounding_boxes():

    testpic = "testpics/pic3.jpg"

    client = boto3.client("rekognition")

    with open(testpic, "rb") as photo:

        response = client.detect_labels(Image={"Bytes": photo.read()})

    boxes = process_response(response)

    photo2 = Image.open(testpic)

    imgwbox = draw_bounding_boxes(photo2, boxes[0])

    os.mkdir('images_with_boxes')
    outpath = "images_with_boxes/pic3_box.jpg"
    imgwbox.save(outpath)
    
    assert os.path.exists(outpath)
