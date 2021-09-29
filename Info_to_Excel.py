# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 10:57:44 2021

@author: ASUS
"""
import os
import pandas as pd

#File directory
file_dir = os.path.dirname(os.path.abspath(__file__))

import requests
from bs4 import BeautifulSoup

WebLinks=['https://www.fincaraiz.com.co/inmueble/local-en-arriendo/cota/cota/4985991']

#Retrieve information using the list of links provided
def retrieveInfo(WLinks):
    df=pd.DataFrame()
    if WLinks:
        for link in WLinks:
            infoLink=[]
            URL = link
            page = requests.get(URL)
            
            soup = BeautifulSoup(page.content, "html.parser") #parsing the request
            results=soup.find_all("p") #find the coincident tags
            
            #Extract text from each element found and return the information as pandas dataframe.
            for i,e in enumerate(results[0:7]+results[7:-8]):
                txt=e.text.strip()
                if "potestativo" in txt:
                    break
                infoLink.append(txt)
            newSeries=pd.Series(infoLink,name=link)
            df=pd.concat([df,newSeries],axis=1)
        return df
    else:
        print("Error: Links not found")

#Copy the information to a xlsx file extension.
df=retrieveInfo(WebLinks)
file_path = os.path.join(file_dir, 'dataframe.xlsx')
df.to_excel(file_path, header=True, index=False)