# Sam Brown
# building prompt and calling openai

# Refine the means used to call the model, with the goal of refining the thinking provided by the chatbot
# and engineering the chatbot request to obtain more accurate results

import os
from openai import OpenAI
from dotenv import load_dotenv

# load .env
load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_prompt(ticker, moves, news_by_date):
    # make prompt for gpt using large movees and headlines (not lined up by dates yet, just getting it working for now)
    lines = []
    lines.append(f"Context: You are a financial analysis aid, with the goal of analyzing this stock: {ticker}")
    lines.append(f"You are expected to provide an overview of the current trends of the stock market in general, and the trends associated with this specific stock ({ticker})")
    lines.append(f"To acomplish this, you are provided with the most current and significant price changes of {ticker}, and large headlines associated with both the stock and the stock market as a whole")
    lines.append("Before generating output. Format a simple human language response to "
        "explain to users the trends found in the data.  Do not format the responses with any markdown atributes (###, **, etc)")
    lines.append("Current significant price changes (percent changes):")
    lines.append("")

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


    lines.append("")
    lines.append(
        f"Using the given significant stock price changes, and associated headlines for the stock {ticker}, analyze the "
        "underlying trends as associated with the movements of the stock price, highlighting the causes behind price movement, "
        f"and finally general stock market trends that may have correlation with the movement of {ticker} stock price"
        "When explaining recent price movements, report the trends per month going back 1 year  (IE December -10%, January +25%), and then report the aggregate change from the first month to now "
    )

    return "\n".join(lines)


def explain_moves(ticker, moves, headlines):
    # call once for explanation string
    if not moves:
        return "no big moves to explain"

    if client.api_key is None:
        return "OPENAI_API_KEY is not set(should be in .env)"

    prompt = build_prompt(ticker, moves, headlines)

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # can try different models
        messages=[
            {
                "role": "system",
                "content": "You are a concise, realistic financial analyst.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3, # how creative model can be in response
        max_tokens=5000, # size of response
    )

    text = response.choices[0].message.content
    return text
