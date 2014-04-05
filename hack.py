from flask import Flask, render_template, redirect, url_for
import json

from process_input import jsonify
from render import render_json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def generate_page(json_file):
    """Takes in the json representation of the page and returns HTML."""
    jason = json.loads(json_file)
    image0 = {
        'top': 0,
        'left': 0,
        'width': 0.3,
        'aspect-ratio': 2,
        'path': url_for('static', filename='images/the.jpg')
    }
    for image in jason['images'].values():
        new_img = url_for('static', filename=image['path'])
        image['path'] = new_img
    # jason['images'][2] = image0
    # jason['num_images'] += 1
    return render_json(jason)

@app.route('/render/')
def render():
    # uploads image
    img = 'images/test'
    return generate_page(jsonify(img))

if __name__ == '__main__':
    app.run(debug=True)
