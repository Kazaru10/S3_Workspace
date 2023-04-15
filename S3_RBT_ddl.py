# -*- coding: utf-8 -*-

import requests
from requests.auth import HTTPBasicAuth
from datetime import date
import xml.etree.ElementTree as ET
import random
import zipfile


#################

username = "NAME"
password = "PASS"

#################

Day = date.today()

# SENTIENL-3(A) RBT
Req_S3 = "https://scihub.copernicus.eu/dhus/odata/v1/Products?$filter=IngestionDate gt datetime'" + str(Day) + "T00:00:00.000' and substringof('S3A_SL_1_RBT',Name) and substringof('_PS1_O_NT',Name)"

result = requests.get(Req_S3, auth = HTTPBasicAuth(username, password))

tree = ET.fromstring(result.text)

entries = tree.findall('{http://www.w3.org/2005/Atom}entry')

n = random.randint(0, len(entries) - 1)

e = entries[n]

prod_id = e.find('{http://www.w3.org/2005/Atom}id')

name = e.find('{http://www.w3.org/2005/Atom}title')
name = name.text

t = requests.get(prod_id.text + '/$value', auth = HTTPBasicAuth(username, password))

with open(r'name.zip', 'wb') as f:
    f.write(t.content)





