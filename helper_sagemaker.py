from PIL import ImageDraw


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
