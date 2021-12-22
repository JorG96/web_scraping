# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 10:08:27 2021

@author: ASUS
"""
import os
import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import datetime
import time
import random

user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

dataFields=['id','ciudad','dirección','tipo_Transaccion','antiguedad','superficie','precio_arriendo','precio_venta',
            'precio_administracion','latitud','longitud','url'
    ]

def navigate(initialPage,page_number=2):
    links=[]
    options = Options()
    options.headless = False
    driver = webdriver.Chrome(options=options, executable_path=r'.\chromedriver.exe')
    driver.fullscreen_window()
    driver.minimize_window()
    driver.get(initialPage)
    n=1
    while n<page_number:
        n+=1
        driver.implicitly_wait(2)
        next_button=driver.find_elements_by_xpath('/html/body/app-root/app-resultview/div/div/div[1]/div[2]/div/div[1]/div/div[3]/ul/li/a/span')
        next_button[-1].click()
        time.sleep(1.6)    
        
    container=driver.find_elements_by_xpath("/html/head/link")
    for elem in container:
        try:
            links.append(elem.get_attribute('href'))
        except:
            print("element not found")
    driver.quit()
    return list(set(links[13:]))

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

def extractInfo(lnks,dataColumns):
    df=pd.DataFrame()
    if lnks:
        for url in lnks:
            sleep_time=random.uniform(1.1, 1.5)
            time.sleep(sleep_time)
            #Pick a random user agent
            user_agent= random.choice(user_agent_list)
            #Set the headers 
            headers = {'User-Agent': user_agent}
            #Make the request
            try:
                response = requests.get(url,headers=headers)
            except requests.exceptions.RequestException as e:
                # A serious problem happened, like an SSLError or InvalidURL
                print(f"Error: {e}")
                continue
            soup = BeautifulSoup(response.content, "html.parser") #parsing the request
            elementScript=soup.find("script",{"id":"ciencuadras-state"})

            if elementScript==None:
                continue
            else:
                print(f'retrieving information from {url}... please wait')
                data=json.loads(elementScript.text.replace('&q;','"'))                
                
                
                try:
                    props=data['dataKey']
                    info=[
                        props['id'],
                        props['cityname'],
                        props['address'],
                        props['transactiontype'],
                        props['propertyFeatures']['antiquity'],
                        props['propertyFeatures']['builtArea']
                        ]
                    
                    price=[
                        props['stratification'][0]['leasefee'],
                        props['stratification'][0]['sellingprice'],
                        props['stratification'][0]['administrationvalue'],
                        ]
                
                    location=[
                    props['latitude'],
                    props['longitude'],
                            ]
                except:
                    pass
                    print(f"Failed to retreive info from {url}")

                Newdf=pd.DataFrame([info+price+location+[url]],columns=dataColumns)
                df=pd.concat([df,Newdf],axis=0)
        return df
    else:
        print('No links found')

file_dir = os.path.dirname((os.path.abspath(__file__)))
init_Page=input('Enter web page url:')
page_number= inputNumber('Enter number of pages to scrap:')
urls= navigate(init_Page,page_number)
df=extractInfo(urls,dataFields)
print('creating data file...')
actual_time=datetime.datetime.now()
file_name=actual_time.strftime("%d-%m-%y_%H%M%S")
file_path = os.path.join(file_dir, f'ciencuadras_{file_name}.xlsx')
df.to_excel(file_path, header=True, index=False)
print('--------SCRAP FINISHED-------')
