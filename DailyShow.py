# -*- coding: utf-8 -*-

from flask import Flask, render_template
import os
import random
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

app = Flask(__name__)

img = os.path.join('static', 'Image')

def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

scheduler = BackgroundScheduler()
scheduler.add_job(print_date_time, IntervalTrigger(seconds=10))
scheduler.start()


@app.route("/")
def hello_world():
    return "<p>Coucou, Monde!</p>"

## S3
@app.route("/S3_RBT")
def display_S3():
    path = os.path.join('static', 'Image', 'S3')
    dir_list = os.listdir(path)
    n = random.randint(0, len(dir_list) - 1)
    
    file = os.path.join(img, dir_list[n])
    return render_template('template_S3.html', image=file)
    
## S2
@app.route("/S2_TCI")
def display_S2():
    path = os.path.join('static', 'Image', 'S2')
    dir_list = os.listdir(path)
    n = random.randint(0, len(dir_list) - 1)
    
    file = os.path.join(img, dir_list[n])
    return render_template('template_S2.html', image=file)


   
if __name__ == '__main__':
    app.run()

## Shut down the scheduler
scheduler.shutdown(wait=False)


# See link below
# https://geekpython.in/render-images-from-flask#heading-displaying-local-images
