import boto3
from jsonresponse import parse_response

aws_region = boto3.Session().region_name

client = boto3.client('sagemaker-runtime', region_name = aws_region)

endpoint_name = 'inference-pytorch-od1-fasterrcnn-resnet50-fpn'

image_file_name = 'Naxos_Taverna.jpg'

with open(image_file_name, "rb") as file:
    input_img_rb = file.read()

"""
query_response = model_predictor.predict(
    input_img_rb,
    {
        "ContentType": "application/x-image",
        "Accept": "application/json;verbose;n_predictions=22",
    },
)

"""


client = boto3.client('sagemaker-runtime')

content_type = "application/x-image"         # The MIME type of the input data in the request body.
accept = "application/json;verbose;n_predictions=22"     # The desired MIME type of the inference in the response.
payload = input_img_rb                                             # Payload for inference.
response = client.invoke_endpoint(
    EndpointName=endpoint_name, 
    ContentType=content_type,
    Accept=accept,
    Body=payload
    )                            
                            
        
print(response) 

response_readable = response['Body'].read().decode('utf-8')

print(type(response_readable))

normalized_boxes, class_names, scores = parse_response(response_readable)

print(class_names)
