# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 17:09:22 2021

@author: ASUS
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = False
options.add_argument("--window-size=12,1200")
# options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options, executable_path=r'.\chromedriver.exe')
driver.maximize_window()

driver.get("https://www.cepedaycia.com/inmueble/?Inmueble=4310")
lnks=driver.find_elements_by_xpath("/html/body/div/div[1]/div[2]/div/div/div/script[5]")

driver.quit()
