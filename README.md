HANDS-ON HTML
=================
Hack project for Big Hack Spring 2014.

Authors
=======
Rohan Chitnis
Brian Hou
Kunal Shalia

Description
===========
Draw a picture of what you would like to be turned into HTML and our service renders and displays the webpage, preserving positioning! Denote images which you would like embedded by enclosing them in a thick black box. Text is automatically detected and rendered in a pretty font!

Then begins phase two! Use hand gesture recognition to dynamically reposition, scale, and rotate the different components of the webpage you created, to calibrate the layout to your heart's content!

Installation
============

1. Install virtualenv.
2. `virtualenv venv --system-site-packages --distribute`
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`

Running
=======
1. 'python hack.py' (set image name at top of file first)
2. Navigate to http://localhost:5000/render.
3. 'python gesture.py' (starts gesture pipeline)

Libraries Used
==============
OpenCV, TODO