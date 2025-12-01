# Sam Brown
# Detect and record "Big moves"

def find_big_moves(df, threshold=2.0):
    # safety check
    if df is None or "return_pct" not in df.columns:
        return []

    # retrieves data that meets threshold
    big = df[abs(df["return_pct"]) >= threshold]
    results = []

    # Get info on each "big move"
    for ts, row in big.iterrows():
        results.append({
            "time": ts,
            "move": float(row["return_pct"]),
        })

    return results
