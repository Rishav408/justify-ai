from sklearn.feature_extraction.text import CountVectorizer
import joblib
import os

class FeatureExtractor:
    def __init__(self, use_ngram: bool = True, max_features: int = 5000):
        """
        Initializes the vectorizer.
        By default, extracts both BoW (unigrams) and Bigrams.
        """
        ngram_range = (1, 2) if use_ngram else (1, 1)
        self.vectorizer = CountVectorizer(
            ngram_range=ngram_range,
            max_features=max_features,
            tokenizer=lambda x: x.split(), # Assumes input text is already pre-tokenized and joined by spaces
            preprocessor=lambda x: x,
            token_pattern=None # Needed since we use a custom tokenizer
        )

    def fit_transform(self, texts: list[str]):
        """
        Fits the vectorizer on the training texts and transforms them.
        Returns the vectorized feature matrix and the feature names.
        """
        feature_matrix = self.vectorizer.fit_transform(texts)
        feature_names = self.vectorizer.get_feature_names_out()
        return feature_matrix, feature_names

    def transform(self, texts: list[str]):
        """
        Transforms new text data based on the fitted vocabulary.
        """
        return self.vectorizer.transform(texts)

    def save_vectorizer(self, filepath: str):
        """Saves the fitted vectorizer to disk."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.vectorizer, filepath)

    def load_vectorizer(self, filepath: str):
        """Loads a fitted vectorizer from disk."""
        self.vectorizer = joblib.load(filepath)

if __name__ == "__main__":
    # Quick Test
    extractor = FeatureExtractor()
    sample_corpus = [
        "the quick brown fox",
        "quick brown foxes jump",
        "lazy dog asleep"
    ]
    X, features = extractor.fit_transform(sample_corpus)
    print("--- BoW an N-Grams Test ---")
    print(f"Matrix shape: {X.shape}")
    print(f"Extracted Features: {features[:10]}...")
