import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import re 
import itertools

ID_Sell = [] 
Sales_Sate = [] 
Real_State = []
Department = []
Municipality = []
Zone = []
Stratum = [] 
Longitude = [] 
Latitude = []
Area_m2 = [] 
Price = [] 
m2_price = [] 
Admin_Cost = [] 
Age_range = [] 
Total_Rooms = [] 
Baths = [] 
Garages = [] 
Floor = []
First_Edit = []
Last_Edit = []

html = requests.get("https://fincaraiz.com.co/apartamentos/proyectos-vivienda-nueva")
soup = BeautifulSoup(html.content, 'html.parser')

print(re.findall('https*', str(html))[0])


# prefix = 'https://www.fincaraiz.com.co/apartamento-casa/venta/bogota/?ad=30|'
# sufix = '||||1||8,9|||67|3630001||||||||||||||||1|||1||griddate%20desc||||||'
# pagelinks = []
# for i in [x for x in range(0,1)]:
#     try:
#         pagelinks.append(prefix + str(i) + sufix)
#     except:
#         pagelinks.append(None)
        
# def weblinks(pagelink):
#     page = requests.get(pagelink.format(i))
#     soup = BeautifulSoup(page.content, 'html.parser')
#     div_container = soup.findAll('div',{'class': 'span-title'})
#     weblinks = ['https://www.fincaraiz.com.co' + n for n in re.findall('href=\"(.+?)\"', str(div_container))]
#     return weblinks

# weblinks = list(map(weblinks,pagelinks))
# weblinks = list(itertools.chain.from_iterable(weblinks))