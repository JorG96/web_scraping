# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 09:14:12 2021

@author: ASUS
"""
import requests
from bs4 import BeautifulSoup

URL = "https://fincaraiz.com.co/inmueble/local-en-arriendo/modelia/bogota/6717417"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results=soup.find_all("p")

for i,e in enumerate(results[1:5]+results[7:-4]):
    print(f'{i}: {e.text.strip()}')