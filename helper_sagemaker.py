from PIL import ImageDraw
import boto3
import json


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


def query_endpoint2(endpoint_name, input_img_rb):

    client = boto3.client("sagemaker-runtime")

    # The MIME type of the input data in the request body.
    content_type = "application/x-image"
    # The desired MIME type of the inference in the response.
    accept = "application/json;verbose;n_predictions=1"
    # Payload for inference.
    payload = input_img_rb

    response = client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType=content_type,
        Accept=accept,
        Body=payload,
    )

    print(response)

    response_readable = response["Body"].read().decode("utf-8")

    # with open("taverna.json", "w") as file:
    #    json.dump(response_readable, file)

    print(type(response_readable))

    normalized_boxes, class_names, scores = parse_response(response_readable)

    print(class_names)
    return normalized_boxes, class_names, scores


def list_endpoints():

    client = boto3.client("sagemaker")

    response = client.list_endpoints()
    # responsedict = json.loads(response)

    endpoints = response["Endpoints"]

    n = len(endpoints)

    for i in range(n):
        name = endpoints[i]["EndpointName"]
        print(name)


def draw_bounding_boxes3(image, box):

    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)

    left = imgWidth * box["Left"]
    top = imgHeight * box["Top"]
    right = imgWidth * box["Right"]
    bottom = imgHeight * box["Bottom"]

    points = [(left, top), (right, bottom)]

    draw.rectangle(points, outline="#c73286", width=4)

    # image.show()

    # displays image when run from a jupyter notebook; useful for debugging/experimenting
    # you can comment next line out for Swagger UI demo in browser

    # ipdisplay(image)

    # # save image with boxes to file
    # outpath = "images_with_boxes/pic.png"
    # image.save(outpath)

    return image
