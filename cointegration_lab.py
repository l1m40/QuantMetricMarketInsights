


import price_stats
price_stats.price_data_dir="/home/data_lake_dir/"
#init()

df=price_stats.download_yfinance(["VALE3"],"2023-10-01",True)
df.loc[df["Asset"]=="VALE3"]

df=price_stats.cache_price_yfinance(["USIM5"])

df=price_stats.cache_price_data("")
df.info()
df=price_stats.cache_price_data_path(["VALE3"],price_stats.price_data_dir+"cache_price_data.csv")
