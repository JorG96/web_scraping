# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 13:27:47 2021

@author: ASUS
"""
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

indexList=['Codigo','Ubicacion','Ciudad','Contrato']

URL = 'https://www.fincaraiz.com.co/inmueble/local-en-arriendo/chapinero-norte/bogota/6703031'
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser") #parsing the request
elementScript=soup.find("script",{"id":"__NEXT_DATA__"})
data=json.loads(elementScript.text)
# retrieve information
general_info=list(data['query'].values())
props=data['props']['pageProps']

stringL=[
        props['address'],
        props['description']
           ]
segmentation=[
        props['segmentation']['estrato'],
        props['segmentation']['tipo_cliente'],
        
    ]
price=[
       props['area'],
       props['price'],
       props['priceM2']
       ]
location=[
        props['locations']['lat'],
        props['locations']['lng']
        ]
s=pd.Series(general_info+stringL+price+location)

