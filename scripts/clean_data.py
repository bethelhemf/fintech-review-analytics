import pandas as pd
import os

def preprocess_data():
    raw_path = 'data/raw/raw_bank_reviews.csv'
    cleaned_path = 'data/cleaned_bank_reviews.csv'
    
    if not os.path.exists(raw_path):
        print("Raw data file not found. Please run the scraper first.")
        return

    # Load data
    df = pd.read_csv(raw_path)
    initial_count = len(df)
    print(f"Initial record count: {initial_count}")

    # 1. Remove duplicate reviews 
    # If review_id exists, use it. Otherwise, use review_text.
    if 'review_id' in df.columns:
        df = df.drop_duplicates(subset=['review_id'])
    else:
        # Fallback: remove if same user wrote same text for same bank
        df = df.drop_duplicates(subset=['review_text', 'bank_name'])
        
    after_duplicates = len(df)
    print(f"Removed {initial_count - after_duplicates} duplicates.")

    # 2. Handle missing values
    df = df.dropna(subset=['review_text', 'rating'])
    after_nulls = len(df)
    print(f"Dropped {after_duplicates - after_nulls} rows with missing text or ratings.")

    # 3. Normalize dates to YYYY-MM-DD
    df['review_date'] = pd.to_datetime(df['review_date']).dt.strftime('%Y-%m-%d')

    # 4. Select and rename columns (Matching your requirement exactly)
    cleaned_df = df[[
        'review_text', 
        'rating', 
        'review_date', 
        'bank_name', 
        'source'
    ]].rename(columns={
        'review_text': 'review',
        'review_date': 'date',
        'bank_name': 'bank'
    })

    # 5. Save cleaned dataset
    cleaned_df.to_csv(cleaned_path, index=False)
    print(f"\nSuccess! Cleaned data saved to {cleaned_path}")
    print(f"Final record count: {len(cleaned_df)}")

if __name__ == "__main__":
    preprocess_data()