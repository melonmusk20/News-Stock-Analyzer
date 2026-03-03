import os
import csv
import feedparser
from datetime import datetime, timezone

os.makedirs("data", exist_ok=True)

TICKER_QUERIES = {
    "AAPL": "AAPL stock",
    "TSLA": "TSLA stock",
    "RELIANCE.NS": "Reliance shares",
    "TCS.NS": "TCS results",
}

def google_news_rss_url(query: str) -> str:
     q = query.strip().replace(" ", "+")
     return f"https://news.google.com/rss/search?q={q}&hl=en-IN&gl=IN&ceid=IN:en"

def parse_published(entry) -> str:
     if getattr(entry, "published_parsed",None):
          dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
          return dt.isoformat()
     return ""

def fetch_items(ticker: str, query: str):
     url = google_news_rss_url(query)
     feed = feedparser.parse(url)

     items = []
     for e in feed.entries:
          source_title = ""
          try:
               src = e.get("source", None)
               if isinstance(src, dict):
                    source_title = src.get("title", "") or ""
               elif src:
                    source_title = getattr(src, "title", "") or ""
          except Exception:
               source_title = ""

          items.append({
            "ticker": ticker,
            "query": query,
            "published_at_utc": parse_published(e),
            "title": (e.get("title") or "").strip(),
            "link": (e.get("link") or "").strip(),
            "source": source_title.strip() or "unknown",
        })
     return items

def dedupe(rows):
    seen = set()
    out = []
    for r in rows:
        key = (r["ticker"], r["link"])  # simple dedupe
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out

def main():
    all_rows = []
    for ticker, query in TICKER_QUERIES.items():
        rows = fetch_items(ticker, query)
        all_rows.extend(rows)

    all_rows = dedupe(all_rows)

    out_path = "data/news.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["ticker", "query", "published_at_utc", "title", "link", "source"],
        )
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Saved {len(all_rows)} rows to {out_path}")
    if all_rows:
        print("Sample row:")
        print(all_rows[0])

if __name__ == "__main__":
    main()