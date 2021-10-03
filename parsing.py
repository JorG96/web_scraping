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

URLs =['https://fincaraiz.com.co/proyecto-de-vivienda/vitra-art-apartamentos/chapinero-central/bogota/6337605', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/concepcion-norte-los-alcazares/bogota/5959950', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/colina-campestre/bogota/6719340', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/conjunto-la-estancia-3/mosquera/6252232', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/mejoras-publicas/bucaramanga/6715905', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/villa-campestre/barranquilla/6716172', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/antiguo-country/bogota/6723302', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/pinar-de-suba/bogota/6725646', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/colina-campestre/bogota/6720172', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/bella-suiza/bogota/6603276', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/centro-internacional/bogota/6711747', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/loma-san-jose/sabaneta/6726216', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/chapinero-alto/bogota/6716001', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/milenta/bogota/6726310', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/santa-barbara-oriental/bogota/6636647', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/chico-navarra/bogota/6723224', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/san-cristobal-norte/bogota/6726582', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/san-martin/bogota/6726032', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/suba-centro/bogota/6498571', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/san-antonio/bogota/6725689', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/calatrava/bogota/6715999', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/pasadena/bogota/6714432', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/villa-santos/puerto-colombia/6365417', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/avenida-libano/santa-marta/6374557', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/nueva-autopista/bogota/6604931', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/bonanza/bogota/6726014', 'https://fincaraiz.com.co/inmueble/apartamento-en-arriendo/reserva-del-lago/cajica/6713909']



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