import contextlib
import io
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
import string

def _safe_download(package: str) -> None:
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            nltk.download(package, quiet=True)
    except Exception:
        pass


def _ensure_nltk_resources() -> None:
    required_paths = [
        'tokenizers/punkt',
        'corpora/stopwords',
        'corpora/wordnet',
        'taggers/averaged_perceptron_tagger',
        'taggers/averaged_perceptron_tagger_eng',
    ]
    missing = False
    for path in required_paths:
        try:
            nltk.data.find(path)
        except LookupError:
            missing = True

    if not missing:
        return

    for package in [
        'punkt',
        'stopwords',
        'wordnet',
        'averaged_perceptron_tagger',
        'averaged_perceptron_tagger_eng',
        'omw-1.4',
    ]:
        _safe_download(package)


_ensure_nltk_resources()

class EnglishPreprocessor:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.profane_words = {
            'bastard', 'bitch', 'bloody', 'crap', 'damn', 'dick', 'fool',
            'garbage', 'idiot', 'jerk', 'moron', 'nasty', 'shit', 'trash'
        }
        # Adding some basic punctuation to stopwords just in case
        self.stop_words.update(list(string.punctuation))

    def get_profanity_count(self, text: str) -> int:
        """Counts profane tokens using a small hardcoded lexicon."""
        tokens = word_tokenize(text.lower())
        return sum(1 for token in tokens if token in self.profane_words)

    def preprocess(self, text: str) -> dict:
        """
        Runs the full English NLTK preprocessing pipeline.
        Returns a dictionary containing all classical NLP extractions.
        """
        # 1. Lowercase text
        lower_text = text.lower()
        
        # 2. Tokenization
        tokens = word_tokenize(lower_text)
        
        # 3. Stopword Removal & basic punctuation cleaning
        clean_tokens = [t for t in tokens if t not in self.stop_words and t.isalpha()]
        
        # 4. Stemming
        stemmed = [self.stemmer.stem(t) for t in clean_tokens]
        
        # 5. Lemmatization
        lemmatized = [self.lemmatizer.lemmatize(t) for t in clean_tokens]
        
        # 6. POS Tagging (done on original tokens to preserve grammatical context)
        pos_tags = nltk.pos_tag(tokens)

        return {
            "original_text": text,
            "tokens": tokens,
            "clean_tokens": clean_tokens,
            "stemmed": stemmed,
            "lemmatized": lemmatized,
            "pos_tags": pos_tags
        }

if __name__ == "__main__":
    # Quick Test
    preprocessor = EnglishPreprocessor()
    sample_text = "The quick brown foxes are jumping over the lazy dogs!"
    results = preprocessor.preprocess(sample_text)
    
    print("--- English Preprocessing Test ---")
    for key, value in results.items():
        print(f"{key.capitalize()}: {value}")
