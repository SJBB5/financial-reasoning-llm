# Sam Brown
# Scraping news headlines for our ticker. NOTE: no aligning time to big moves yet.

import requests
from bs4 import BeautifulSoup

def get_news(ticker, limit=10):
    url = f"https://finviz.com/quote.ashx?t={ticker}"
    headers = {"User-Agent": "Mozilla/5.0"}

    resp = requests.get(url, headers=headers)
    html = resp.text

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="news-table")

    if table is None:
        return []

    items = []

    # grab first `limit` headlines
    for row in table.find_all("tr")[:limit]:
        a = row.find("a")
        if not a:
            continue

        title = a.get_text(strip=True)
        link = a["href"]

        items.append({
            "title": title,
            "link": link,
        })

    return items