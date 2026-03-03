import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("outputs", exist_ok=True)

def main():
    df = pd.read_csv("data/news_impact.csv")

    df = df.dropna(subset=["alpha_1d", "sent_score"])

    print("\nTotal usable rows:", len(df))

    correlation = df["sent_score"].corr(df["alpha_1d"])
    print("\n📊 Correlation (sentiment vs alpha_1d):", round(correlation, 4))


    avg_alpha = df.groupby("sent_label")["alpha_1d"].mean()
    print("\n📈 Average alpha by sentiment:")
    print(avg_alpha)

    plt.figure()
    plt.scatter(df["sent_score"], df["alpha_1d"])
    plt.xlabel("Sentiment Score")
    plt.ylabel("Next Day Alpha")
    plt.title("Sentiment vs Next Day Alpha")
    plt.savefig("outputs/sentiment_vs_alpha.png")
    plt.close()

    avg_alpha.plot(kind="bar")
    plt.title("Average Alpha by Sentiment Label")
    plt.ylabel("Average Alpha")
    plt.savefig("outputs/avg_alpha_bar.png")
    plt.close()

    print("\n Charts saved in outputs/ folder")

if __name__ == "__main__":
    main()