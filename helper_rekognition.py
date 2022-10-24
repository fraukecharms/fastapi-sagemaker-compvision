import boto3
import io
from PIL import Image, ImageDraw, ImageColor


from fastapi import FastAPI, UploadFile, File
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

from IPython.display import Image as ipImage
from IPython.display import display as ipdisplay


def process_response(response, verbose=False):

    # print(response.keys())
    boxes = []

    if verbose:
        print("Detected labels")
        print()

    for label in response["Labels"]:
        if verbose:
            print("Label: " + label["Name"])
            print("Confidence: " + str(label["Confidence"]))
            print("Instances:")

        for instance in label["Instances"]:
            if verbose:
                print("  Bounding box")
                print("    Top: " + str(instance["BoundingBox"]["Top"]))
                print("    Left: " + str(instance["BoundingBox"]["Left"]))
                print("    Width: " + str(instance["BoundingBox"]["Width"]))
                print("    Height: " + str(instance["BoundingBox"]["Height"]))
                print("  Confidence: " + str(instance["Confidence"]))
                print()

            box = instance["BoundingBox"]
            boxes.append(box)

    return boxes


def draw_bounding_boxes(image, box):

    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)

    left = imgWidth * box["Left"]
    top = imgHeight * box["Top"]
    width = imgWidth * box["Width"]
    height = imgHeight * box["Height"]

    points = (
        (left, top),
        (left + width, top),
        (left + width, top + height),
        (left, top + height),
        (left, top),
    )
    draw.line(points, fill="#c73286", width=4)

    # image.show()

    # displays image when run from a jupyter notebook; useful for debugging/experimenting
    # you can comment next line out for Swagger UI demo in browser
    """
    ipdisplay(image)
    
    # save image with boxes to file
    outpath = "images_with_boxes/pic.png"
    image.save(outpath)
    """

    return image
