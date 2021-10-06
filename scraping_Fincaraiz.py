#!python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 13:27:47 2021

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


#Options for chromedriver configurations
options = Options()
options.headless = True
options.add_argument("--window-size=12,1200")

initialPage=input('Enter web page url:')
# Change chromedriver path to your own
driver = webdriver.Chrome(options=options, executable_path=r'.\chromedriver.exe')
# Copy and Paste principal page url
driver.get(initialPage)
lnks=driver.find_elements_by_tag_name("a")
webLinks=[]
# traverse list
for lnk in lnks[1:-15]:
    # get_attribute() to get all href
    webLinks.append(lnk.get_attribute('href'))

driver.quit()

file_dir = os.path.dirname((os.path.abspath(__file__)))
columnsList=['Titulo','Ubicación','Ciudad','Código',
           'Dirección','Descripción','Área','Precio',
           'PrecioM2','estrato','Tipo de Cliente', 'teléfono',
           'nombre_cliente','apellido_cliente','latitud','longitud',
           'link']

def retrieveInfo(linksList):
    if linksList:
        df=pd.DataFrame()
        for url in webLinks:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser") #parsing the request
            elementScript=soup.find("script",{"id":"__NEXT_DATA__"})
            if elementScript==None:
                continue
            else:
                data=json.loads(elementScript.text)
                # retrieve information
                general_info=list(data['query'].values())
                props=data['props']['pageProps']
                
                stringL=[props['address'],
                        props['description']
                           ]
                segmentation=[
                        props['segmentation']['estrato'],
                        props['segmentation']['tipo_cliente'],
                        props['contact']['phones']['call'],
                        props['client']['firstName'],
                        props['client']['lastName']
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
                Newdf=pd.DataFrame([general_info+stringL+price+segmentation+location+[url]],columns=columnsList)
                df=pd.concat([df,Newdf],axis=0)

        return df
    else:
         print("Error: Links not found")
         
df=retrieveInfo(webLinks)
time=datetime.datetime.now()
file_name=time.strftime("%d-%m-%y_%H%M%S")
file_path = os.path.join(file_dir, f'{file_name}.xlsx')
df.to_excel(file_path, header=True, index=False)
print('----Scraping finished----')