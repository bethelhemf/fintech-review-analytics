### **Scraping Methodology**
- **Data Source:** Google Play Store.
- **Volume:** Collected 500 reviews per bank (Total: 1,500) to ensure a high-confidence sample.
- **Language/Region:** Primary focus on `lang='en'` and `country='et'` to capture local Ethiopian feedback.
- **Fallback:** Implemented a global region fallback for apps with restricted local visibility.
- **Tools:** `google-play-scraper` library for Python.