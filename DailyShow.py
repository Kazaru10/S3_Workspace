# -*- coding: utf-8 -*-

from flask import Flask, render_template
import os

app = Flask(__name__)

img = os.path.join('static', 'Image')


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/S3_RBT")
def display_S3():
    file = os.path.join(img, 'img.jpg')
    return render_template('template.html', image=file)
    
app.run()
