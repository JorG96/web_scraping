# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 09:06:20 2021

@author: ASUS
"""

import os
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


page = requests.get('https://www.metrocuadrado.com/inmueble/arriendo-local-comercial-bogota-acevedo-tejada-1-banos/4903-M2875462')
html = browser.page_source


# data=json.loads(elementScript.text)
# retrieve information
# general_info=list(data['query'].values())
# props=data['props']['pageProps']

# stringL=[props['address'],
#         props['description']
#            ]
# segmentation=[
#         props['segmentation']['estrato'],
#         props['segmentation']['tipo_cliente'],
#         props['contact']['phones']['call'],
#         props['client']['firstName'],
#         props['client']['lastName']
#     ]
# price=[
#        props['area'],
#        props['price'],
#        props['priceM2']
#        ]
# location=[
#         props['locations']['lat'],
#         props['locations']['lng']
#         ]
# Newdf=pd.DataFrame([general_info+stringL+price+segmentation+location+[url]])
# df=pd.concat([df,Newdf],axis=0)

columnsList=[]
