# -*- coding: utf-8 -*-


from flask import Flask, render_template
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import time
from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
import pycurl
import random
from zipfile import ZipFile
import glob
import xarray as xr


app = Flask(__name__)

img = os.path.join('static', 'Image')

def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

# Mask function ###############################################################

def Ocean_mask(x):
    # Flagin Ocean
    x_bin = bin(x)
    try:
        if (int(x_bin[-2]) == 1):
            y = 1
        else:
            y = 0
    except:
        y = 0
    return y
    
def Land_mask(x):
    # Flagin Land
    x_bin = bin(x)
    try:
        if (int(x_bin[-4]) == 1):
            y = 1
        else:
            y = 0
    except:
        y = 0
    return y

def Cloud_mask(x):
    # Flagin Cloud
    x_bin = bin(x)
    try: 
        if (int(x_bin[-15]) == 1):
            y = 1
        else:
            y = 0
    except:
        y = 0
    return y

## S3 RBT processing ##########################################################

def S3_RBT_process(path2prod):
    SAFE_directory = path2prod
    
    # read all the bands from our products: nadir and a-stripe
    solar_channels = [1,2,3,4,5,6]
    TIR_channels = [7,8,9]

    band_dict = {}
    
    for pattern, bands_needed, flag_file, flag_var in zip(['S*radiance_an.nc', 'S*BT_in.nc'], 
                                                         [solar_channels, TIR_channels],
                                                         ["flags_an.nc", "flags_in.nc"],
                                                         ["confidence_an", "confidence_in"]):
            band_files = glob.glob(os.path.join(SAFE_directory, pattern))
            band_vars = xr.open_mfdataset(band_files)

            # read variables
            for band_var in band_vars:
                band_num = int(band_var.split('_')[0][1])
                if band_num in bands_needed and "exception" not in band_var and "orphan" not in band_var:
                    print(f"Reading:  {band_var}")
                    band_dict[band_var] = band_vars[band_var].data[:,:]
            band_vars.close()
            
    

## Download ###################################################################

def ddl_n_stuffs():
    # Products download 
    
    # Get product list released the day before
    Req1 = "https://scihub.copernicus.eu/dhus/odata/v1/Products?$filter=IngestionDate gt datetime'2023-04-08T00:00:00.000' and substringof('S3A_SL_1_RBT',Name) and substringof('_PS1_O_NT',Name)"
    r = requests.get(Req1, auth = HTTPBasicAuth('lya', 'Oriflammes123'))
    tree = ET.fromstring(r.text)
    entries = tree.findall('{http://www.w3.org/2005/Atom}entry')
    n = random.randint(0, len(entries) - 1)
    e = entries[n]
    prod_id = e.find('{http://www.w3.org/2005/Atom}id')
    name = e.find('{http://www.w3.org/2005/Atom}title')
    name = name.text
    # Download via request 
    t = requests.get(prod_id.text + '/$value', auth = HTTPBasicAuth('lya', 'Oriflammes123'))
    # save to zip file
    name_zip = name + '.zip'
    path2zip = os.path.join('static', name_zip)
    with open(path2zip, 'wb') as f:
        f.write(t.content)
    # Extract zip file
    tmp = os.path.join('static', 'tmp')
    with ZipFile(path2zip, 'r') as zip_ref:
        zip_ref.extractall(tmp)

    
## S3_RBT_main ################################################################

def S3_main():
    # Main script S3 process
    ddl_n_stuffs()
    # Recuperation directory 
    # Process S3
    # sauvegarde img processed dans repertoir static

###############################################################################

scheduler = BackgroundScheduler()
scheduler.add_job(S3_main, IntervalTrigger(hours=4))
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
@app.route("/S2_IMG")
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
