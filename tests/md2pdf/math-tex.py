import os
import matplotlib.pyplot as plt
from typing import Union, Tuple

import numpy as np
from PIL import Image

def to_inline_expr(math_expr: str):
    return f"${math_expr}$"

def latex_to_image(math_expr: str, file_name: str) -> None:
    file_format = os.path.splitext(file_name)[1][1:]

    # Set the LaTeX font
    plt.rcParams['text.usetex'] = True
    plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

    # Add $ symbols to format the string as an inline math expression
    inline_expr = f"${math_expr}$"

    # Create a plot with the expression
    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, inline_expr, size=20, ha='center')

    # Remove the plot axes
    ax.set_axis_off()

    # Save the plot as a PNG with a transparent background
    plt.savefig(fname=file_name, format=file_format, transparent=True, bbox_inches='tight', pad_inches=0.0, dpi=300)
    plt.close(fig)

def crop_image(file_name:str):
    # Read input image, and convert to NumPy array.
    img = np.array(Image.open(file_name))  # img is 1080 rows by 1920 cols and 4 color channels, the 4'th channel is alpha.

    # Find indices of non-transparent pixels (indices where alpha channel value is above zero).
    idx = np.where(img[:, :, 3] > 0)

    # Get minimum and maximum index in both axes (top left corner and bottom right corner)
    x0, y0, x1, y1 = idx[1].min(), idx[0].min(), idx[1].max(), idx[0].max()
     
    print(x0, y0, x1, y1)

    # Crop rectangle and convert to Image
    out = Image.fromarray(img[y0:y1+1, x0:x1+1, :])

    # Save the result (RGBA color format).
    out.save("cropped_" + file_name)


print(latex_to_image(math_expr="x^2 + y^2 = 1", file_name="circle.png"))
crop_image("circle.png")
