
# scripts on github done!
# how to update url with with token
# git remote set-url origin https://oho_Ah8EPD1RrN9o8E7W7KvpldWtk2QF830xYmHI@github.com/l1m40/QuantMetricMarketInsights

#
# import price_stats
#


import numpy as np
import pandas as pd
import datetime
import os
import logging

if not ('price_data_dir' in globals()):
  print("variable price_data_dir must have a directory path")

# def log_message(msg,lvl):
#   prefix_level = {
#     0: "",
#     1: "success",
#     2: "warning",
#     3: "ERROR",
#   }
#   prefix="["+prefix_level.get(lvl,"#N/D")+"] "#np.where(lvl==3,"ERROR","#N/D")[0]#"["+np.where(lvl==0,"",np.where(lvl==1,"success",np.where(lvl==2,"warning",np.where(lvl==3,"ERROR","#N/D"))))+"]"
#   print(prefix+msg)
#   return
  
# cache from yahoo #############################################################
# yf.Tickers
# yf.download
# yf.pandas_datareader
#
#tickers = yf.Tickers(["VALE3.SA","BBAS3.SA","BOVA11.SA"])
#data = tickers.download()
# ^^ returns dataframe
#
def asset_yahoo_mask(asset):
  # if Brazil set suffix
  return asset+".SA"

def download_yfinance(tickers,date,progress_input=True): # tickers=["VALE3","BBAS3","BOVA11"] date = "2023-09-21" progress_input= True
  """
  Download historical stock data from Yahoo Finance for the given tickers and date.

  Args:
      tickers (list): List of stock tickers.
      date (str): End date for data retrieval in the "YYYY-MM-DD" format.
      progress_input (bool): Whether to display progress during download.

  Returns:
      DataFrame containing historical stock data.
  """
  import yfinance as yf 
  return_df=pd.DataFrame()
  for t in tickers:
    asset_yahoo=asset_yahoo_mask(t)
    df=yf.download(asset_yahoo, start=pd.Timestamp(date) - datetime.timedelta(days=500), end=date, progress=progress_input)
    #df["Asset Yahoo"]=asset_yahoo
    df["Asset"]=t#df["Asset Yahoo"].str.replace('.SA','')
    return_df = pd.concat([df,return_df])
  #return_df.info()
  #return_df.describe()
  return return_df

def cache_price_data_filename():
  return price_data_dir+"cache_price_data.csv"

def cache_price_data(tickers):
  return cache_price_data_path(tickers,cache_price_data_filename())

def cache_price_data_path(tickers,cache_filename): # cache_filename = cache_price_data_filename()
  """
  Load cached price data from a CSV file.

  Args:
      tickers (list): List of stock tickers to filter data.
      cache_filename (str): Path to the cache data file.

  Returns:
      DataFrame containing cached price data.
  """
  if(not os.path.isfile(cache_filename)):
    #log_message("cache price data file does not exists "+cache_filename,3)
    logging.error(f"Cache price data file does not exist: {cache_filename}")
    return pd.DataFrame()
  
  fileupd=datetime.datetime.fromtimestamp(os.path.getmtime(cache_filename))
  if((datetime.datetime.now()-fileupd).days>5):
    #log_message("cache price data file last updated on "+fileupd.strftime("%Y-%m-%d %H:%M:%S"),2)
    logging.warning(f"Cache price data file last updated on {fileupd.strftime('%Y-%m-%d %H:%M:%S')}")
  df=pd.read_csv(cache_filename)
  #df.info()
  #df.describe()
  # health data check TO-DO
  if(len(tickers)!=0):
    df=df.loc[df.Asset.isin(tickers)]
  return df
  
def cache_price_yfinance(tickers,force_update=False,progress_input=True): # force_update=False
  df=pd.DataFrame()
  if((os.path.isfile(cache_price_data_filename())) & (not force_update)):
    fileupd=datetime.datetime.fromtimestamp(os.path.getmtime(cache_price_data_filename))
    if((datetime.datetime.now()-fileupd).days<1): # do not load from cache if "outdated"
      df=cache_price_data("")
  
  #  TO-DO
  
  
  
  df=download_yfinance(tickers,datetime.date.today(),progress_input)
  
  #pd.DataFrame.to_csv(df,price_data_dir+"cache_price_data.csv")
  
  return df
  


#cached price statistics storage

# math indicators derived from price and volume




