import os
import pandas as pd
import yfinance as yf

os.makedirs("data", exist_ok=True)

STOCK_TICKERS = ["AAPL", "TSLA", "RELIANCE.NS", "TCS.NS"]
INDEX_TICKERS = ["^GSPC", "^NSEI"] 

START = "2026-02-01" 
END = None

def download(tickers: list[str], start: str, end=None) -> pd.DataFrame:
    df = yf.download(tickers, start=start, end=end, progress=False, group_by="ticker", auto_adjust=False)
    out = []
    if isinstance(df.columns, pd.MultiIndex):
        for t in tickers:
            if t not in df.columns.levels[0]:
                continue
            tmp = df[t].copy()
            tmp = tmp.reset_index().rename(columns={"Date": "date"})
            tmp.columns = [c.lower() for c in tmp.columns]
            tmp["ticker"] = t
            out.append(tmp[["date","ticker","open","high","low","close","volume"]])
        res = pd.concat(out, ignore_index=True)
    else:
        df = df.reset_index().rename(columns={"Date": "date"})
        df.columns = [c.lower() for c in df.columns]
        df["ticker"] = tickers[0]
        res = df[["date","ticker","open","high","low","close","volume"]]
    return res

def add_next_day_return(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["ticker", "date"])
    df["next_close"] = df.groupby("ticker")["close"].shift(-1)
    df["ret_1d"] = (df["next_close"] - df["close"]) / df["close"]
    return df

def main():
    stock = download(STOCK_TICKERS, START, END)
    index = download(INDEX_TICKERS, START, END)

    stock = add_next_day_return(stock)
    index = add_next_day_return(index)

    stock.to_csv("data/prices_stock.csv", index=False)
    index.to_csv("data/prices_index.csv", index=False)

    print("Saved data/prices_stock.csv and data/prices_index.csv")
    print(stock.head(3))

if __name__ == "__main__":
    main()