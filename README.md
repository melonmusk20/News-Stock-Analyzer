# 📈 News-Driven Stock Sentiment Analyzer

An end-to-end AI-powered stock analysis system that combines:

• Financial News (Google RSS) 
• FinBERT Sentiment Analysis  
• Stock Price Data (Yahoo Finance)  
• Market Index Benchmarking 
• Alpha Calculation  
• Trading Signal Generation  
• Interactive Streamlit Dashboard  

---

## 🚀 Live Demo
https://melonmusk20-news-stock-analyzer-srcapp-uul8tx.streamlit.app/

---

## 🎯 Problem Statement

Can financial news sentiment help predict short-term stock performance?

This project:
- Fetches real-time stock news
- Analyzes sentiment using FinBERT
- Merges it with stock & index returns
- Calculates alpha (stock performance vs market)
- Generates BUY / HOLD / AVOID signals
- Visualizes everything in a professional dashboard

---

## 🏗️ System Architecture

```bash 
Google News RSS
↓
Sentiment Analysis (FinBERT)
↓
Yahoo Finance Price Data
↓
Alpha Calculation (Stock - Index)
↓
Signal Engine
↓
Streamlit Dashboard
```

```code
---

## 🧠 Tech Stack

| Layer | Technology |
|-------|------------|
| NLP Model | FinBERT (ProsusAI) |
| Backend Logic | Python |
| Data Processing | Pandas |
| Stock Data | yFinance |
| Frontend | Streamlit |
| Deployment | Streamlit Cloud |
| Version Control | Git + GitHub |

---
<!-- test commit for n8n AI code reviewer workflow -->
```

## 📂 Project Structure

```

News-Stock-Analyzer/
│
├── data/
│ ├── news.csv
│ ├── news_scored.csv
│ ├── prices_stock.csv
│ ├── prices_index.csv
│ ├── news_impact.csv
│
├── outputs/
│ ├── avg_alpha_bar.png
│ ├── sentiment_vs_alpha.png
│
├── src/
│ ├── analysis.py
│ ├── app.py
│ ├── impact_join.py
│ ├── main.py
│ ├── prices.py
│ ├── rss_fetch.py
│ ├── sentiment.py
│ ├── signal.py
│
└── README.md

```

---

## ⚙️ How It Works

### 1️⃣ News Collection
Pulls stock-related news using Google RSS feeds.

### 2️⃣ Sentiment Analysis
Uses FinBERT to classify news as:
- Positive
- Neutral
- Negative

Generates:
- `sent_score`
- `sent_label`
- `confidence`

---

### 3️⃣ Price Data Integration
Downloads:
- Stock price
- Market index (^GSPC / ^NSEI)

Calculates:
- 1-day return
- Alpha (Stock return - Index return)

---

### 4️⃣ Signal Generation

```python
if sentiment > 0.4 and mentions >= 2:
    BUY
elif sentiment < -0.4:
    AVOID
else:
    HOLD
```

---

# 📊 Dashboard Features

   • Stock selector

   • Sentiment overview

   • Alpha correlation

   • Signal output (BUY / HOLD / AVOID)

   • Clean professional UI

 ---

 # 🔧 Local Setup

 ```bash
git clone https://github.com/melonmusk20/News-Stock-Analyzer.git
cd News-Stock-Analyzer

pip install -r requirements.txt

streamlit run streamlit_app.py

```


