# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 13:27:47 2021

@author: ASUS
"""


import os
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

file_dir = os.path.dirname(os.path.abspath(__file__))
indexList=['Titulo','Ubicación','Ciudad','Código',
           'Dirección','Descripción','Área','Precio',
           'PrecioM2','estrato','Tipo de Cliente',
           'latitud','longitud']

URLs = ['https://www.fincaraiz.com.co/inmueble/local-en-arriendo/chapinero-norte/bogota/6703031',
        'https://www.fincaraiz.com.co/proyecto-de-vivienda/vitra-art-apartamentos/chapinero-central/bogota/6337605',
'https://www.fincaraiz.com.co/proyecto-de-vivienda/sorrento/restrepo/bogota/3760694']
        


def retrieveInfo(linksList):
    if linksList:
        df=pd.DataFrame()
        for url in URLs:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser") #parsing the request
            elementScript=soup.find("script",{"id":"__NEXT_DATA__"})
            data=json.loads(elementScript.text)
            # retrieve information
            general_info=list(data['query'].values())
            props=data['props']['pageProps']
            
            stringL=[
                    props['address'],
                    props['description']
                       ]
            segmentation=[
                    props['segmentation']['estrato'],
                    props['segmentation']['tipo_cliente'],
                    
                ]
            price=[
                   props['area'],
                   props['price'],
                   props['priceM2']
                   ]
            location=[
                    props['locations']['lat'],
                    props['locations']['lng']
                    ]
            newSeries=pd.Series(general_info+stringL+price+segmentation+location,name=url,index=indexList)
            df=pd.concat([df,newSeries],axis=1)
        return df
    else:
         print("Error: Links not found")
         
df=retrieveInfo(URLs)
file_path = os.path.join(file_dir, 'dataframe.xlsx')
df.to_excel(file_path, header=True, index=True)