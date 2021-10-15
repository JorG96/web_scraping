# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 09:09:00 2021

@author: ASUS
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

import json

options = Options()
options.headless = True
options.add_argument("--window-size=12,1200")
initialPage='https://www.metrocuadrado.com/inmueble/venta-apartamento-bogota-bellavista-3-habitaciones-4-banos-3-garajes/10366-6646'
webLinks=[]
# Change chromedriver path to your own
driver = webdriver.Chrome(options=options, executable_path=r'.\chromedriver.exe')
# Copy and Paste principal page url
driver.get(initialPage)
lnks=driver.page_source()
print(lnks)
# traverse list

    
driver.quit()


# usnig pd.Series.str.contains() function with default parameters
# search=df[0].str.contains("546-94228", case=True, flags=0, na=None, regex=True)