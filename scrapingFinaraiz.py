from selenium import webdriver
from selenium.webdriver.chrome.options import Options


#Options for chromedriver configurations
options = Options()
options.headless = True
options.add_argument("--window-size=12,1200")

# Change chromedriver path to your own
driver = webdriver.Chrome(options=options, executable_path=r'E:\Documentos\PythonScripts\chromedriver.exe')
# Copy and Paste principal page url
driver.get("https://www.fincaraiz.com.co/locales/proyectos-vivienda-nueva")
lnks=driver.find_elements_by_tag_name("a")
webLinks=[]
# traverse list
for lnk in lnks[1:-15]:
    # get_attribute() to get all href
    webLinks.append(lnk.get_attribute('href'))

driver.quit()

