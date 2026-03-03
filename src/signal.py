import pandas as pd

def generate_signal():
    df = pd.read_csv("data/news_impact.csv")

    # sentiment must exist, alpha optional
    df = df.dropna(subset=["sent_score"])
    if df.empty:
        return {"error": "No sentiment rows found"}

    grouped = df.groupby("ticker").agg(
        avg_sentiment=("sent_score", "mean"),
        mentions=("title", "count"),
        avg_alpha=("alpha_1d", "mean")  # will be NaN if missing, that's OK
    ).reset_index()

    signals = []
    for _, row in grouped.iterrows():
        sentiment = row["avg_sentiment"]
        mentions = int(row["mentions"])

        if sentiment > 0.4 and mentions >= 2:
            decision = "BUY"
        elif sentiment < -0.4:
            decision = "AVOID"
        else:
            decision = "HOLD"

        signals.append({
            "ticker": row["ticker"],
            "avg_sentiment": round(float(sentiment), 3),
            "mentions": mentions,
            "avg_alpha": None if pd.isna(row["avg_alpha"]) else round(float(row["avg_alpha"]), 4),
            "signal": decision
        })

    # best first
    signals.sort(key=lambda x: x["avg_sentiment"], reverse=True)
    return signals