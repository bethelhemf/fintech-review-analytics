import pandas as pd
from google_play_scraper import Sort, reviews
import os

# 1. Updated App IDs based on your links
APPS = {
    'Commercial Bank of Ethiopia': 'com.combanketh.mobilebanking',
    'Bank of Abyssinia': 'com.boa.boaMobileBanking', # Updated from your link
    'Dashen Bank': 'com.dashen.dashensuperapp'
}

def scrape_bank_reviews():
    all_reviews = []

    for bank_name, app_id in APPS.items():
        print(f"Starting scrape for {bank_name} ({app_id})...")
        
        # Try scraping with Ethiopia filter first
        rvws, _ = reviews(
            app_id,
            lang='en',
            country='et',
            sort=Sort.NEWEST,
            count=500
        )

        # Fallback: If 0 reviews found, try without the country restriction
        if len(rvws) == 0:
            print(f"Warning: 0 reviews found for {bank_name} in 'et'. Trying global search...")
            rvws, _ = reviews(
                app_id,
                lang='en',
                sort=Sort.NEWEST,
                count=500
            )

        for r in rvws:
            all_reviews.append({
                'review_text': r['content'],
                'rating': r['score'],
                'review_date': r['at'],
                'bank_name': bank_name,
                'source': 'Google Play'
            })
        
        print(f"Successfully collected {len(rvws)} reviews for {bank_name}.")

    df = pd.DataFrame(all_reviews)
    
    if not df.empty:
        os.makedirs('data/raw', exist_ok=True)
        df.to_csv('data/raw/raw_bank_reviews.csv', index=False)
        print(f"\nSuccess! Total Reviews: {len(df)}")
    else:
        print("\nNo reviews collected. Check App IDs or Internet connection.")

if __name__ == "__main__":
    scrape_bank_reviews()