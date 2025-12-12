from flask import Flask, redirect, render_template, request, url_for
from PIL import Image
import sys
import os
from werkzeug.utils import secure_filename
from datetime import datetime

from classes.wfc import setup
from classes.dotify import dotify


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

GENERATED_FOLDER = "static/images/generated"
os.makedirs(GENERATED_FOLDER, exist_ok=True)

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



@app.route('/dotted', methods=['GET', 'POST'])
def dotted_page():
    if request.method == 'POST':
        file = request.files.get('image')
        if not file or file.filename == '':
            return render_template('dotted.html', result_url=None)
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'png'
        if ext not in ALLOWED_EXTENSIONS:
            ext = 'png'
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        out_name = f"dotted_{timestamp}.png"
        out_path = os.path.join(GENERATED_FOLDER, out_name)
        bg_color = request.form.get('bg_color', '#ffffff')
        dot_color = request.form.get('dot_color', '#000000')
        try:
            multiplier = int(request.form.get('multiplier', 50))
        except Exception:
            multiplier = 50
        dotify(file, out_path, multiplier=multiplier, bg_color=bg_color, dot_color=dot_color)
        result_url = f"/{GENERATED_FOLDER}/{out_name}"
        return render_template('dotted.html', result_url=result_url)
    return render_template('dotted.html')


GALLERY_FOLDER = "static/images/gallery"

os.makedirs(GALLERY_FOLDER, exist_ok=True)

@app.route('/gallery')
def gallery():
    images = os.listdir(GALLERY_FOLDER)
    images = [f"/{GALLERY_FOLDER}/{img}" for img in images]
    return render_template("gallery.html", images=images)



if __name__ == '__main__':
    app.run(debug=True)
