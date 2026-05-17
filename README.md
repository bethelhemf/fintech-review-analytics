## **Implementation Details & Methods**

### **Task 1: Data Collection & Preprocessing**
- **Method:** Used `google-play-scraper` to collect 1,200+ reviews.
- **Assumptions:** We assumed English-language reviews provided the most reliable signal for sentiment analysis in this initial phase.
- **Cleaning:** Implemented **spaCy** for lemmatization and tokenization. We removed stop-words and duplicates to ensure data integrity.

### **Task 2: Sentiment & Thematic Analysis**
- **Sentiment Model:** `distilbert-base-uncased-finetuned-sst-2-english`. 
- **Thematic Model:** Zero-Shot Classification using `facebook/bart-large-mnli` (or `distilbert-mnli`).
- **Logic:** Used a **confidence threshold of 0.7** to define "Neutral" sentiment, preventing the binary model from forcing a positive/negative label on ambiguous feedback.

### **Task 3: Database Engineering**
- **Schema:** Relational design with a `banks` dimension table and a `reviews` fact table.
- **Tools:** **SQLAlchemy** for ORM and **psycopg2** as the database driver.
- **Automation:** The `DBManager` class automatically handles bank ID mapping and data ingestion.

### **Task 4: Strategic Visualization**
- **Tools:** Matplotlib and Seaborn.
- **Outputs:** Stacked bar charts for sentiment, frequency plots for themes, and boxplots for rating distribution.