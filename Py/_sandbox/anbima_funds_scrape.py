
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime
import re 
import os
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException





chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment this line if you want to run headless
chrome_options.add_argument("window-size=1920,1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
chrome_options.add_argument("--disable-gpu")

# Create a new instance of the Chrome driver
# https://googlechromelabs.github.io/chrome-for-testing/
# service = Service(chromedriver_path)
# driver = webdriver.Chrome(service=service, options=chrome_options)

driver = webdriver.Chrome(options=chrome_options)
print("driver = webdriver.Chrome(options=chrome_options)")


# successful_message("Reading Anbima Stock Funds...")
url = "https://data.anbima.com.br/fundos?page=1&size=5&classe_anbima=A%C3%A7%C3%B5es&tipo_anbima=&benchmark="
start_time = time.time()
driver.set_page_load_timeout(30)
driver.get(url)
time.sleep(10)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
list_items = soup.find_all('li', class_='list-item__container')
data = []
# Loop through each <li> element to extract the relevant data
for item in list_items:
    name            = item.find('h2', class_='list-item__title').get_text(strip=True)
    cnpj            = item.find('span', id=lambda x: x and x.startswith('cnpj')).get_text(strip=True)
    company         = item.find('dl', id=lambda x: x and x.startswith('gestor')).find('dd').get_text(strip=True)
    minimum         = item.find('dl', id=lambda x: x and x.startswith('aplicacaoInicialMinima')).find('dd').get_text(strip=True)
    net_worth       = item.find('dl', id=lambda x: x and x.startswith('patrimonioLiquido')).find('dd').get_text(strip=True)
    administrator   = item.find('dl', id=lambda x: x and x.startswith('administrador')).find('dd').get_text(strip=True)
    qualified       = item.find('dl', id=lambda x: x and x.startswith('caracteristicaInvestidor')).find('dd').get_text(strip=True)
    adm_fee         = item.find('dl', id=lambda x: x and x.startswith('taxaAdministracaoMaxima')).find('dd').get_text(strip=True)
    profit          = item.find('dl', id=lambda x: x and x.startswith('rentabilidade')).find('dd').get_text(strip=True)
    # Append the extracted data as a dictionary to the list
    data.append({
        'name': name,
        'cnpj': cnpj,
        'company': company,
        'minimum': minimum,
        'net_worth': net_worth,
        'administrator': administrator,
        'qualified': qualified,
        'adm_fee': adm_fee,
        'profit': profit
    })
# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data)






# Close the browser
driver.quit()
# successful_message("driver.quit()")


