# Sam Brown
# Get stock data from yfinance

import yfinance as yf
import pandas as pd

def get_data(ticker, period="2y", interval="1d"): # List of possible tickers found in docdumentation
    data = yf.download(ticker, period=period, interval=interval, auto_adjust=True)
    if data.empty:
        print("no data for", ticker)
        return None

    # Get percentages to later apply threshold to detect large moves
    data = data.sort_index()
    data["return_pct"] = data["Close"].pct_change() * 100
    return data
