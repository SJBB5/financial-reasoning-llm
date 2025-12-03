# Sam Brown
# building prompt and calling openai

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_prompt(ticker, moves, news_by_date):
    """
    moves: list of dicts like {"time", "date", "move"}
    news_by_date: dict { date_obj -> [headline_dict, ...] }

    Returns one big prompt with all info
    """
    lines = []
    lines.append(f"You are a financial analyst looking at {ticker}.")
    lines.append("For each big price move, here are the moves and nearby news.")
    lines.append("Explain in simple, realistic language what might be happening.")
    lines.append("If the news does not clearly explain the move, say that.")
    lines.append("")

    # Loop through moves 
    for m in moves:
        d = m["date"]
        move_pct = m["move"]
        time_str = m["time"]

        lines.append(f"Date: {d} | Move: {move_pct:.2f}% | Timestamp: {time_str}")

        # Get headlines for this move's date
        headlines = news_by_date.get(d, [])

        if not headlines:
            lines.append("Headlines: (no news found near this date)")
        else:
            lines.append("Headlines around this date:")
            for h in headlines:
                lines.append(f" - {h.get('date')}: {h.get('title')}")
        lines.append("")

    # join all lines and return to get sent to model
    return "\n".join(lines)


def explain_moves(ticker, moves, news_by_date):
    """
    ticker: stock symbol
    moves: list from find_big_moves
    news_by_date: dict returned by get_news_for_moves
    """
    if not moves:
        return "no big moves to explain"

    if client.api_key is None:
        return "OPENAI_API_KEY is not set(should be in .env)"

    prompt = build_prompt(ticker, moves, news_by_date) # build prompt based on our data

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a concise, realistic financial analyst.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3, # more consistent, less creative
        max_tokens=5000, # size of output
    )

    return response.choices[0].message.content
