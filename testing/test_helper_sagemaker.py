import boto3
from helper_sagemaker import parse_response, query_endpoint, draw_all_boxes
from PIL import Image, ImageDraw, ImageColor
from IPython.display import Image as ipImage
from IPython.display import display as ipdisplay
from helper_sagemaker import list_endpoints
import os
import warnings
import io





def test_parse_response(endpoint_name="faster-rcnn", image_file_name="testpics/pic3.jpg"):
    #aws_region = 'eu-west-1'
    #client = boto3.client("sagemaker-runtime", region_name=aws_region)

    if "faster-rcnn" in list_endpoints():

        with open(image_file_name, "rb") as file:
            input_img_rb = file.read()
    
        client = boto3.client("sagemaker-runtime")
    
        # The MIME type of the input data in the request body.
        content_type = "application/x-image"
        # The desired MIME type of the inference in the response.
        accept = "application/json;verbose;n_predictions=3"
        # Payload for inference.
        payload = input_img_rb
    
        response = client.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType=content_type,
            Accept=accept,
            Body=payload,
        )
    
    
        response_readable = response["Body"].read().decode("utf-8")
    
    
    
    
        normalized_boxes, class_names, scores = parse_response(response_readable)
    
        assert len(normalized_boxes) > 0
    else:
        warnings.warn(Warning("endpoint is not live, can't test properly"))
        assert True


def test_draw_all_boxes():

    testpic = "testpics/pic3.jpg"


    with open(testpic, "rb") as photo:

        photobytes = bytearray(photo.read())
        normalized_boxes, class_names, _ = query_endpoint("faster-rcnn", photobytes)


    image_stream = io.BytesIO(photobytes)
    image_stream.seek(0)
    photo2 = Image.open(image_stream)

    imgwbox = draw_all_boxes(photo2, normalized_boxes, labels = class_names)

    if not os.path.exists("images_with_boxes"):
        os.mkdir("images_with_boxes")
    outpath = "images_with_boxes/pic3_box.jpg"
    imgwbox.save(outpath)

    assert os.path.exists(outpath)
