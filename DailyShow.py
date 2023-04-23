# -*- coding: utf-8 -*-

from flask import Flask, render_template
import os

app = Flask(__name__)

img = os.path.join('static', 'Image')


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# S3
@app.route("/S3_RBT")
def display_S3():
    file = os.path.join(img, 'img.jpg')
    return render_template('template.html', image=file)

# S2
@app.route("/S2_TCI")

app.run()
