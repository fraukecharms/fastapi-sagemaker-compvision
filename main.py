from fastapi import FastAPI, UploadFile, File

from fastapi import HTTPException
from fastapi.responses import StreamingResponse

# from fastapi.responses import FileResponse
import uvicorn

# import boto3
import io

from helper_sagemaker import draw_all_boxes
from helper_sagemaker import query_endpoint
from PIL import Image

# from PIL import Image, ImageDraw

# from PIL import ExifTags, ImageColor

app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "Hello there ... append '/docs' to the URL to interact with the API"
    }


@app.post("/labels")
async def label_objects(photo: UploadFile = File(...)):
    """upload image"""

    # client = boto3.client("rekognition")

    # response = client.detect_labels(Image={"Bytes": photo.file.read()})

    endpoint_name = "faster-rcnn"
    # normalized_boxes, class_names, scores = query_endpoint2(endpoint_name, photo.file.read())

    _, class_names, scores = query_endpoint(endpoint_name, photo.file.read())

    response = {}

    response["label"] = class_names[0]
    response["confidence"] = scores[0]

    return response


@app.post("/draw_boxes")
async def draw_boxes(photo: UploadFile = File(...)):
    """upload image"""

    filename = photo.filename
    file_ext = filename.split(".")[-1]

    if file_ext == "jpg":
        file_ext = "jpeg"

    if not (file_ext == "jpeg"):
        raise HTTPException(status_code=415, detail="Unsupported file provided.")

    photobytes = bytearray(photo.file.read())

    endpoint_name = "faster-rcnn"

    normalized_boxes, classes_names, _ = query_endpoint(endpoint_name, photobytes)

    image_stream = io.BytesIO(photobytes)
    image_stream.seek(0)
    photo2 = Image.open(image_stream)

    # rawbox = normalized_boxes[0]
    # left, bot, right, top = rawbox
    # box = {}
    # box["Left"] = left
    # box["Top"] = bot
    # box["Right"] = right
    # box["Bottom"] = top

    imgwbox = draw_all_boxes(photo2, normalized_boxes, labels=classes_names)

    # conversion was necessary when I was being sloppy with jpeg vs png
    # imgwbox2 = imgwbox.convert("RGB")

    imstream = io.BytesIO()
    imgwbox.save(imstream, file_ext)
    imstream.seek(0)

    return StreamingResponse(imstream, media_type="image/" + file_ext)


if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")
