Sentiment Analysis Rationale:

    Primary Model: distilbert-base-uncased-finetuned-sst-2-english. We selected this because it is a Transformer model capable of understanding complex sentence structures and context that simpler models miss.

    Neutral Handling: Since the chosen model is binary (Pos/Neg), we implemented a confidence threshold of 0.7. Scores below this are categorized as NEUTRAL to ensure we don't force a sentiment on ambiguous reviews.

    Baseline Comparison: TextBlob was used as a rule-based baseline. This allows us to identify reviews where the Transformer might be "over-thinking" compared to a simple word-count approach.

    Thematic Grouping Logic:
We categorized feedback into 5 overarching themes based on common fintech pain points in the Ethiopian market:

    Account Access & OTP: Captures issues with registration, password resets, and the reliability of SMS/OTP codes.

    Transaction Performance: Focuses on speed, failed transfers, and "money deducted but not reached" complaints.

    UI & Design: Covers feedback on the look-and-feel, ease of navigation, and app updates.

    Customer Support: Captures mentions of bank branches, call centers, and staff responsiveness.

    Feature Requests: Groups requests for new services (e.g., "International transfers," "Utility payments").

Discovery Method: We used TF-IDF (Term Frequency-Inverse Document Frequency) to find bank-specific keywords and Zero-Shot Classification (BART model) to objectively map reviews to these categories without manual labeling.