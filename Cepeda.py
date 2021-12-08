# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 17:09:22 2021

@author: ASUS
"""
import requests
from bs4 import BeautifulSoup
import time
import random


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
url="https://www.cepedaycia.com/inmueble/?Inmueble=5919"

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
    
    driver.quit()
    return webLinks

def parsePrice(price):
    if '$' in price:
        value=price.split('$')
        return value[-1]
    else:
        return price


options = Options()
options.headless = False
options.add_argument("--window-size=12,1200")
# options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options, executable_path=r'.\chromedriver.exe')
driver.get(url)
code=driver.find_element_by_id("det-code").text
habitacion=driver.find_element_by_id("det-nb-bed").text
baño=driver.find_element_by_id("det-nb-bath").text
superficie=driver.find_element_by_id("det-area").text
venta=parsePrice(driver.find_element_by_id("det-venta-price").text)
renta=parsePrice(driver.find_element_by_id("det-arriendo-price").text)

driver.quit()