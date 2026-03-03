import os
import pandas as pd
from transformers import pipeline

os.makedirs("data", exist_ok=True)

MODEL_NAME = "ProsusAI/finbert"

def label_to_score(label: str, prob: float) -> float:
    label = label.lower()
    if label == "positive":
        return +prob
    if label == "negative":
        return -prob
    return 0.0

def main():
    in_path = "data/news.csv"
    out_path = "data/news_scored.csv"

    df = pd.read_csv(in_path)

    clf = pipeline("sentiment-analysis", model=MODEL_NAME)

    labels = []
    scores = []
    confs = []

    for title in df["title"].fillna("").astype(str).tolist():
        text = title.strip()
        if not text:
            labels.append("neutral")
            scores.append(0.0)
            confs.append(0.0)
            continue

        res = clf(text[:512])[0] 
        lab = res["label"].lower()
        prob = float(res["score"])

        labels.append(lab)
        confs.append(prob)
        scores.append(label_to_score(lab, prob))

    df["sent_label"] = labels
    df["sent_conf"] = confs
    df["sent_score"] = scores

    df.to_csv(out_path, index=False)
    print(f" Saved {len(df)} rows to {out_path}")
    print(df[["ticker","title","sent_label","sent_score"]].head(5))

if __name__ == "__main__":
    main()