# -*- coding: utf-8 -*-

import requests
from requests.auth import HTTPBasicAuth
from datetime import date
import xml.etree.ElementTree as ET


#################

username = "NAME"
password = "PASS"

#################

Day = date.today()

# SENTIENL-3(A) RBT
Req_S3 = "https://scihub.copernicus.eu/dhus/odata/v1/Products?$filter=IngestionDate gt datetime'" + str(Day) + "T00:00:00.000' and substringof('S3A_SL_1_RBT',Name) and substringof('_PS1_O_NT',Name)"

result = requests.get(Req_S3, auth = HTTPBasicAuth(username, password))

tree = ET.fromstring(result.text)


