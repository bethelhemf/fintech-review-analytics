import pandas as pd
import os
from src.sentiment_engine import SentimentEngine

def main():
    # 1. Setup paths
    input_file = 'data/cleaned_bank_reviews.csv'
    output_file = 'data/sentiment_results.csv'
    
    if not os.path.exists(input_file):
        print("Cleaned data not found. Run preprocessing first.")
        return

    # 2. Load Data
    df = pd.read_csv(input_file)
    texts = df['review'].astype(str).tolist()

    # 3. Initialize Engine and Run Analysis
    engine = SentimentEngine()
    
    print("Analyzing with DistilBERT...")
    df['bert_label'], df['bert_confidence'] = engine.get_bert_sentiment(texts)

    print("Analyzing with TextBlob (Baseline)...")
    tb_results = [engine.get_textblob_sentiment(t) for t in texts]
    df['textblob_label'] = [res[0] for res in tb_results]
    df['textblob_score'] = [res[1] for res in tb_results]

    # 4. Aggregate Results (Business Requirement)
    print("\n--- Summary: Sentiment by Bank ---")
    bank_summary = df.groupby(['bank', 'bert_label']).size().unstack(fill_value=0)
    print(bank_summary)

    print("\n--- Summary: Mean Sentiment by Rating ---")
    # Map for calculation: POSITIVE=1, NEUTRAL=0, NEGATIVE=-1
    mapping = {'POSITIVE': 1, 'NEUTRAL': 0, 'NEGATIVE': -1}
    df['sentiment_val'] = df['bert_label'].map(mapping)
    print(df.groupby('rating')['sentiment_val'].mean())

    # 5. Save
    df.to_csv(output_file, index=False)
    print(f"\nAnalysis complete. Results saved to {output_file}")

if __name__ == "__main__":
    main()