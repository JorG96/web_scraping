#!python
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 13:27:47 2021

@author: ASUS
"""


import os
import datetime
import requests
import random
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

dataColumns=['IDpropiedad','estado','mercado','estrato','telefono',
             'barrio','tipo de negocio','descripción',
             'antiguedad','ciudad','area construida',
             'precio de renta', 'precio de venta','latitud',
             'longitud','area privada','url']

def retrieveInfo(links,columns):
    df=pd.DataFrame()
    if links:
        for url in urls:
            propertyId,info,price,location=[None],[None]*9,[None]*4,[None]*2
            sleep_time=random.uniform(1.1, 1.8)
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
            soup = BeautifulSoup(response.content, "html.parser") #parsing the request
            elementScript=soup.find("script",{"id":"__NEXT_DATA__"})

            if elementScript==None:
                continue
            else:
                print(f'retrieving information from {url}... please wait')
                data=json.loads(elementScript.text)
                props=data['props']['initialState']['realestate']['basic']
                
            
                
            try:
                propertyId=[props['propertyId']]

                info=[
                props['propertyState'],
                props['breadcrumb']['links'][0]['text'],
                props['stratum'],
                props['contactPhone'],
                props['neighborhood'],
                props['businessType'],
                props['comment'],
                props['builtTime'],
                props['city']['nombre']
                    ]
                
                price=[
                props['area'],
                props['areac'],
                props['salePrice'],
                props['rentPrice'],
                    ]
            
                location=[
                props['coordinates']['lat'],
                props['coordinates']['lon'],
                        ]
            except:
                pass
                print(f"Failed to retreive info from {url}")

            Newdf=pd.DataFrame([propertyId+info+price+location+[url]],columns=dataColumns)
            df=pd.concat([df,Newdf],axis=0)
        return df
    else:
        print('No links found')
         
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

def automateNav(initialPage,page_number=1):
    webLinks=[]
    options = Options()
    options.headless = False
    options.add_argument("--window-size=12,1200")
    # options.add_argument('start-maximized')
    driver = webdriver.Chrome(options=options, executable_path=r'.\chromedriver.exe')
    driver.maximize_window()
    driver.get(initialPage)
    n=1
    while n<=page_number:
        driver.implicitly_wait(2)
        print("extracting links from page: "+str(n))
        # traverse list
            # Copy and Paste principal page url
        container=driver.find_elements_by_xpath("/html/body/div[2]/div/div/div[2]/div[2]/div[2]/div[2]/ul[1]/li/div/ul/li[1]/a")
        # traverse list
        for lnk in container:
            # get_attribute() to get all href
            webLinks.append(lnk.get_attribute('href'))
        if n<3:
            next_button=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[2]/div[2]/ul[2]/li[12]/a')
        else:
            next_button=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[2]/div[2]/ul[2]/li[12]/a')
    
        driver.execute_script("arguments[0].scrollIntoView();",next_button)
        next_button.click()
        print('please wait...')
        
        n+=1
    
    driver.quit()
    return webLinks

file_dir = os.path.dirname((os.path.abspath(__file__)))
init_Page=input('Enter web page url:')
page_number= inputNumber('Enter number of pages to scrap:')
urls= automateNav(init_Page,page_number)
df=retrieveInfo(urls,dataColumns)
print('creating data file...')
actual_time=datetime.datetime.now()
file_name=actual_time.strftime("%d-%m-%y_%H%M%S")
file_path = os.path.join(file_dir, f'{file_name}.xlsx')
df.to_excel(file_path, header=True, index=False)
print('--------SCRAP FINISHED-------')