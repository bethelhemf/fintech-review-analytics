import pandas as pd
from src.sentiment_engine import SentimentEngine
def main():
    df = pd.read_csv("data/raw/raw_bank_reviews.csv")
    engine = SentimentEngine()
    df["sentiment"], df["score"] = engine.get_bert_sentiment(df["content"].astype(str).tolist())
    df.to_csv("data/final_analytics_results.csv", index=False)
    print("✅ NLP Pipeline Complete")
if __name__ == "__main__":
    main()
