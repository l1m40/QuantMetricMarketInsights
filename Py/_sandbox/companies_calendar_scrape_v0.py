
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
import re
import os


os.chdir("working_directory")

chrome_options = Options()
chrome_options.add_argument("--headless")  # Uncomment this line if you want to run headless
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chromedriver_path = 'change-to-the-path-of-your-driver'

# Create a new instance of the Chrome driver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)


filename="data/calendar_of_events.csv"








########







########

########







########


def before_get_event(url): 
  print(colors.CYAN,"Navigate to "+colors.DARKCYAN+url+colors.END)

def after_data_transformation_event(df):
  if not df_healthcheck:
    return
  if len(df)>8:
    successful_message(str(len(df))+" Events found")
  else:
    warning_message(str(len(df))+" Events found")
  
  company_calendar_df = pd.read_csv(filename)
  company_calendar_df["Date"]=pd.to_datetime(company_calendar_df["Date"])
  company_calendar_df = pd.merge(df,company_calendar_df,on=["Asset","Date","Event","Important"],how="outer")
  company_calendar_df.to_csv(filename, index=False)
  successful_message("Saved to file!")
  # successful_message("great!")
  # warning_message("great!")
  # error_message("great!")

def df_healthcheck(df):
    columns = ["Asset", "Date", "Event", "Important"]
    missing_columns = [col for col in columns if col not in df.columns]
    if missing_columns:
        error_message("The following columns are missing from df:", missing_columns)
        return False
    else:
        return True

def successful_message(msg):
  print(colors.GREEN+msg+colors.END)
def warning_message(msg):
  print(colors.YELLOW+msg+colors.END)
def error_message(msg):
  print(colors.RED+msg+colors.END)
class colors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'




########







########

########







########






url = "https://ri.3rpetroleum.com.br/en/servicos-aos-investidores/calendar-of-events/"
########
before_get_event(url)
########
driver.get(url)
time.sleep(5)
soup = BeautifulSoup(driver.page_source, 'html.parser')
table = soup.find('table', {'id': 'eventos-futuros'})
rows = table.find_all('tr')
table_data = []
for row in rows:
    cells = row.find_all('td')
    row_data = [cell.text.strip() for cell in cells]
    table_data.append(row_data)

df = pd.DataFrame(table_data, columns=["Date", "Event", "Details", "Export"])

df["Asset"]="RRRP3"
df["Date"]=pd.to_datetime(df["Date"],format="%m/%d/%Y")
df["Important"]=df["Event"].str.contains("Earnings release")
df = df.dropna(subset=["Date"])
df = df[["Asset","Date","Event","Important"]]
########
after_data_transformation_event(df)
########











url = "https://ri.cielo.com.br/servicos-ri/calendario-de-eventos/"
########
before_get_event(url)
########
driver.get(url)
time.sleep(5)
soup = BeautifulSoup(driver.page_source, 'html.parser')
table = soup.find('table', {'id': 'eventos-futuros'})
rows = table.find_all('tr')
table_data = []
for row in rows:
    cells = row.find_all('td')
    row_data = [cell.text.strip() for cell in cells]
    table_data.append(row_data)

df = pd.DataFrame(table_data, columns=["Date", "Event", "Details", "Export"])
df["Asset"]="CIEL3"
df["Date"]=pd.to_datetime(df["Date"],format="%d/%m/%Y",errors='coerce')
df = df[df['Date'].notna()]
df["Important"]=df["Event"].str.contains("Divulgação de resultados")
df = df[["Asset","Date","Event","Important"]]
########
after_data_transformation_event(df)
########







url = "https://www.investidorpetrobras.com.br/apresentacoes-relatorios-e-eventos/eventos/"
########
before_get_event(url)
########
driver.get(url)
time.sleep(5)
soup = BeautifulSoup(driver.page_source, 'html.parser')
table = soup.find('div', {'id': 'eventos-futuros'})
text_divs = table.find_all('div', class_='text')
titles = []
dates = []
for div in text_divs:
    title = div.find('div', class_='title').text.strip()
    date = div.find('span', class_='date').text.strip()
    titles.append(title)
    dates.append(date)

