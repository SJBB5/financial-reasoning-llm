# Sam Brown
# building prompt and calling openai

import os
from openai import OpenAI
from dotenv import load_dotenv

# load .env
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_prompt(ticker, moves, headlines):
    # make prompt for gpt using large movees and headlines (not lined up by dates yet, just getting it working for now)
    lines = []
    lines.append(f"You are a financial analyst looking at {ticker}.")
    lines.append("Here are some big price moves (percent changes):")
    lines.append("")

    for m in moves:
        lines.append(f"- {m['time']} : {m['move']:.2f}%")

    lines.append("")
    lines.append("Here are recent news headlines for this ticker:")
    lines.append("")

    if not headlines:
        lines.append("- (no headlines found)")
    else:
        for h in headlines:
            title = h.get("title")
            lines.append(f"- {title}")

    lines.append("")
    lines.append(
        "Based on the moves and the headlines, explain in simple language "
        "what might be going on with this stock. If you are not sure, say that."
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
        max_tokens=400, # size of response
    )

    text = response.choices[0].message.content
    return text
