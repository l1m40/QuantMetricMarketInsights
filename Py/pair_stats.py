

import numpy as np
import pandas as pd
import logging
from Py import price_stats
from statsmodels.tsa.stattools import adfuller
from statsmodels.formula.api import ols 


# cointegration variables from pairs ###########################################
def cointegration_stats(df,date_input,period): 
  """
  Calculate cointegration method variables like 
  stationary p_value, half_life, residuals

  Args:
      df (DataFrame): .

  Returns:
      DataFrame containing .
      
  Sample input:
date_input = "2023-10-04"
period = 160
df = price_stats.cache_price_data_path(["VALE3","PETR4"],price_stats.price_data_dir+"cache_data_extract1.csv")
df["Close"] = df["Adj Close"]
  """
  df = pd.merge(df.query("Asset == '"+df["Asset"].unique()[0]+"'"),df.query("Asset == '"+df["Asset"].unique()[1]+"'"),on="Date",how="inner")[["Date","Asset_y","Close_y","Asset_x","Close_x"]]
  if not (pd.isna(date_input)):
    df = df.query("Date <= '"+date_input+"'").reset_index(level=0, drop=False)
  df = df.sort_values(by="Date").reset_index(level=0, drop=False)
  return_df = pd.DataFrame()
  for x in range(period-1, len(df.index)):
    df2 = df.loc[(df["index"]<=x) & (df["index"]>(x-period))]
    lm = ols("Close_y ~ Close_x",data=df2).fit()
    p_value=adfuller(lm.resid,regression="ct",maxlag=round(period**(1/3)),autolag=None)[1]
    
    df2 = df2.loc[(df2["index"]==df2.index.max())].reset_index(level=0, drop=True)[["Date","Asset_y","Close_y","Asset_x","Close_x"]]
    df2["period"] = period
    df2["stationary"] = (p_value<0.1)
    df2["p_value"] = p_value
    
    return_df = pd.concat([return_df, df2], ignore_index=True).reset_index(level=0, drop=True)
  
  return return_df


# end ##########################################################################


"""




import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
#import statsmodels.api as sm 
from statsmodels.formula.api import ols 


df_y=price_stats.download_yfinance(["PETR3"],"2023-10-01")
df_x=price_stats.download_yfinance(["PETR4"],"2023-10-01")

df = pd.DataFrame()
df["Y"] = df_y["Adj Close"]
df["X"] = df_x["Adj Close"]


date_input = "2023-10-04"
period = 160
cache_prices = price_stats.cache_price_data_path(["VALE3","PETR4"],price_stats.price_data_dir+"cache_data_extract1.csv")
cache_prices["Close"] = cache_prices["Adj Close"]

df = pd.merge(cache_prices.query("Asset == 'PETR4'"),cache_prices.query("Asset == 'VALE3'"),on="Date",how="inner")[["Date","Close_y","Close_x"]]
df = df.query("Date <= '"+date_input+"'").tail(period).reset_index(level=0, drop=True)

lm = ols("Close_y ~ Close_x",data=df).fit()
lm.summary()
lm.resid.plot()
plt.show()
plt.clf()

np.corrcoef(df["Close_x"], df["Close_y"])

adfuller(lm.resid,regression="ct",maxlag=round(period**(1/3)),autolag=None)[1]


result
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
for key, value in result[4].items():
 print('\t%s: %.3f' % (key, value))

adfuller()

"""
