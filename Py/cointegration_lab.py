

import numpy as np
import pandas as pd

import market_data
import price_stats
price_stats.price_data_dir="/home/data_lake_dir/"
#init()

import pair_stats

df = price_stats.cache_price_yfinance(["VALE3","PETR4"],True,True)
df["Close"] = df["Adj Close"]
pair_stats.cointegration_stats(df,"2023-10-05",160)


df = price_stats.cache_price_yfinance(market_data.scrape_index_advfn("IBOV")["Asset"],False,True)
df.info()
df.head()



df = price_stats.cache_price_data_path(["VALE3","PETR4"],price_stats.price_data_dir+"cache_data_extract1.csv")
df["Close"] = df["Adj Close"]
df["Close"] = np.log(df["Adj Close"])
pair_stats.cointegration_stats(df,"2023-10-05",160)


pair_stats.cointegration_stats(df,pd.NA,160).query("Date>'2023-01-02'").reset_index(level=0, drop=True)["p_value"].plot()
pair_stats.cointegration_stats(df,pd.NA,190).query("Date>'2023-01-02'").reset_index(level=0, drop=True)["p_value"].plot()
pair_stats.cointegration_stats(df,pd.NA,210).query("Date>'2023-01-02'").reset_index(level=0, drop=True)["p_value"].plot()
pair_stats.cointegration_stats(df,pd.NA,240).query("Date>'2023-01-02'").reset_index(level=0, drop=True)["p_value"].plot()

#cointegration_stats(df,pd.NA,250)["p_value"].plot()
#import matplotlib.pyplot as plt 
plt.show()
plt.clf()





df=price_stats.download_yfinance(["VALE3"],"2023-10-01",True)
df.loc[df["Asset"]=="VALE3"]

df=price_stats.cache_price_yfinance(["USIM5"])

df=price_stats.cache_price_data("")
df.info()
df=price_stats.cache_price_data_path(["VALE3"],price_stats.price_data_dir+"cache_price_data.csv")


df=price_stats.cache_price_data_path(["VALE3","PETR3","PETR4"],price_stats.price_data_dir+"cache_data_extract1.csv")


