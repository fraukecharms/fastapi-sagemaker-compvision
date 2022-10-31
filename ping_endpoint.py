import boto3
from jsonresponse import parse_response
import json


def query_endpoint(endpoint_name="faster-rcnn", image_file_name="Naxos_Taverna.jpg"):
    #aws_region = boto3.Session().region_name

    #client = boto3.client("sagemaker-runtime", region_name=aws_region)

    with open(image_file_name, "rb") as file:
        input_img_rb = file.read()

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

    '''
    with open("taverna.json", "w") as file:
        json.dump(response_readable, file)
    '''

    print(type(response_readable))


    normalized_boxes, class_names, scores = parse_response(response_readable)

    print(class_names)
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

    '''
    with open("taverna.json", "w") as file:
        json.dump(response_readable, file)
    '''

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
