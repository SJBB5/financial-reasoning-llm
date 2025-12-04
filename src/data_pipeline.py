# Sam Brown
# Get stock data from yfinance

import yfinance as yf
import pandas as pd

def get_data(ticker, period="2y", interval="1d"):
    data = yf.download(ticker, period=period, interval=interval, auto_adjust=True)
    
    # Flatten multi-level columns if they exist
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    if data.empty:
        print("no data for", ticker)
        return None

    # Get percentages to later apply threshold to detect large moves
    data = data.sort_index()
    data["return_pct"] = data["Close"].pct_change() * 100
    return data
