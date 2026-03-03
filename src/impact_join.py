import os
import pandas as pd

os.makedirs("data", exist_ok=True)

INDEX_MAP = {
    "AAPL": "^GSPC",
    "TSLA": "^GSPC",
    "RELIANCE.NS": "^NSEI",
    "TCS.NS": "^NSEI",
}

def main():
    news = pd.read_csv("data/news_scored.csv")
    stock = pd.read_csv("data/prices_stock.csv")
    idx = pd.read_csv("data/prices_index.csv")

    news["ticker"] = news["ticker"].astype(str).str.strip()
    stock["ticker"] = stock["ticker"].astype(str).str.strip()
    idx["ticker"] = idx["ticker"].astype(str).str.strip()

    stock["date"] = pd.to_datetime(stock["date"], errors="coerce").dt.strftime("%Y-%m-%d")
    idx["date"] = pd.to_datetime(idx["date"], errors="coerce").dt.strftime("%Y-%m-%d")

    news_dt = pd.to_datetime(news["published_at_utc"], errors="coerce", utc=True)
    news["date"] = (news_dt.dt.floor("D") + pd.Timedelta(days=1)).dt.strftime("%Y-%m-%d")

    merged = news.merge(
        stock[["date", "ticker", "close", "ret_1d"]],
        on=["date", "ticker"],
        how="left"
    )

    merged["index_ticker"] = merged["ticker"].map(INDEX_MAP)

    merged = merged.merge(
        idx[["date", "ticker", "ret_1d"]].rename(
            columns={"ticker": "index_ticker", "ret_1d": "index_ret_1d"}
        ),
        on=["date", "index_ticker"],
        how="left"
    )

    merged["alpha_1d"] = merged["ret_1d"] - merged["index_ret_1d"]

    out_path = "data/news_impact.csv"
    merged.to_csv(out_path, index=False)

    print(f" Saved {len(merged)} rows to {out_path}")
    print("Non-null ret_1d:", int(merged["ret_1d"].notna().sum()))
    print("Non-null alpha_1d:", int(merged["alpha_1d"].notna().sum()))
    print(merged[["ticker", "title", "sent_score", "ret_1d", "alpha_1d"]].head(5))


if __name__ == "__main__":
    main()