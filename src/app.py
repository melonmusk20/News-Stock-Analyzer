import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="News Stock Analyzer", layout="wide")

# ---------- Load ----------
df = pd.read_csv("data/news_impact.csv")
df["ticker"] = df["ticker"].astype(str).str.strip()

usable = df.dropna(subset=["sent_score", "alpha_1d"]).copy()

# ---------- CSS (React-like) ----------
st.markdown("""
<style>
/* Page background gradient */
.stApp {
  background: radial-gradient(circle at 20% 30%, rgba(99,102,241,0.35), transparent 55%),
              radial-gradient(circle at 80% 35%, rgba(16,185,129,0.28), transparent 55%),
              radial-gradient(circle at 55% 70%, rgba(236,72,153,0.22), transparent 55%),
              #05060a;
  color: rgba(255,255,255,0.92);
  font-family: ui-sans-serif, system-ui;
}

.block-container { padding-top: 1.2rem; max-width: 1200px; }

/* Remove Streamlit default padding around widgets a bit */
div[data-testid="stHorizontalBlock"] { gap: 14px; }

/* Cards */
.card {
  border: 1px solid rgba(255,255,255,0.14);
  background: rgba(255,255,255,0.06);
  border-radius: 18px;
  padding: 14px 14px;
  box-shadow: 0 12px 34px rgba(0,0,0,0.38);
}

.cardHeader {
  display:flex; align-items:center; justify-content:space-between;
  margin-bottom: 10px;
}

.h1 { font-size: 34px; font-weight: 800; margin: 0; letter-spacing: 0.2px; }
.sub { color: rgba(255,255,255,0.70); font-size: 14px; margin-top: 6px; }

.badge {
  display:inline-block;
  padding: 6px 12px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.15);
  font-weight: 800;
  font-size: 12px;
}

.badge-buy { background: rgba(34,197,94,0.15); border-color: rgba(34,197,94,0.35); }
.badge-hold { background: rgba(245,158,11,0.15); border-color: rgba(245,158,11,0.35); }
.badge-avoid { background: rgba(239,68,68,0.15); border-color: rgba(239,68,68,0.35); }

.small { color: rgba(255,255,255,0.68); font-size: 12px; }
.kpi { font-size: 26px; font-weight: 900; margin: 2px 0 0; }

.divider {
  height:1px; background: rgba(255,255,255,0.10);
  margin: 10px 0 12px;
}

/* Signal row */
.signalRow {
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.05);
  border-radius: 16px;
  padding: 12px 12px;
  margin-bottom: 10px;
}

.signalTop { display:flex; justify-content:space-between; align-items:center; }
.ticker { font-size: 16px; font-weight: 900; letter-spacing: 0.2px; }
.meta { color: rgba(255,255,255,0.70); font-size: 13px; margin-top: 6px; }
.meta b { color: rgba(255,255,255,0.92); }

/* News card */
.newsCard {
  border: 1px solid rgba(255,255,255,0.12);
  background: rgba(255,255,255,0.08);
  border-radius: 16px;
  padding: 12px 12px;
  margin-bottom: 10px;
}

.newsTitle { font-weight: 850; font-size: 14px; line-height: 1.35; }
.newsMeta { margin-top: 6px; font-size: 12px; color: rgba(255,255,255,0.68); }
.tags { margin-top: 10px; display:flex; flex-wrap:wrap; gap: 8px; }
.tag {
  border: 1px solid rgba(255,255,255,0.12);
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 12px;
  color: rgba(255,255,255,0.70);
  background: rgba(255,255,255,0.04);
}

/* Make text inputs look nicer */
input[type="text"] {
  border-radius: 14px !important;
}

/* Footer */
.footer {
  text-align:center; margin-top: 16px;
  color: rgba(255,255,255,0.60); font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Helpers ----------
def decide_signal(avg_sentiment: float, mentions: int) -> str:
    if avg_sentiment > 0.4 and mentions >= 2:
        return "BUY"
    if avg_sentiment < -0.4:
        return "AVOID"
    return "HOLD"

def fmt(x, d=3):
    try:
        if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
            return "—"
        return f"{float(x):.{d}f}"
    except Exception:
        return "—"

# ---------- Compute metrics ----------
corr = None
if len(usable) > 1:
    c = usable["sent_score"].corr(usable["alpha_1d"])
    if not (isinstance(c, float) and math.isnan(c)):
        corr = c

avg_alpha = {}
if "sent_label" in usable.columns and len(usable) > 0:
    avg_alpha = usable.groupby("sent_label")["alpha_1d"].mean().to_dict()

# Signals per ticker
signals_df = pd.DataFrame()
if len(usable) > 0:
    signals_df = usable.groupby("ticker").agg(
        avg_sentiment=("sent_score", "mean"),
        mentions=("title", "count"),
        avg_alpha=("alpha_1d", "mean"),
    ).reset_index()
    signals_df["signal"] = signals_df.apply(lambda r: decide_signal(r["avg_sentiment"], int(r["mentions"])), axis=1)

# ---------- Header row ----------
h1, h2 = st.columns([4, 1])

with h1:
    st.markdown("""
    <div class="card">
      <div class="cardHeader">
        <div style="display:flex; align-items:center; gap:12px;">
          <div style="width:44px;height:44px;border-radius:14px;display:grid;place-items:center;
                      font-weight:900;background: linear-gradient(135deg, rgba(99,102,241,0.95), rgba(16,185,129,0.85));">
            NS
          </div>
          <div>
            <div class="h1">News Stock Analyzer</div>
            <div class="sub">FinBERT sentiment → next-day market-adjusted alpha signals</div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with h2:
    st.markdown(f"""
    <div class="card">
      <div class="small">Correlation</div>
      <div class="kpi">{fmt(corr, 2)}</div>
      <div class="small">rows: {len(usable)}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ---------- Main layout ----------
left, right = st.columns([1.25, 0.9])

with left:
    st.markdown("<div class='card'><div class='cardTitle' style='font-weight:900;font-size:18px;'>Signals</div>", unsafe_allow_html=True)

    # Chips
    chip = st.segmented_control(
        "signal_filter",
        options=["ALL", "BUY", "HOLD", "AVOID"],
        default="ALL",
        label_visibility="collapsed"
    )

    # Search
    q = st.text_input("", placeholder="Search ticker (AAPL, TSLA, RELIANCE.NS...)")

    # mini stats
    st.markdown(f"""
    <div class="small" style="display:flex; gap:14px; margin: 6px 0 10px;">
      <div>pos α <b>{fmt(avg_alpha.get("positive"),4)}</b></div>
      <div>neu α <b>{fmt(avg_alpha.get("neutral"),4)}</b></div>
      <div>neg α <b>{fmt(avg_alpha.get("negative"),4)}</b></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Filter signals
    show = signals_df.copy()
    if len(show) > 0:
        if chip != "ALL":
            show = show[show["signal"] == chip]
        if q.strip():
            show = show[show["ticker"].str.lower().str.contains(q.strip().lower())]
        show = show.sort_values("avg_sentiment", ascending=False)

    if len(show) == 0:
        st.markdown("<div class='small'>No tickers match your search/filter.</div>", unsafe_allow_html=True)
        selected = None
    else:
        # clickable list
        tickers = show["ticker"].tolist()
        selected = st.radio(
            "ticker_select",
            options=tickers,
            label_visibility="collapsed",
            index=0
        )

        # render rows as cards (below radio, but radio handles selection)
        for _, r in show.iterrows():
            cls = "badge-hold"
            if r["signal"] == "BUY": cls = "badge-buy"
            if r["signal"] == "AVOID": cls = "badge-avoid"

            st.markdown(f"""
            <div class="signalRow">
              <div class="signalTop">
                <div class="ticker">{r['ticker']}</div>
                <span class="badge {cls}">{r['signal']}</span>
              </div>
              <div class="meta">
                sent <b>{fmt(r['avg_sentiment'],3)}</b> &nbsp;•&nbsp;
                α <b>{fmt(r['avg_alpha'],4)}</b> &nbsp;•&nbsp;
                mentions <b>{int(r['mentions'])}</b>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close card

with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    if not selected:
        st.markdown("""
        <div style="font-weight:900; font-size:18px;">Select a ticker</div>
        <div class="divider"></div>
        <div class="newsCard">
          <div style="font-weight:900; font-size:18px; margin-bottom:6px;">How to use</div>
          <div class="small">
            1. Pick a ticker from the left.<br/>
            2. See recent news + sentiment + alpha here.<br/>
            3. Signals are rule-based: BUY/HOLD/AVOID.
          </div>
          <div class="small" style="margin-top:10px;">
            Tip: deploy on Streamlit Cloud for a shareable demo.
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='font-weight:900; font-size:18px;'>News • {selected}</div>", unsafe_allow_html=True)
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        news = df[df["ticker"] == selected].copy()
        # show latest first if published exists
        if "published_at_utc" in news.columns:
            news["published_at_utc"] = news["published_at_utc"].astype(str)
        news = news.tail(25)

        if len(news) == 0:
            st.markdown("<div class='small'>No news items found.</div>", unsafe_allow_html=True)
        else:
            # render
            for _, n in news.iloc[::-1].iterrows():
                title = str(n.get("title", ""))
                source = str(n.get("source", "unknown"))
                link = str(n.get("link", ""))
                when = str(n.get("published_at_utc", ""))[:16].replace("T", " ")
                sent_label = str(n.get("sent_label", "neutral"))
                sent_score = n.get("sent_score", None)
                alpha = n.get("alpha_1d", None)

                st.markdown(f"""
                <div class="newsCard">
                  <div class="newsTitle">{title}</div>
                  <div class="newsMeta">{source} • {when}</div>
                  <div class="tags">
                    <span class="tag">{sent_label}</span>
                    <span class="tag">score {fmt(sent_score,3)}</span>
                    <span class="tag">α {fmt(alpha,4)}</span>
                  </div>
                  <div style="margin-top:10px;">
                    <a href="{link}" target="_blank" style="color: rgba(255,255,255,0.85); text-decoration: underline;">Open article</a>
                  </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='footer'>Built with Streamlit • Signals are informational, not financial advice.</div>", unsafe_allow_html=True)