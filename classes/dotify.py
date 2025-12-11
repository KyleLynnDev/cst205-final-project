from PIL import Image, ImageDraw
import numpy as np
import os

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    lv = len(hex_color)
    return tuple(int(hex_color[i:i+lv//3], 16) for i in range(0, lv, lv//3))

def dotify(input_file, output_path, max_dots=140, multiplier=50, bg_color="#ffffff", dot_color="#000000"):
    im = Image.open(input_file).convert("L")
    width, height = im.size
    if height == max(height, width):
        downsized_image = im.resize((int(height * (max_dots / width)), max_dots))
    else:
        downsized_image = im.resize((max_dots, int(height * (max_dots / width))))
    downsized_image_width, downsized_image_height = downsized_image.size
    blank_img_height = downsized_image_height * multiplier
    blank_img_width = downsized_image_width * multiplier
    padding = int(multiplier / 2)
    bg_rgb = hex_to_rgb(bg_color) if isinstance(bg_color, str) else tuple(bg_color)
    dot_rgb = hex_to_rgb(dot_color) if isinstance(dot_color, str) else tuple(dot_color)
    blank_image = np.full(((blank_img_height), (blank_img_width), 3), bg_rgb, dtype=np.uint8)
    pil_image = Image.fromarray(blank_image)
    draw = ImageDraw.Draw(pil_image)
    downsized_image = np.array(downsized_image)
    for y in range(0, downsized_image_height):
        for x in range(0, downsized_image_width):
            k = (x * multiplier) + padding
            m = (y * multiplier) + padding
            r = int((0.6 * multiplier) * ((255 - downsized_image[y][x]) / 255))
            leftUpPoint = (k - r, m - r)
            rightDownPoint = (k + r, m + r)
            twoPointList = [leftUpPoint, rightDownPoint]
            draw.ellipse(twoPointList, fill=dot_rgb)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pil_image.save(output_path)
    return output_path
