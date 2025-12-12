from flask import Flask, redirect, render_template, request, url_for
from PIL import Image
import sys
import os

# Import WFC module (lowercase wfc.py)
from classes.wfc import setup
import os
from datetime import datetime


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/wavefunctioncollapse')
def wavefunctioncollapsepage():
    # Run WFC on every page load
    print("\n" + "="*60)
    print("Running WFC from web request...")
    print("="*60)
    try:
        setup(tile_size=16, output_width=160, output_height=160, save_steps=True, use_config=True)
        print("WFC generation complete!")
    except Exception as e:
        print(f"Error running WFC: {e}")
    
    return render_template('WFC.html')


@app.route('/pixelArt', methods=['GET'])
def pixelArt_page():
    return render_template("pixelArt.html")

@app.route('/pixelArt', methods=['POST'])
def pixelArt_image():
    file = request.files['image']
    pixel_size = int(request.form['pixel_size'])


@app.route('/filter', methods=['GET'])
def filter_page():
    return render_template("filter.html")


    img = Image.open(file)
    width, height = img.size
    pixelated = Image.new("RGB", (width, height))

    for y in range(0, height, pixel_size):
        for x in range(0, width, pixel_size):
            r, g, b = img.getpixel((x, y))

            for yy in range(y, min(y + pixel_size, height)):
                for xx in range(x, min(x + pixel_size, width)):
                    pixelated.putpixel((xx, yy), (r, g, b))

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    output_filename = f"pixelated_{timestamp}.png"
    output_path = os.path.join(GALLERY_FOLDER, output_filename)
    pixelated.save(output_path)

  
    return render_template("pixelArt.html", output_image=f"/{GALLERY_FOLDER}/{output_filename}")


GALLERY_FOLDER = "static/images/gallery"
os.makedirs(GALLERY_FOLDER, exist_ok=True)

@app.route('/gallery')
def gallery():
    images = os.listdir(GALLERY_FOLDER)
    images = [f"/{GALLERY_FOLDER}/{img}" for img in images]
    return render_template("gallery.html", images=images)



if __name__ == '__main__':
    app.run(debug=True)
