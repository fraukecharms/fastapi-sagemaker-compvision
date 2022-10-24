
import matplotlib.patches as patches
from matplotlib import pyplot as plt
#from matplotlib.backends.backend_agg import FigureCanvasAgg
from PIL import Image
from PIL import ImageColor
import numpy as np


def display_predictions(img_jpg, normalized_boxes, classes_names, confidences):
    colors = list(ImageColor.colormap.values())
    image_np = np.array(Image.open(img_jpg))
    plt.figure(figsize=(20, 20))
    ax = plt.axes()
    ax.imshow(image_np)

    for idx in range(len(normalized_boxes)):

        left, bot, right, top = normalized_boxes[idx]

        x, w = [val * image_np.shape[1] for val in [left, right - left]]
        y, h = [val * image_np.shape[0] for val in [bot, top - bot]]

        color = colors[hash(classes_names[idx]) % len(colors)]
        rect = patches.Rectangle(
            (x, y), w, h, linewidth=3, edgecolor=color, facecolor="none"
        )

        ax.add_patch(rect)
        ax.text(
            x,
            y,
            "{} {:.0f}%".format(classes_names[idx], confidences[idx] * 100),
            bbox=dict(facecolor="white", alpha=0.5),
        )