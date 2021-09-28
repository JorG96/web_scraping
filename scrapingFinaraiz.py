from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from collections import defaultdict

import requests
from bs4 import BeautifulSoup
 
import pandas as pd

#Options for chromedriver configurations
options = Options()
options.headless = True
options.add_argument("--window-size=12,1200")

# Change chromedriver path to your own
driver = webdriver.Chrome(options=options, executable_path=r'E:\Documentos\PythonScripts\chromedriver.exe')
# Copy and Paste principal page url
driver.get("https://fincaraiz.com.co/habitaciones/venta?pagina=1")
lnks=driver.find_elements_by_tag_name("a")
webLinks=[]
# traverse list
for lnk in lnks[1:-15]:
    # get_attribute() to get all href
    webLinks.append(lnk.get_attribute('href'))

driver.quit()

# def retrieveInfo(WLinks):
#     infoLocal=defaultdict(list)
#     if WLinks:
#         for link in WLinks:
#             infoLink=[]
#             URL = link
#             page = requests.get(URL)
            
#             soup = BeautifulSoup(page.content, "html.parser")
#             results=soup.find_all("p")
            
#             for i,e in enumerate(results[1:5]+results[7:-4]):
#                 infoLink.append(f'{i}: {e.text.strip()}')
#             infoLocal[link]=infoLink
#         return infoLocal
#     else:
#         print("Error: Links not found")

# retrieveInfo(webLinks)