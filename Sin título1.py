# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 09:09:00 2021

@author: ASUS
"""

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import pandas as pd

import json

options = Options()
options.headless = False
# options.add_argument("--window-size=12,1200")
options.add_argument('start-maximized')
initialPage='https://www.metrocuadrado.com/bodega/arriendo/barranquilla/'
webLinks=[]
# Change chromedriver path to your own
driver = webdriver.Chrome(options=options, executable_path=r'.\chromedriver.exe')
driver.maximize_window()
# Copy and Paste principal page url
driver.get(initialPage)
page_number=2
n=1
while n<=page_number:
    print("extracting links from page: "+str(n))
    # traverse list
        # Copy and Paste principal page url
    container=driver.find_elements_by_xpath("/html/body/div[2]/div/div/div[2]/div[2]/div[2]/div[2]/ul[1]/li/div/ul/li[1]/a")
    # traverse list
    for lnk in container:
        # get_attribute() to get all href
        webLinks.append(lnk.get_attribute('href'))
    next_button=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/div[2]/div[2]/ul[2]/li[12]/a')
    driver.execute_script("arguments[0].scrollIntoView();",next_button)
    next_button.click()
    driver.implicitly_wait(10)
    n+=1


driver.quit()


