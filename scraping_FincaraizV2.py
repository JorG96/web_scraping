# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 14:21:25 2022

@author: Jorge.Camacho1
"""

import os
import requests
import json
import pandas as pd
import time
import random
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

def inputNumber(message):
  while True:
    try:
       userInput = int(input(message))       
    except ValueError:
       print("invalid page number! Try again.")
       continue
    else:
       return userInput 


def getURL(page_number):
    for n in range(1,page_number+1):
        print(f'extracting links from page {n}...' )
        # Copy and Paste principal page url
        driver.get(initialPage+r'?pagina='+str(n))
        urls=driver.find_elements_by_xpath("/html/body/div/div[1]/div[3]/div/div/div[3]/div/article/a"
                                           )
        with open("./URL.csv",mode="a") as file:
            for url in urls[1:-16]:
            # get_attribute() to get all href
                file.write(url.get_attribute('href'))
                file.write("\n")
    print('links extracted')


def retrieveInfo(linksList,dataColumns):
    if linksList:
        df=pd.DataFrame()
        for url in linksList:
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

def extractInfo(file_path):
    with open(file_path, mode="r") as url_file:
        for url in url_file:
            sleep_time=random.uniform(0.98, 1.35)
            time.sleep(sleep_time)
            print(f'retrieving information from {url}...')
            try:
                #cambiar el User Agent para realizar el request
                user_agent= random.choice(user_agent_list)
                headers = {'User-Agent': user_agent}
                #enviar el request con con los headers configurados
                page = requests.get(url,headers=headers,timeout=4)
                #parsear el contenido html del request
                soup = BeautifulSoup(page.content, "html.parser") 
                elementScript=soup.find("script",{"id":"__NEXT_DATA__"})
                if elementScript==None:
                    continue
                else:
                    with open("./RawData.json",mode="a") as data_file:
                        data_file.write(elementScript.text)
                        data_file.write("\n")
            except:
                print(f'information from {url} could not be extracted')
                continue
        print("information extraction finished")
        
def jsonToCSV(json_file_path):
    Newdf=pd.DataFrame()
    with open(json_file_path, mode="r") as json_file:
        print("transformation started")
        for element in json_file:
            try:
                element_data=json.loads(element)
                if element_data['props']['pageProps']==404:
                    continue
                else:
                    df=pd.json_normalize(element_data['props']['pageProps'])
                    Newdf=pd.concat([Newdf,df],axis=0)
                    
            except:
                print("element couldn't be loaded")
    return Newdf
    
if __name__=='__main__':
#Opciones de configuracion para el driver web
    options = Options()
    options.headless = True
    options.add_argument("--window-size=12,1200")
    initialPage=input('Enter web page url:')
    page_number=inputNumber('Enter number of pages to scrap:')
# ruta de Chromedriver
    driver = webdriver.Chrome(options=options, executable_path=r'C:\PythonScripts\chromedriver.exe')
    # driver.set_page_load_timeout(20)
# Obtener csv con todos los enlaces por inmueble.
    # getURL(page_number)
# Cerrar el driver
    driver.quit()
# Extraer informacion en formato json del codigo fuente.
    # extractInfo(file_path="url2.csv")
    df=jsonToCSV("./RawData.json")
    df.to_csv("./MercadoBogota.csv",index=False)
