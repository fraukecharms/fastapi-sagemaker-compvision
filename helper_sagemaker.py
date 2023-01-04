from PIL import ImageDraw, ImageFont
import boto3
import json
import numpy as np


def parse_response(query_response):
    model_predictions = json.loads(query_response)
    normalized_boxes, classes, scores, labels = (
        model_predictions["normalized_boxes"],
        model_predictions["classes"],
        model_predictions["scores"],
        model_predictions["labels"],
    )
    # Substitute the classes index with the classes name
    class_names = [labels[int(idx)] for idx in classes]
    return normalized_boxes, class_names, scores


def query_endpoint(endpoint_name, input_img_rb):

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


def draw_all_boxes(image, boxes, labels=None, conf=None, threshold=0.9):

    img_width, img_height = image.size
    draw = ImageDraw.Draw(image, mode="RGBA")

    linewidth = max(int((img_width + img_height) // 250), 2)
    linewidth_textbox = max(int(linewidth // 3), 1)

    textsize = linewidth * 4
    shift_const = 3
    shift = np.array([-1, -1, 1, 1]) * shift_const * linewidth_textbox

    scale = np.array([img_width, img_height, img_width, img_height])

    if conf:
        inds = [i for i in range(len(conf)) if conf[i] >= threshold]
        boxes = [boxes[i] for i in inds]
        if labels:
            labels = [labels[i] for i in inds]

    for i in range(len(boxes)):

        box = np.array(boxes[i])
        left, top, right, bottom = box * scale

        points = [(left, top), (right, bottom)]

        draw.rectangle(points, outline="#c73286", width=linewidth)

        if labels:
            label = labels[i]

            font = ImageFont.truetype("font/OpenSans-Regular.ttf", textsize)

            textanchor = (left + 2 * linewidth, top + 2 * linewidth)
            draw.text(textanchor, label, font=font, anchor="lt")

            textbb = draw.textbbox(textanchor, label, font=font, anchor="lt")
            spaceybox = [sum(x) for x in zip(textbb, shift)]

            draw.rectangle(
                spaceybox, width=linewidth_textbox, fill=(255, 255, 255, 128)
            )
            # draw.rectangle(spaceybox, width = linewidth_textbox)

    return image


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
