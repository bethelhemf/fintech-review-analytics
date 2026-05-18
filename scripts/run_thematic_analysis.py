import pandas as pd
import os
from src.thematic_engine import ThematicEngine

def main():
    input_file = 'data/sentiment_results.csv'
    output_file = 'data/final_thematic_results.csv'
    
    if not os.path.exists(input_file):
        print("Sentiment results not found.")
        return

    df = pd.read_csv(input_file)
    engine = ThematicEngine()

    # 1. Keyword Extraction Per Bank
    print("\n--- Top Keywords Per Bank (TF-IDF) ---")
    for bank in df['bank'].unique():
        bank_texts = df[df['bank'] == bank]['review'].astype(str)
        keywords = engine.get_top_keywords(bank_texts)
        print(f"{bank}: {', '.join(keywords)}")

    # 2. Theme Classification (This takes time, let's sample or run on all)
    print("\nClassifying themes for all reviews (BART model)...")
    # For speed during testing, you can use .head(100), otherwise use full df
    df['theme'] = df['review'].apply(lambda x: engine.classify_theme(str(x)))

    # 3. Aggregate Theme Sentiment
    print("\n--- Sentiment Drivers by Theme ---")
    theme_summary = df.groupby(['theme', 'bert_label']).size().unstack(fill_value=0)
    print(theme_summary)

    # 4. Save
    df.to_csv(output_file, index=False)
    print(f"\nFinal analysis saved to {output_file}")

if __name__ == "__main__":
    main()