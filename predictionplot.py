
import matplotlib.patches as patches
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PIL import Image
from PIL import ImageColor
import numpy as np
from IPython.display import Image as ipImage
from IPython.display import display as ipdisplay
import os

def display_predictions(img_jpg, normalized_boxes, classes_names, confidences):
    
    colors = list(ImageColor.colormap.values())
    
    image_np = np.array(Image.open(img_jpg))
    
    #fig = plt.figure(figsize=(20, 20))
    fig = plt.figure()
    ax = plt.axes()
    ax.set_axis_off()
    
    fig.set_tight_layout(True)
    fig.tight_layout(pad = 0)
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
        
    fig.canvas.draw()
    rgbstring = fig.canvas.tostring_argb()
    
    pilimg = Image.frombytes('RGB', fig.canvas.get_width_height(),fig.canvas.tostring_rgb())
    
    # turn off matplotlib inline, otherwise get 2 plots
    #ipdisplay(pilimg)
    if not os.path.exists('images_with_boxes'):
        os.mkdir('images_with_boxes')
    #outpath = "images_with_boxes/pic.png"
    #pilimg.save(outpath)
    
    plt.savefig("images_with_boxes/pic.png", bbox_inches=None, pad_inches=0)
    
