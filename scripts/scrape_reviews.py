from google_play_scraper import Sort, reviews
import pandas as pd
def scrape():
    res, _ = reviews("com.combanketh.mobilebanking", count=500, lang="en", country="et")
    df = pd.DataFrame(res)
    df.to_csv("data/raw/raw_bank_reviews.csv", index=False)
    print("✅ Scraped 500 reviews")
if __name__ == "__main__":
    scrape()
