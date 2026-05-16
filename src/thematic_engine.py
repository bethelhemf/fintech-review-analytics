import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import pipeline

class ThematicEngine:
    def __init__(self):
        # We use a Zero-Shot Classifier to map reviews to business themes automatically
        print("Initializing Zero-Shot Classifier for thematic mapping...")
        self.classifier = pipeline("zero-shot-classification", 
                                   model="facebook/bart-large-mnli", 
                                   device=-1)
        
        # Predefined business themes for Ethiopian Banking
        self.candidate_themes = [
            "Account Access & OTP",
            "Transaction Performance",
            "UI & Design",
            "Customer Support",
            "Feature Requests"
        ]

    def get_top_keywords(self, texts, n=10):
        """Extract significant n-grams using TF-IDF."""
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_features=n)
        tfidf_matrix = vectorizer.fit_transform(texts)
        return vectorizer.get_feature_names_out()

    def classify_theme(self, text):
        """Assign the most likely business theme to a review."""
        result = self.classifier(text, self.candidate_themes, multi_label=False)
        return result['labels'][0] # Return the top theme