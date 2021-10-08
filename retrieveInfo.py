import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def retrieveInfo(linksList):
    if linksList:
        df=pd.DataFrame()
        print('retrieving information... please wait')
        for url in webLinks:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser") #parsing the request
            elementScript=soup.find("script",{"id":"__NEXT_DATA__"})
            if elementScript==None:
                continue
            else:
                data=json.loads(elementScript.text)
                # retrieve information
                general_info=list(data['query'].values())
                props=data['props']['pageProps']
                
                stringL=[props['address'],
                        props['description']
                           ]
                segmentation=[
                        props['segmentation']['estrato'],
                        props['segmentation']['tipo_cliente'],
                        props['contact']['phones']['call'],
                        props['client']['firstName'],
                        props['client']['lastName']
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
                Newdf=pd.DataFrame([general_info+stringL+price+segmentation+location+[url]],columns=columnsList)
                df=pd.concat([df,Newdf],axis=0)

        return df
    else:
         print("Error: Links not found")
         
