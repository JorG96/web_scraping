# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 09:06:20 2021

@author: ASUS
"""

import requests
import random
from bs4 import BeautifulSoup
import pandas as pd
import json


user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
dataColumns=['IDpropiedad','estado','estrato','telefono',
             'barrio','tipo de negocio','descripción',
             'antiguedad','area privada','area construida',
             'precio de renta', 'precio de venta','latitud',
             'longitud','ciudad','url']

url = 'https://www.metrocuadrado.com/bodega/arriendo/barranquilla/'
Weblinks=[]

#Pick a random user agent
user_agent= random.choice(user_agent_list)
#Set the headers 
headers = {'User-Agent': user_agent}
#Make the request
response = requests.get(url,headers=headers)
soup = BeautifulSoup(response.content, "html.parser") #parsing the request
df=pd.DataFrame()
print('retrieving information... please wait')
# links=soup.find_all(has_href)
# elementScript=soup.find("script",{"id":"__NEXT_DATA__"})
# data=json.loads(elementScript.text)

# props=data['props']['initialState']['realestate']['basic']

# propertyId=[props['propertyId']]

# info=[
     
#     props['propertyState'],
#     props['stratum'],
#     props['contactPhone'],
#     props['neighborhood'],
#     props['businessType'],
#     props['comment'],
#     props['builtTime'],
# ]
# price=[
#    props['area'],
#    props['areac'],
#    props['salePrice'],
#    props['rentPrice'],
#    ]
# location=[
#     props['coordinates']['lat'],
#     props['coordinates']['lon'],
#     props['city']['nombre']
#     ]
# Newdf=pd.DataFrame([propertyId+info+price+location+[url]],columns=dataColumns)

# print("-------------------")