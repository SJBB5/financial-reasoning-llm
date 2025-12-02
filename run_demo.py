# quick test for basic implementation

from src.data_pipeline import get_data
from src.anomaly_detection import find_big_moves
from src.llm_reasoning_playground import explain_moves
from src.news_data import get_news

def main():
    # what we are using for now to test
    ticker = "AAPL"
    threshold = 3.0 # percent move
    news_limit = 10 # how many headlines from finviz

    print("ticker:", ticker)

    # get price data
    df = get_data(ticker)
    if df is None:
        print("could not get data")
        return None

    # find big moves
    print("finding big moves...")
    moves = find_big_moves(df, threshold=threshold)

    if not moves:
        print("no big moves found")
        return None

    print(f"found {len(moves)} big moves\n")

    # get news from FinViz
    print("getting news from finviz...")
    headlines = get_news(ticker, limit=news_limit)

    if not headlines:
        print("no headlines found")
    else:
        print("recent headlines:")
        for h in headlines:
            print("-", h.get("title"))
        print()

    # ask the LLM to explain, using moves + headlines
    print("asking LLM for explanation...\n")
    explanation = explain_moves(ticker, moves, headlines)

    print("LLM explanation:\n")
    print(explanation)
    
    # Return results with LLM parameters
    return {
        "explanation": explanation,
        "ticker": ticker,
        "moves": moves,
        "headlines": headlines,
        "llm_config": {
            "model": "gpt-4o-mini",
            "temperature": 0.3,
            "max_tokens": 1000
        }
    }


if __name__ == "__main__":
    main()