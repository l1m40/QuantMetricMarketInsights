
import numpy as np
import pandas as pd




def scrape_index_advfn(index_str):
  import requests
  from bs4 import BeautifulSoup
  URL=""
  if(index_str=="IBXX"):
    URL="https://br.advfn.com/indice/ibrx"
  elif(index_str=="IBXL"):
    URL="https://br.advfn.com/indice/ibrx-50"
  elif(index_str=="IBOV"):
    URL="https://br.advfn.com/indice/ibovespa"
  else:
    return pd.DataFrame()
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, "html.parser")
  results = soup.find("table",id="id_sl-dax") # find object id using source code on Chrome Developer Tools 
  df = pd.read_html(str(results))[0]
  df["Último"] = pd.to_numeric(df["Último"],errors='coerce')
  df = df.loc[pd.notna(df["Último"])]
  return df[["Ativo"]].rename(columns={"Ativo":"Asset"}).reset_index(level=0, drop=True)

def scrape_b3_wikipedia():
  import requests
  from bs4 import BeautifulSoup
  URL="https://en.wikipedia.org/wiki/List_of_companies_listed_on_B3"
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, "html.parser")
  results = soup.find(id="constituents")
  df = pd.read_html(str(results))[0]
  return df[["Ticker"]].rename(columns={"Ticker":"Asset"}).reset_index(level=0, drop=True)
  
