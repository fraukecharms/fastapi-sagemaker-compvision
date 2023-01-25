from typing import Tuple, List
from PIL import ImageDraw, ImageFont, Image
import boto3
import json
import numpy as np


def parse_response(query_response: str) -> Tuple[list, list, list]:
    """extract bounding box coordinates, class labels, confidence values from sagemaker
    response

    Args:
        query_response (str): response string

    Returns:
        tuple[list, list, list]: bounding box coordinates, class labels, confidence
            values
    """

    model_predictions = json.loads(query_response)
    normalized_boxes, classes, scores, labels = (
        model_predictions["normalized_boxes"],
        model_predictions["classes"],
        model_predictions["scores"],
        model_predictions["labels"],
    )
    # Substitute the class index with the class name
    class_names = [labels[int(idx)] for idx in classes]
    return normalized_boxes, class_names, scores


def query_endpoint(
    endpoint_name: str, input_img_rb: bytearray
) -> Tuple[list, list, list]:
    """send image to sagemaker endpoint

    Args:
        endpoint_name (str): endpoint name
        input_img_rb (bytearray): image

    Returns:
        Tuple[list, list, list]: bounding box coordinates, class labels, confidence
            values
    """

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

    return normalized_boxes, class_names, scores


def draw_all_boxes(
    image: Image,
    boxes: List[List[float]],
    labels: List[str],
    conf: List[float] = None,
    threshold=0.9,
) -> Image:
    """draw bounding boxes on PIL image

    Args:
        image (Image): image to draw bounding boxes on
        boxes (List[List[float]]): list of bounding box coordinates
        labels (List[str]): list of object class labels
        conf (List[float], optional): list of confidence values for each detection.
            Defaults to None.
        threshold (float, optional): optional confidence threshold. Defaults to 0.9.

    Returns:
        Image: PIL Image with boxes
    """

    img_width, img_height = image.size
    draw = ImageDraw.Draw(image, mode="RGBA")

    # set bounding box linewidth based on image size
    # for object bounding box and text bounding box
    linewidth = max(int((img_width + img_height) // 250), 2)
    linewidth_textbox = max(int(linewidth // 3), 1)
    textsize = linewidth * 4
    font = ImageFont.truetype("font/OpenSans-Regular.ttf", textsize)

    # margins for text bounding box
    shift_const = 3
    shift = np.array([-1, -1, 1, 1]) * shift_const * linewidth_textbox

    # scaling factors for rescaling normalized boxes
    scale = np.array([img_width, img_height, img_width, img_height])

    if conf:
        inds = [i for i in range(len(conf)) if conf[i] >= threshold]
        boxes = [boxes[i] for i in inds]
        labels = [labels[i] for i in inds]

    for i in range(len(boxes)):

        # draw object bounding box
        box = np.array(boxes[i])
        left, top, right, bottom = box * scale
        points = [(left, top), (right, bottom)]
        draw.rectangle(points, outline="#c73286", width=linewidth)

        # draw label text
        label = labels[i]
        textanchor = (left + 2 * linewidth, top + 2 * linewidth)
        draw.text(textanchor, label, font=font, anchor="lt")

        # draw label bounding box with added margins
        textbb = draw.textbbox(textanchor, label, font=font, anchor="lt")
        spaceybox = [sum(x) for x in zip(textbb, shift)]
        draw.rectangle(spaceybox, width=linewidth_textbox, fill=(255, 255, 255, 128))

    return image


def list_endpoints() -> List[str]:
    """list live Sagemaker endpoints

    Returns:
        List[str]: list of endpoint names
    """

    client = boto3.client("sagemaker")

    response = client.list_endpoints()

    endpoints = response["Endpoints"]

    n = len(endpoints)

    endpointnames = []
    for i in range(n):
        name = endpoints[i]["EndpointName"]
        endpointnames.append(name)

    return endpointnames
