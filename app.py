from flask import Flask, render_template, request
from PIL import Image
import sys
import os

# Import WFC module (lowercase wfc.py)
from classes.wfc import setup

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

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

@app.route('/wfc-steps')
def wfc_steps():
    return render_template('WFC_steps.html')


if __name__ == '__main__':
    app.run(debug=True)
