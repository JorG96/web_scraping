import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import random
urls=['https://www.metrocuadrado.com/inmueble/arriendo-oficina-bogota-jardin-botanico-4-garajes/164-M3043326',
      'https://www.metrocuadrado.com/inmueble/venta-local-comercial-chia-terranova/432-1433',
      'https://www.metrocuadrado.com/inmueble/arriendo-bodega-bogota-santa-sofia/3561-M2520215'
           ]
dataColumns=['IDpropiedad','estado','mercado','estrato','telefono',
             'barrio','tipo de negocio','descripción',
             'antiguedad','ciudad','area construida',
             'precio de renta', 'precio de venta','latitud',
             'longitud','area privada','url']
user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

df=pd.DataFrame()
if urls:
    for url in urls:
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
            
            propertyId=[props['propertyId']]
            info,price,location=[None]*9,[None]*4,[None]*2

        try:
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
else:
    print('No links found')
     
