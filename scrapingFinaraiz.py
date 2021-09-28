from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

 



options = Options()
options.headless = True
options.add_argument("--window-size=12,1200")

driver = webdriver.Chrome(options=options, executable_path=r'E:\Documentos\PythonScripts\chromedriver.exe')
driver.get("https://fincaraiz.com.co/locales/arriendos?pagina=1")
lnks=driver.find_elements_by_tag_name("a")
webLinks=[]
# traverse list
for lnk in lnks[1:-15]:
    # get_attribute() to get all href
    webLinks.append(lnk.get_attribute('href'))

driver.quit()

