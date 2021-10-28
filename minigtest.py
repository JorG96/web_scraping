# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 09:06:20 2021

@author: ASUS
"""

import requests
import random
from bs4 import BeautifulSoup
import pandas as pd
import json
import time

user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
dataColumns=['IDpropiedad','estado','estrato','telefono',
             'barrio','tipo de negocio','descripción',
             'antiguedad','area privada','area construida',
             'precio de renta', 'precio de venta','latitud',
             'longitud','ciudad','url']

urls = ['https://www.metrocuadble/arriendo-local-comercial-bogota-veraguas/164-M3120309',
        'https://www.metrocuadm/inmueble/arriendo-oficina-medellin-san-diego-1-banos/10280-M3065213'

        ]

Weblinks=[]

def retrieveInfo(links,columns):
    df=pd.DataFrame()
    if links:
        for url in urls:
            sleep_time=random.uniform(1.1, 2.0)
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
                print("Error: {}".format(e))
                return "Error: {}".format(e)
            soup = BeautifulSoup(response.content, "html.parser") #parsing the request
            
            print('retrieving information... please wait')
            elementScript=soup.find("script",{"id":"__NEXT_DATA__"})
            data=json.loads(elementScript.text)
            props=data['props']['initialState']['realestate']['basic']
            
            propertyId=[props['propertyId']]
            try:
                info=[
                props['propertyState'],
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
                print(f"error retrieving info from {url}")


            Newdf=pd.DataFrame([propertyId+info+price+location+[url]],columns=dataColumns)
            df=pd.concat([df,Newdf],axis=0)
    else:
        print('No links found')
        
retrieveInfo(urls, dataColumns)
print("--------SCRAPING FINISHED-----------")