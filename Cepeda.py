# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 20:09:22 2021

@author: ASUS
"""
import os
import datetime
import random
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


dataColumns=['codigo','ubicacion','habitaciones','baños','superficie','Precio de Venta','Precio de Renta','latitud','longitud','url']

def automateNav(initialPage,page_number=1):
    def retrieveInfo(url):
        driver.get(url)
        print(f'retrieving information from {url}... please wait')
        location=driver.find_element_by_id("det-title").text
        code=driver.find_element_by_id("det-code").text
        bed=driver.find_element_by_id("det-nb-bed").text
        bath=driver.find_element_by_id("det-nb-bath").text
        superficie=driver.find_element_by_id("det-area").text
        venta=parsePrice(driver.find_element_by_id("det-venta-price").text)
        renta=parsePrice(driver.find_element_by_id("det-arriendo-price").text)
        key="API-KEY"
        response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={key}')
        resp_json_payload = response.json()
        lat=resp_json_payload['results'][0]['geometry']['location']['lat']
        long=resp_json_payload['results'][0]['geometry']['location']['lng']
        info=[code,location,bed,bath,superficie,venta,renta,lat,long]

        return info

    webLinks=[]
    options = Options()
    options.headless = False
    options.add_argument("--window-size=12,1200")
    # options.add_argument('start-maximized')
    driver = webdriver.Chrome(options=options, executable_path=r'.\chromedriver.exe')
    driver.minimize_window()
    driver.get(initialPage)
    n=1
    while n<=page_number:
        sleep_time=random.uniform(1.1, 1.8)
        time.sleep(sleep_time)

        driver.implicitly_wait(2)
        print("extracting links from page: "+str(n))
        # traverse list
            # Copy and Paste principal page url
        container=driver.find_elements_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/a")
        # traverse list
        for lnk in container:
            # get_attribute() to get all href
            webLinks.append(lnk.get_attribute('href'))
            next_button=driver.find_element_by_xpath('/html/body/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div/div[2]/div/div/div/ul/li[10]/a')

    
        driver.execute_script("arguments[0].scrollIntoView();",next_button)
        next_button.click()
        print('please wait...')
        
        n+=1
    df=pd.DataFrame()
    for url in webLinks:
        try:
            information=retrieveInfo(url)
        except:
            # A serious problem happened, like an SSLError or InvalidURL
            print(f"Error retrieving information from {url}")
            continue

        Newdf=pd.DataFrame([information+[url]],columns=dataColumns)
        df=pd.concat([df,Newdf],axis=0)
    driver.quit()
    return df

def parsePrice(price):
    if '$' in price:
        value=price.split('$')
        return value[-1]
    else:
        return price
    
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


file_dir = os.path.dirname((os.path.abspath(__file__)))
init_Page=input('Enter web page url:')
page_number= inputNumber('Enter number of pages to scrap:')
df=automateNav(init_Page,page_number)
print('creating data file...')
actual_time=datetime.datetime.now()
file_name=actual_time.strftime("%d-%m-%y_%H%M%S")
file_path = os.path.join(file_dir, f'{file_name}.xlsx')
df.to_excel(file_path, header=True, index=False)
print('--------SCRAP FINISHED-------')