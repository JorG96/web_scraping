# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 15:38:27 2021

@author: ASUS
"""
# Cleaning
import pandas as pd

df=pd.read_excel('dataframe.xlsx', index_col=None, header=0)
iList=[]
for column in df:
    wordIndex=df.index[df[column]=="Ubicación"].tolist()
    if wordIndex:
        iList.append(wordIndex)
        df.iloc[wordIndex[0]:,]=None

df = df.dropna(how='all')