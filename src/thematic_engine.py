from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

class ThematicEngine:
    def __init__(self):
        print("Initializing Zero-Shot Classifier...")
        # Use a smaller model for speed if needed
        self.classifier = pipeline("zero-shot-classification", 
                                   model="typeform/distilbert-base-uncased-mnli", 
                                   device=-1)
        
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
        vectorizer.fit_transform(texts)
        return vectorizer.get_feature_names_out()

    def classify(self, text):
        """Assign the most likely business theme. This matches the pipeline call."""
        if not text or str(text).strip() == "":
            return "General"
        result = self.classifier(str(text), self.candidate_themes, multi_label=False)
        return result['labels'][0]