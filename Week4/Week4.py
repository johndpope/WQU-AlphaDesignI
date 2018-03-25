
import pandas as pd
import numpy as np
import pandas_datareader.data as web

import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc



# Question 1 to 5:
# Download price data for McDonald's stock from 1/2004 to 7/2005
start = datetime.datetime(2004, 1, 1)
end = datetime.datetime(2005, 8, 1)
f = web.DataReader('MCD', 'yahoo', start, end)

# Function to calculate
# Moving Average
def MA(df, n):
    MA = pd.Series(pd.rolling_mean(df['Close'], n), name='MA_'+str(n))
    df = df.join(MA)
    return(df)

# Exponential Moving Average
def EMA(df, n):
    EMA = pd.Series(pd.rolling_mean(df['Close'], n), name='EMA_'+str(n))
    df = df.join(EMA)
    return(df)

# Create new column for MA10 and MA60
f = MA(f, 10)
f = MA(f, 60)
# Calculate Oscillators of MA
f["Diff"] = f["MA_10"]-f["MA_60"]
f["MA_diff"] = pd.Series(pd.rolling_mean(f["Diff"],15), name="MA_diff")


# Extract Date from DataFrame Index
f['Date'] = f.index.values
f['Date'] = f.index.map(mdates.date2num)
ohlc = f[['Date', 'Open', 'High', 'Low', 'Close']]

# Plot candle stick/bar chart for stock price
f1, ax = plt.subplots(2, sharex=True, figsize=(10,8))
candlestick_ohlc(ax[0], ohlc.values, width=0.6, colorup='blue', colordown='red')
ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

ax[0].plot(f['MA_10'])
ax[0].plot(f['MA_60'])
ax[0].set_title("MCD stock price from 2004 to 2005")
ax[0].legend()
ax[0].grid()

# Plot 2nd graph for oscillators
ax[1].plot(f["MA_diff"])
ax[1].plot(f["Diff"])
ax[1].legend()
ax[1].set_title("Difference between MA60 and MA10 and 15-day MA oscillators")
ax[1].grid()
plt.show()

# Question 6 to 7:
# I will use backtrader library for backtesting purpose. The script will be included
# other files in zip folder

# Bollinger Band Calculation:
def BBands(df, n):
    MA = pd.Series(pd.rolling_mean(df['Close'], n))
    MSD = pd.Series(pd.rolling_std(df['Close'], n))
    b1 = MA+1.5*MSD
    B1 = pd.Series(b1, name = 'BollingerB+'+str(n))
    df = df.join(B1)
    b2 = MA-1.5*MSD
    B2 = pd.Series(b2, name = 'BollingerB_'+str(n))
    df = df.join(B2)
    return df
    
f = BBands(f, 10)

f1, ax = plt.subplots(figsize=(10,5))
candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='blue', colordown='red')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.plot(f['BollingerB+10'])
ax.plot(f['BollingerB_10'])
ax.set_title("Bollinger Band of 1.5 standard deviation and 10-day MA")
ax.legend()
ax.grid()