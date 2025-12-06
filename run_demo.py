# quick test for basic implementation

from src.data_pipeline import get_data
from src.anomaly_detection import find_big_moves
from src.news_data import get_news_for_moves
from src.llm_reasoning_playground import explain_moves

def main():
    ticker = "ORCL"
    threshold = 5.0  # pct move
    window_days = 1 # news window around each move
    per_move_limit = 50  # max headlines per move window

    print("ticker:", ticker)

    #  price data
    df = get_data(ticker)
    if df is None or df.empty:
        print("could not get data")
        return

    # big moves (list of dictionaries with time, date, and move size)
    moves = find_big_moves(df, threshold=threshold) 
    if not moves:
        print("no big moves found")
        return

    print(f"found {len(moves)} big moves")

    # news per move 
    news_by_date = get_news_for_moves(
        ticker,
        moves,
        window_days=window_days,
        limit=per_move_limit,
    )

    # list how many headlines for each move
    for m in moves:
        d = m["date"]
        print(f"{d} ({m['move']:.2f}%): {len(news_by_date.get(d, []))} headlines")

    # LLM explanation
    explanation = explain_moves(ticker, moves, news_by_date)
    print("\nLLM explanation:\n")
    print(explanation)

    return {
        "ticker": ticker,
        "moves": moves,
        "news_by_date": news_by_date,
        "explanation": explanation,
    }

if __name__ == "__main__":
    main()
