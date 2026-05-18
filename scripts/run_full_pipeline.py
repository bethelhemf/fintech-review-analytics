import pandas as pd
import os
from src.sentiment_engine import SentimentEngine
from src.nlp_pipeline import NLPPipeline
from src.thematic_engine import ThematicEngine

def main():
    input_file = 'data/raw/raw_bank_reviews.csv'
    output_file = 'data/final_analytics_results.csv'
    
    if not os.path.exists(input_file):
        print("❌ Error: raw_bank_reviews.csv not found!")
        return

    df = pd.read_csv(input_file)

    # --- AUTO-DETECT COLUMNS ---
    # We look for common names for the review text
    text_col = None
    for col in ['content', 'review_text', 'review']:
        if col in df.columns:
            text_col = col
            break
            
    score_col = 'score' if 'score' in df.columns else 'rating'
    
    if text_col is None:
        print(f"❌ Error: Could not find review text column. Available: {df.columns.tolist()}")
        return

    print(f"✅ Using column '{text_col}' for analysis.")

    # Cleanup
    df = df.dropna(subset=[text_col, score_col])
    
    # Standardize for the AI models
    texts = df[text_col].astype(str).tolist()

    # --- RUN ENGINES ---
    print("Step 1: Running Sentiment Analysis...")
    sent_engine = SentimentEngine()
    df['sentiment_label'], df['sentiment_score'] = sent_engine.get_bert_sentiment(texts)

    print("Step 2: Running Thematic Classification...")
    them_engine = ThematicEngine()
    df['identified_theme'] = df[text_col].apply(lambda x: them_engine.classify(str(x)))

    # --- FINAL FORMATTING ---
    # Rename to the project required names
    df['review_text'] = df[text_col]
    df['rating'] = df[score_col]
    df['bank'] = df['bank_name'] if 'bank_name' in df.columns else 'Unknown'
    df['date'] = pd.to_datetime(df['at']).dt.date if 'at' in df.columns else '2023-01-01'
    
    # If no review_id, create one
    if 'reviewId' in df.columns:
        df['review_id'] = df['reviewId']
    else:
        df['review_id'] = range(len(df))

    final_df = df[['review_id', 'bank', 'review_text', 'rating', 'date', 'sentiment_label', 'sentiment_score', 'identified_theme']]
    
    final_df.to_csv(output_file, index=False)
    print(f"✅ Pipeline Complete! Results saved to {output_file}")

if __name__ == "__main__":
    main()