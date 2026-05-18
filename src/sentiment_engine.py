import pandas as pd
from transformers import pipeline
from textblob import TextBlob

class SentimentEngine:
    def __init__(self, model_name="distilbert-base-uncased-finetuned-sst-2-english"):
        print(f"Initializing {model_name}...")
        # Use GPU (device=0) if available, else CPU (device=-1)
        self.transformer_pipeline = pipeline("sentiment-analysis", model=model_name, device=-1)

    def get_bert_sentiment(self, texts, neutral_threshold=0.7):
        """Classifies text using DistilBERT with a custom neutral threshold."""
        results = self.transformer_pipeline(texts, truncation=True)
        
        final_labels = []
        scores = []
        
        for res in results:
            label = res['label'] # POSITIVE or NEGATIVE
            score = res['score']
            
            # If the model is not confident, call it NEUTRAL
            if score < neutral_threshold:
                final_labels.append("NEUTRAL")
            else:
                final_labels.append(label)
            scores.append(score)
            
        return final_labels, scores

    def get_textblob_sentiment(self, text):
        """Rule-based sentiment score using TextBlob."""
        polarity = TextBlob(str(text)).sentiment.polarity
        if polarity > 0.1:
            return "POSITIVE", polarity
        elif polarity < -0.1:
            return "NEGATIVE", polarity
        else:
            return "NEUTRAL", polarity