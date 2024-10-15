
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller
import logging

def calculate_massive_adf(price_df, asset_pairs, period=240):
    '''
    Function to calculate the Augmented Dickey-Fuller (ADF) test across multiple asset pairs.

    Args:
        price_df (pd.DataFrame): DataFrame with price series, should have columns ['Date', 'Asset', 'Close'].
        asset_pairs (list): List of tuples where each tuple is a pair of asset names (e.g., [('Asset1', 'Asset2'), ('Asset3', 'Asset4')]).
        period (int): Rolling window length for the ADF test. Default is 240.

    Returns:
        pd.DataFrame: A DataFrame summarizing the ADF results for each pair, including p-value and stationarity.
    '''

    result_df = pd.DataFrame()

    # Iterating through each asset pair
    for asset1, asset2 in asset_pairs:
        logging.info(f"Processing pair: {asset1} and {asset2}")
        
        # Filter data for each asset and merge
        df_asset1 = price_df[price_df['Asset'] == asset1].rename(columns={'Close': 'Close_1'})
        df_asset2 = price_df[price_df['Asset'] == asset2].rename(columns={'Close': 'Close_2'})
        merged_df = pd.merge(df_asset1[['Date', 'Close_1']], df_asset2[['Date', 'Close_2']], on='Date', how='inner')

        # Calculate rolling ADF stats
        for i in range(period, len(merged_df)):
            window_df = merged_df.iloc[i-period:i]
            result = adfuller(window_df['Close_2'] - window_df['Close_1'], regression='ct', autolag='AIC')
            
            result_summary = {
                'Date': merged_df.iloc[i]['Date'],
                'Asset_1': asset1,
                'Asset_2': asset2,
                'ADF Statistic': result[0],
                'p-value': result[1],
                'Critical Values': result[4],
                'Stationary': result[1] < 0.05
            }
            result_df = pd.concat([result_df, pd.DataFrame([result_summary])], ignore_index=True)
    
    return result_df



