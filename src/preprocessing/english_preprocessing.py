import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
import string

# Ensure NLTK resources are available (will download if missing)
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
    nltk.data.find('taggers/averaged_perceptron_tagger')
    nltk.data.find('taggers/averaged_perceptron_tagger_eng')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('averaged_perceptron_tagger_eng')
    nltk.download('omw-1.4') # Added for lemmatizer stability

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
