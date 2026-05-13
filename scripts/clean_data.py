"""
Preprocessing script for Omega Consultancy.
This script cleans raw Play Store data, removes duplicates, and 
standardizes the format for downstream analysis.
"""

import pandas as pd
import os

def preprocess_data():
    # Define file paths
    raw_path = 'data/raw/raw_bank_reviews.csv'
    cleaned_path = 'data/cleaned_bank_reviews.csv'
    
    # Ensure raw data exists before proceeding
    if not os.path.exists(raw_path):
        print("Error: Raw data file not found.")
        return

    # Load the raw dataset
    df = pd.read_csv(raw_path)
    print(f"Initial record count: {len(df)}")

    # --- STEP 1: Duplicate Removal ---
    # We use 'review_id' if available, otherwise we use the review text itself.
    # This prevents counting the same customer complaint twice.
    if 'review_id' in df.columns:
        df = df.drop_duplicates(subset=['review_id'])
    else:
        df = df.drop_duplicates(subset=['review_text', 'bank_name'])
    print(f"Count after removing duplicates: {len(df)}")

    # --- STEP 2: Handling Missing Values ---
    # Reviews without text or ratings provide no value to sentiment analysis.
    df = df.dropna(subset=['review_text', 'rating'])
    print(f"Count after dropping nulls: {len(df)}")

    # --- STEP 3: Date Normalization ---
    # Convert various date formats into a standard YYYY-MM-DD format for time-series analysis.
    df['review_date'] = pd.to_datetime(df['review_date']).dt.strftime('%Y-%m-%d')

    # --- STEP 4: Column Standardization ---
    # Selecting and renaming columns to match the project requirements exactly.
    # Required: review, rating, date, bank, source.
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

    # --- STEP 5: Data Export ---
    # Save as a clean CSV. Note: This file is ignored by Git via .gitignore.
    cleaned_df.to_csv(cleaned_path, index=False)
    print(f"\nSuccess! Final count: {len(cleaned_df)}")

if __name__ == "__main__":
    preprocess_data()