# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 10:13:56 2021

@author: ASUS
"""
import requests
from bs4 import BeautifulSoup

URL = "https://fincaraiz.com.co/proyecto-de-vivienda/vitra-art-apartamentos/chapinero-central/bogota/6337605"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results=soup.find_all("p")

for i,e in enumerate(results):
    print(i,e.text.strip())
    # print(f'{i}: {e.text.strip()}')