df = pd.DataFrame({'Asset': "PETR4", 'Date': dates, 'Event': titles})
df["Date"]=df["Date"].str.split(", ").str[1]
month_mapping = {
    'janeiro': '01', 'fevereiro': '02', 'março': '03', 'abril': '04',
    'maio': '05', 'junho': '06', 'julho': '07', 'agosto': '08',
    'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12'
}
for month, num in month_mapping.items():
    df['Date'] = df['Date'].str.replace(month, num)
df["Date"]=pd.to_datetime(df["Date"],format="%d de %m de %Y")
df["Important"]=df["Event"].str.contains("Divulgação do Resultado")
########
after_data_transformation_event(df)
########






url = "https://ri.prio3.com.br/servicos-aos-investidores/calendario-de-eventos/"
########
before_get_event(url)
########
driver.get(url)
time.sleep(5)
soup = BeautifulSoup(driver.page_source, 'html.parser')
table = soup.find('table', {'id': 'eventos-futuros'})
rows = table.find_all('tr')
table_data = []
for row in rows:
    cells = row.find_all('td')
    row_data = [cell.text.strip() for cell in cells]
    table_data.append(row_data)

df = pd.DataFrame(table_data, columns=["Date", "Event", "Details"])
df["Asset"]="PRIO3"
df["Date"]=pd.to_datetime(df["Date"],format="%d/%m/%Y")
df["Important"]=df["Event"].str.contains("Release")
df = df[["Asset","Date","Event","Important"]]
########
after_data_transformation_event(df)
########








url = "https://vale.com/pt/informacoes-para-o-mercado"
########
before_get_event(url)
########
driver.get(url)
time.sleep(5)
soup = BeautifulSoup(driver.page_source, 'html.parser')
div_elements = soup.select('#events > div > div:nth-of-type(1) > div')
data = [div.get_text(strip=True) for div in div_elements]
date_pattern = r'\d{2}/\d{2}/\d{4}' # Define a regular expression pattern for dates in the format dd/mm/yyyy
dates = [re.findall(date_pattern, string) for string in data]
dates = [date for sublist in dates for date in sublist]
data_with_separator = [re.sub(date_pattern, ';;;', string) for string in data]
split_data = [string.split(';;;') for string in data_with_separator]
split_data_cleaned = [item[1:] for item in split_data]
split_data_flat = [item for sublist in split_data_cleaned for item in sublist]
df = pd.DataFrame({'Date': dates, 'Event': split_data_flat})
df["Asset"]="VALE3"
df["Date"]=pd.to_datetime(df["Date"],format="%d/%m/%Y")
df["Important"]=df["Event"].str.contains("Informações Trimestrais")
df = df[["Asset","Date","Event","Important"]]
########
after_data_transformation_event(df)
########





url = "https://ri.rdsaude.com.br/"
########
before_get_event(url)
########
driver.set_page_load_timeout(10)
driver.get(url)
time.sleep(5)
soup = BeautifulSoup(driver.page_source, 'html.parser')
div_elements = soup.select('#maincontent > div > div > section:nth-of-type(2) > div > div')
data = [div.get_text(strip=True) for div in div_elements]
months = "jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez"
months_list = months.split("|")
pattern = r'\d{2}(?:'+months+')'
matches = re.findall(pattern, data[0])
formatted_matches = []
for match in matches:
    formatted_matches.append(match[:2]+"/"+str('{:02d}'.format(months_list.index(match[2:]) + 1))+"/"+str(datetime.datetime.now().year))
data_with_separator = re.sub(pattern,';;;',data[0])
text_data = data_with_separator.split(';;;')
df = pd.DataFrame({'Date': formatted_matches, 'Event': text_data[1:]})
df["Asset"]="RADL3"
df["Date"]=pd.to_datetime(df["Date"],format="%d/%m/%Y")
df["Important"]=df["Event"].str.contains("Divulgação Resultados")
df = df[["Asset","Date","Event","Important"]]
########
after_data_transformation_event(df)
########







# Close the browser
driver.quit()
successful_message("driver.quit()")


