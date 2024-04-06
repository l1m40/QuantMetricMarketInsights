#
# Inpired by
# https://twitter.com/pedma7/status/1772961948654546966
# Code generated using GPT 
# https://chat.openai.com/share/7de65c8c-4498-4a11-8bff-fde9da5d1449
#
#
#

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define the function to fetch historical data from Yahoo Finance
def fetch_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)
    return data['Adj Close'].to_frame()

# Define the function to calculate trading signals
def generate_signals_SMACross(data,short_window,long_window):
    # Example: Simple Moving Average (SMA) crossover strategy
    # short_window = 40
    # long_window = 100

    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0

    signals['short_mavg'] = data.rolling(window=short_window, min_periods=1, center=False).mean()
    signals['long_mavg'] = data.rolling(window=long_window, min_periods=1, center=False).mean()

    signals['signal'][short_window:] = \
        np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)

    signals['positions'] = signals['signal'].diff()

    return signals

# Define the function to backtest the trading strategy
def backtest_strategy(data, signals, hand):
    initial_capital = 10000.0
    positions = pd.DataFrame(index=signals.index).fillna(0.0)
    positions['positions'] = hand / data['Adj Close'] * signals['signal']   # Buy or sell 100 shares of the asset
    portfolio = positions.multiply(data['Adj Close'], axis=0)
    pos_diff = positions.diff()

    portfolio['holdings'] = (positions.multiply(data['Adj Close'], axis=0)).sum(axis=1)
    portfolio['cash'] = initial_capital - (pos_diff.multiply(data['Adj Close'], axis=0)).sum(axis=1).cumsum()

    portfolio['total'] = portfolio['cash'] + portfolio['holdings']
    portfolio['returns'] = portfolio['total'].pct_change()
    
    return portfolio

# Define the function to visualize the backtest results
def visualize_backtest(portfolio):
    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(111, ylabel='Portfolio value in $')
    portfolio['total'].plot(ax=ax1, lw=2.)
    ax1.plot(portfolio.loc[portfolio.positions == 1.0].index,
             portfolio.total[portfolio.positions == 1.0],
             '^', markersize=10, color='g', lw=0, label='Buy signal')
    ax1.plot(portfolio.loc[portfolio.positions == -1.0].index,
             portfolio.total[portfolio.positions == -1.0],
             'v', markersize=10, color='r', lw=0, label='Sell signal')
    plt.legend()
    plt.show()

# Evaluate the backtest results
def evaluate_backtest(portfolio):
    # Calculate cumulative returns
    portfolio['Returns'] = portfolio['total'].pct_change()
    portfolio['Cumulative_Returns'] = (1 + portfolio['Returns']).cumprod() - 1

    # Calculate drawdown
    cumulative_returns = portfolio['Cumulative_Returns']
    rolling_max = cumulative_returns.cummax()
    drawdown = cumulative_returns - rolling_max

    # Calculate maximum drawdown and its duration
    max_drawdown = drawdown.min()
    max_drawdown_duration = drawdown[drawdown == max_drawdown].index[0]

    # Calculate Sharpe ratio (assuming risk-free rate of 0)
    daily_returns = portfolio['Returns']
    sharpe_ratio = np.sqrt(252) * (daily_returns.mean() / daily_returns.std())

    # Print key performance metrics
    print("Key Performance Metrics:")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"Maximum Drawdown: {max_drawdown:.2%}")
    print(f"Maximum Drawdown Duration: {max_drawdown_duration}")

    # Plot the equity curve and drawdown
    plt.figure(figsize=(12, 6))
    plt.plot(portfolio.index, portfolio['Cumulative_Returns'], label='Equity Curve')
    plt.fill_between(portfolio.index, portfolio['Cumulative_Returns'], color='skyblue', alpha=0.3)
    plt.plot(drawdown.index, drawdown, label='Drawdown', color='red')
    plt.title('Equity Curve and Drawdown for SMA Crossover Strategy Backtest')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.show()



# Main function to run the backtest
# def main():

# tickers = ['AAPL']  # Example: Apple stock
tickers = ['BTC-USD']
start_date = '2020-01-01'
end_date = '2025-01-01'

# Fetch historical data
data = fetch_data(tickers, start_date, end_date)

# Generate trading signals
# signals = generate_signals(data)
signals = generate_signals_SMACross(data,5,21)
# signals = generate_signals_SMACross(data,55,233)

# Backtest the trading strategy
portfolio = backtest_strategy(data, signals, 10000)

# Concatenate the two portfolios
# portfolio = pd.concat([
#   backtest_strategy(data[data.index< "2023-01-01"], signals[data.index< "2023-01-01"], 10000), 
#   backtest_strategy(data[data.index>="2023-01-01"], signals[data.index>="2023-01-01"], 10000)
# ])
# portfolio.reset_index(drop=True, inplace=True)

# Visualize the backtest results
# visualize_backtest(portfolio)

# Evaluate the backtest and plot the results
evaluate_backtest(portfolio)
    
# if __name__ == "__main__":
#     main()

