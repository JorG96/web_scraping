# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 09:06:20 2021

@author: ASUS
"""

import requests
import random
from bs4 import BeautifulSoup
user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
url = 'https://www.metrocuadrado.com/inmueble/arriendo-apartamento-bogota-chico-4-habitaciones-5-banos-3-garajes/2162-M3108906'

#Pick a random user agent
user_agent= random.choice(user_agent_list)
#Set the headers 
headers = {'User-Agent': user_agent}
#Make the request
response = requests.get(url,headers=headers)
soup = BeautifulSoup(response.content, "html.parser") #parsing the request

print("-------------------")