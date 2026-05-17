from transformers import pipeline
class SentimentEngine:
    def __init__(self):
        self.pipe = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    def get_bert_sentiment(self, texts):
        res = self.pipe(texts, truncation=True)
        return [r["label"] for r in res], [r["score"] for r in res]
