

# import subprocess
# # Specify the Python script you want to execute
# script_to_execute = "price_stats.py"
# # Run the script using the subprocess module
# subprocess.run(["python", script_to_execute])

import price_stats
price_stats.price_data_dir="/Users/marcoslima/Zion/"
#init()

df=price_stats.download_yfinance(["VALE3"],"2023-10-01",True)
df.loc[df["Asset"]=="VALE3"]

df=price_stats.cache_price_yfinance(["VALE3"],"2023-10-01")

df=price_stats.cache_price_data(["VALE3"])

df=price_stats.cache_price_data_path(["VALE3"],price_stats.price_data_dir+"cache_price_data.csv")
