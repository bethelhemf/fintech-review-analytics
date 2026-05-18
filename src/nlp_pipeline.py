import spacy

class NLPPipeline:
    def __init__(self):
        # Load the small English model
        self.nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

    def process_text(self, text):
        """
        Tokenizes, removes stop-words, and lemmatizes the input text.
        Example: "crashes" -> "crash", "the" -> removed.
        """
        if not isinstance(text, str):
            return ""
        
        doc = self.nlp(text.lower())
        
        # Keep tokens that are:
        # 1. Not stop words
        # 2. Not punctuation
        # 3. Alphabetical (removes numbers/emojis)
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and token.is_alpha]
        
        return " ".join(tokens)