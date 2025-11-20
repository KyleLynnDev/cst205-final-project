from flask import Flask, render_template, request
from PIL import Image

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/wavefunctioncollapse')
def wavefunctioncollapsepage():
    return render_template('WFC.html')


if __name__ == '__main__':
    app.run(debug=True)
