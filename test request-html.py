# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 13:41:20 2021

@author: ASUS
"""
from requests_html import HTMLSession
s = HTMLSession()
url = 'https://www.metrocuadrado.com/bodega/arriendo/barranquilla/'

response = s.get(url)
container = response.html.find("#__next", first=True)
lista = container.find("li")