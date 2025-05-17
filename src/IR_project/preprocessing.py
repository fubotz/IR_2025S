import re
import spacy


class Preprocessor:
    def __init__(self, stopwords=True, lemmatize=True, preserve_punct=False):
        self.remove_stopwords = stopwords
        self.lemmatize = lemmatize
        self.preserve_punct = preserve_punct
        self.nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])

    def tokenize(self, text):
        """
        Custom tokenizer that ensures whitespace before punctuation.
        E.g., "Hello!" -> ["Hello", "!"]
        """
        spaced = re.sub(r"([^\w\s])", r" \1 ", text)        # add space around punctuation
        spaced = re.sub(r"\s{2,}", " ", spaced)     # remove extra spaces
        return spaced.strip().split()

    def normalize(self, tokens):
        """
        Applies spaCy NLP processing: lowercasing, lemmatization, stopword/punctuation filtering.
        """
        doc = self.nlp(" ".join(tokens))
        normalized = []
        for token in doc:
            if not token.is_alpha and not self.preserve_punct:
                continue
            if self.remove_stopwords and token.is_stop:
                continue
            norm = token.lemma_ if self.lemmatize else token.text
            normalized.append(norm.lower())
        return normalized

    def preprocess_text(self, text):
        tokens = self.tokenize(text)
        return self.normalize(tokens)

    def preprocess_dataset(self, dataset):
        for entry in dataset:
            entry["tokens"] = self.preprocess_text(entry["text"])
        return dataset