from flask import Flask, render_template, redirect, url_for
import json

from process_input import jsonify
# from render import render_json

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

def fix_image_links(jason):
  image0 = {
    'top': 0,
    'left': 0,
    'width': 0.3,
    'aspect': 2,
    'path': url_for('static', filename='images/the.jpg')
  }
  for image in jason['images'].values():
    new_img = url_for('static', filename=image['path'])
    image['path'] = new_img
  # jason['images'][2] = image0
  # jason['num_images'] += 1
  return jason

@app.route('/render/')
def render():
  # uploads image
  img = 'images/landmark1.jpg'
  jason = json.loads(jsonify(img))
  jason = fix_image_links(jason)
  return render_template('user.html', content=jason)

@app.route('/render/instructions')
def instructions():
  with open('static/instructions.txt') as f:
    return f.read()

@app.route('/upload/')
def upload():
  return render_template('upload.html')

if __name__ == '__main__':
  app.run(debug=True)
