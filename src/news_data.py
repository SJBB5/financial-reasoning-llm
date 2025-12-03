# Sam Brown
# Scraping news headlines for our ticker. 

import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
EODHD_API_KEY = os.getenv("EODHD_API_KEY")

def get_news_for_moves(ticker, moves, window_days=1, limit=50, exchange="US"):
    """
    For each move we return the news headline within a window defined by window_days
    Returns:
        dict:
            A single dictionary mapping each move date (datetime.date)
            to a list of dictionaries, where each inner dictionary
            contains information about one news headline for that date.
    """
    if not moves or EODHD_API_KEY is None:
        return {}

    print("Starting news pull")

    # Needed for api
    symbol = f"{ticker}.{exchange}"
    base_url = "https://eodhd.com/api/news"

    news_by_date = {}

    # unique dates so we don't call the API twice for the same day
    for d in sorted({m["date"] for m in moves}):
        
        print(f"pulling news from {d}")
        
        # Define time window for news pull
        center = pd.Timestamp(d)
        start = (center - pd.Timedelta(days=window_days)).strftime("%Y-%m-%d")
        end   = (center + pd.Timedelta(days=window_days)).strftime("%Y-%m-%d")

        params = {
            "s": symbol,
            "from": start,
            "to": end,
            "limit": limit,
            "offset": 0, # start from first result
            "api_token": EODHD_API_KEY,
            "fmt": "json",
        }

        resp = requests.get(base_url, params=params)

        # grab error if request fails
        if resp.status_code != 200:
            print("News error:", resp.status_code, resp.text)
            news_by_date[d] = []
            continue

        # get response in json
        data = resp.json()
        
        headlines = []
        # Looping through headlines for each date
        for item in data:
            dt = pd.to_datetime(item.get("date")) if item.get("date") else None
            headlines.append({
                "ticker": ticker,
                "datetime": dt,
                "date": dt.date(),
                "title": item.get("title"),
                "link": item.get("link"),
                "content": item.get("content"),
            })

        news_by_date[d] = headlines

    return news_by_date
