# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 10:08:12 2021

@author: ASUS
"""
import requests
from lxml.html import fromstring
from itertools import cycle


def get_proxies():
  url = 'https://free-proxy-list.net/'
  response = requests.get(url)
  parser = fromstring(response.text)
  proxies = set()
  for i in parser.xpath('//tbody/tr')[:100]:
    if i.xpath('.//td[7][contains(text(),"yes")]'):
      #Grabbing IP and corresponding PORT
      proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
      proxies.add(proxy)
  return proxies
proxies=get_proxies()
proxy_pool = cycle(proxies)

url = 'https://ipecho.net/plain'
for i in range(1,10):
  #Get a proxy from the pool
  proxy = next(proxy_pool)
  print("Request #%d"%i)
  
  try:
    response = requests.get(url,proxies={"http": proxy, "https": proxy})
    print(response.json())
  except:
    #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
    #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url 
    print("Skipping. Connnection error")