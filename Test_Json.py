# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 09:29:22 2021

@author: ASUS
"""
import requests
from bs4 import BeautifulSoup
import json

URL = 'https://www.fincaraiz.com.co/inmueble/local-en-arriendo/chapinero-norte/bogota/6703031'
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser") #parsing the request
elementScript=soup.find("script",{"id":"__NEXT_DATA__"})
data=json.loads(elementScript.text)
general_info=data['query']
props=data['props']['pageProps']





# :{"lat":4.865344047546387,"lng":-74.05972290039062
#  4.6497273445129395,-74.06437683105469