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
import datetime
import time

url="https://www.ciencuadras.com/inmueble/apartamento-en-arriendo-en-la-salle-medellin-2154784"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser") #parsing the request
elementScript=soup.find("script",{"id":"ciencuadras-state"})
data=json.loads(elementScript.text.replace('&q;','"'))
print(data)


ur2="https://www.ciencuadras.com/inmueble/oficina-en-venta-en-mejoras-publicas-bucaramanga-1597024"
page = requests.get(ur2)
soup = BeautifulSoup(page.content, "html.parser") #parsing the request
elementScript=soup.find("script",{"id":"ciencuadras-state"})
data2=json.loads(elementScript.text.replace('&q;','"'))


'''id,cityname,addres,transactiontype,stratification[0][leasefee],stratification[0][sellingprice],stratification[0][administrationvalue],propretyFeatures[builtArea],
propretyFeatures[antiquity],latitude,longitude'''

initialPage="https://www.ciencuadras.com/venta"
links=[]
options = Options()
options.headless = False
options.add_argument("--window-size=12,1200")
driver = webdriver.Chrome(options=options, executable_path=r'.\chromedriver.exe')
driver.maximize_window()
driver.get(initialPage)
n=1
page_number=9
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

