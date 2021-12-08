

def parsePrice(price):
    if '$' in price:
        value=price.split('$')
        return value[-1]
    else:
        return price
    
# import requests
# # https://maps.googleapis.com/maps/api/js?&callback=initMap
# # key=AIzaSyBjZ6e9WW8rGdI-ohhh9xw7UEbQ4rVudss
# address="ALTO PRADO BARRANQUILLA"
# response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key=AIzaSyBjZ6e9WW8rGdI-ohhh9xw7UEbQ4rVudss')
# resp_json_payload = response.json()
# print(resp_json_payload['results'][0]['geometry']['location'])
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url="https://www.cepedaycia.com/inmueble/?Inmueble=5919"
options = Options()
options.headless = False
options.add_argument("--window-size=12,1200")
# options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options, executable_path=r'.\chromedriver.exe')
driver.get(url)
location=driver.find_element_by_id("det-title").text
code=driver.find_element_by_id("det-code").text
bed=driver.find_element_by_id("det-nb-bed").text
bath=driver.find_element_by_id("det-nb-bath").text
superficie=driver.find_element_by_id("det-area").text
venta=parsePrice(driver.find_element_by_id("det-venta-price").text)
renta=parsePrice(driver.find_element_by_id("det-arriendo-price").text)
info=[code,location,bed,bath,superficie,venta,renta]
