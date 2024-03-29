#!python
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
import time
import random
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]


def retrieveInfo(linksList,dataColumns):
    if linksList:
        df=pd.DataFrame()
        for url in linksList:
            elementScript=None
            sleep_time=random.uniform(0.98, 1.37)
            time.sleep(sleep_time)
            print(f'retrieving information from {url}... please wait')
            try:
                user_agent= random.choice(user_agent_list)
                headers = {'User-Agent': user_agent}
                page = requests.get(url,headers=headers)
                soup = BeautifulSoup(page.content, "html.parser") #parsing the request
                elementScript=soup.find("script",{"id":"__NEXT_DATA__"})
                if elementScript==None:
                    continue
                else:
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
                    Newdf=pd.DataFrame([general_info+stringL+price+segmentation+location+[url]],columns=dataColumns)
                    df=pd.concat([df,Newdf],axis=0)

            except:
                print(f'information fron {url} could not be retrieved')
                continue
        return df
    else:
         print("Error: Links not found")
         
def inputNumber(message):
  while True:
    try:
       userInput = int(input(message))       
    except ValueError:
       print("invalid page number! Try again.")
       continue
    else:
       return userInput 
       break 
#Options for chromedriver configurations
options = Options()
options.headless = True
options.add_argument("--window-size=12,1200")
initialPage=input('Enter web page url:')
page_number=inputNumber('Enter number of pages to scrap:')
webLinks=[]
# Change chromedriver path to your own
driver = webdriver.Chrome(options=options, executable_path=r'C:\PythonScripts\chromedriver.exe')
for n in range(1,page_number+1):
    print(f'extracting links from page {n}...' )
    # Copy and Paste principal page url
    driver.get(initialPage+r'?pagina='+str(n))
    lnks=driver.find_elements_by_tag_name("a")
    # traverse list
    for lnk in lnks[1:-16]:
        # get_attribute() to get all href
        webLinks.append(lnk.get_attribute('href'))
print('links extracted')
driver.quit()

file_dir = os.path.dirname((os.path.abspath(__file__)))
columnsList=['Titulo','Ubicación','Ciudad','Código',
           'Dirección','Descripción','Área','Precio',
           'PrecioM2','estrato','Tipo de Cliente', 'teléfono',
           'nombre_cliente','apellido_cliente','latitud','longitud',
           'link']

df=retrieveInfo(webLinks,columnsList)
print('creating data file...')
time_now=datetime.datetime.now()
file_name=time_now.strftime("%d-%m-%y_%H%M%S")
file_path = os.path.join(file_dir, f'FincaRaiz_{file_name}.xlsx')
df.to_excel(file_path, header=True, index=False)
print('--------FINISHED-------')