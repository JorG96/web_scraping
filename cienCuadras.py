# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 10:08:27 2021

@author: ASUS
"""
import os
import requests
from bs4 import BeautifulSoup
import json

url="https://www.ciencuadras.com/inmueble/apartamento-en-arriendo-en-la-salle-medellin-2154784"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser") #parsing the request
elementScript=soup.find("script",{"id":"ciencuadras-state"})
data=json.loads(elementScript.text.replace('&q;','"'))
print(data)


ur2="https://www.ciencuadras.com/inmueble/oficina-en-venta-en-mejoras-publicas-bucaramanga-1597024"
page = requests.get(ur2)
soup = BeautifulSoup(page.content, "html.parser") #parsing the request
elementScript=soup.find("script",{"id":"ciencuadras-state"})
data2=json.loads(elementScript.text.replace('&q;','"'))


'''id,cityname,addres,transactiontype,stratification[0][leasefee],stratification[0][sellingprice],stratification[0][administrationvalue],propretyFeatures[builtArea],
propretyFeatures[antiquity],latitude,longitude'''