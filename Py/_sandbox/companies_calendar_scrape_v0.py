
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

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










url = "https://ri.3rpetroleum.com.br/en/servicos-aos-investidores/calendar-of-events/"
print("Navigate to",url)
driver.get(url)
time.sleep(5)
soup = BeautifulSoup(driver.page_source, 'html.parser')
table = soup.find('table', {'id': 'eventos-futuros'})
rows = table.find_all('tr')
table_data = []
print(len(rows),"Events found")
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

company_calendar_df = pd.read_csv(filename)
company_calendar_df["Date"]=pd.to_datetime(company_calendar_df["Date"])
company_calendar_df = pd.merge(df,company_calendar_df,on=["Asset","Date","Event","Important"],how="outer")
company_calendar_df.to_csv(filename, index=False)
print("Saved to file!")







url = "https://www.investidorpetrobras.com.br/apresentacoes-relatorios-e-eventos/eventos/"
print("Navigate to",url)
driver.get(url)
time.sleep(5)
soup = BeautifulSoup(driver.page_source, 'html.parser')
table = soup.find('div', {'id': 'eventos-futuros'})
text_divs = table.find_all('div', class_='text')
titles = []
dates = []
print(len(text_divs),"Events found")
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

company_calendar_df = pd.read_csv(filename)
company_calendar_df["Date"]=pd.to_datetime(company_calendar_df["Date"])
company_calendar_df = pd.merge(df,company_calendar_df,on=["Asset","Date","Event","Important"],how="outer")
company_calendar_df.to_csv(filename, index=False)
print("Saved to file!")






url = "https://ri.prio3.com.br/servicos-aos-investidores/calendario-de-eventos/"
print("Navigate to",url)
driver.get(url)
time.sleep(5)
soup = BeautifulSoup(driver.page_source, 'html.parser')
table = soup.find('table', {'id': 'eventos-futuros'})
rows = table.find_all('tr')
table_data = []
print(len(rows),"Events found")
for row in rows:
    cells = row.find_all('td')
    row_data = [cell.text.strip() for cell in cells]
    table_data.append(row_data)

df = pd.DataFrame(table_data, columns=["Date", "Event", "Details"])
df["Asset"]="PRIO3"
df["Date"]=pd.to_datetime(df["Date"],format="%d/%m/%Y")
df["Important"]=df["Event"].str.contains("Release")
df = df[["Asset","Date","Event","Important"]]

company_calendar_df = pd.read_csv(filename)
company_calendar_df["Date"]=pd.to_datetime(company_calendar_df["Date"])
company_calendar_df = pd.merge(df,company_calendar_df,on=["Asset","Date","Event","Important"],how="outer")
company_calendar_df.to_csv(filename, index=False)
print("Saved to file!")










# Close the browser
driver.quit()
print("driver.quit()")

