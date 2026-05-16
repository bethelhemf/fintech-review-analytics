import pandas as pd
from transformers import pipeline
import torch

def run_sentiment_analysis():
    # 1. Load Cleaned Data
    file_path = 'data/cleaned_bank_reviews.csv'
    if not os.path.exists(file_path):
        print("Cleaned data not found!")
        return
    
    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} reviews for analysis.")

    # 2. Initialize DistilBERT Pipeline
    # sst-2 is great for binary sentiment (Positive/Negative)
    print("Loading DistilBERT model (this may take a minute)...")
    classifier = pipeline(
        "sentiment-analysis", 
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=-1 # Set to 0 if you have a GPU, -1 for CPU
    )

    # 3. Process Sentiments
    results = []
    # Using a list comprehension for efficiency
    # We truncate text to 512 tokens (DistilBERT limit)
    texts = df['review'].astype(str).tolist()
    
    print("Analyzing sentiment...")
    raw_results = classifier(texts, truncation=True)

    # 4. Refine Results (Adding Neutral Logic)
    # Rationale: If confidence is low (< 0.6), we categorize as 'Neutral'
    final_labels = []
    scores = []

    for res in raw_results:
        label = res['label']
        score = res['score']
        
        if score < 0.7:  # Threshold for Neutrality
            final_labels.append('NEUTRAL')
        else:
            final_labels.append(label)
        scores.append(score)

    df['sentiment'] = final_labels
    df['confidence'] = scores

    # 5. Aggregate Results
    print("\n--- Sentiment Aggregation by Bank ---")
    summary = df.groupby(['bank', 'sentiment']).size().unstack(fill_value=0)
    print(summary)

    print("\n--- Mean Sentiment by Star Rating ---")
    # We map POSITIVE to 1, NEGATIVE to -1, NEUTRAL to 0 for a 'Mean Sentiment'
    sentiment_map = {'POSITIVE': 1, 'NEUTRAL': 0, 'NEGATIVE': -1}
    df['sentiment_numeric'] = df['sentiment'].map(sentiment_map)
    
    rating_agg = df.groupby('rating')['sentiment_numeric'].mean()
    print(rating_agg)

    # 6. Save Results
    df.to_csv('data/sentiment_results.csv', index=False)
    print("\nResults saved to data/sentiment_results.csv")

if __name__ == "__main__":
    import os
    run_sentiment_analysis()