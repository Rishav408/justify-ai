import re

class HindiPreprocessor:
    def __init__(self):
        # Traditional stopword list for Hindi (Can be expanded)
        self.stop_words = set([
            'है', 'हैं', 'को', 'में', 'से', 'का', 'की', 'के', 'पर', 'कि',
            'तो', 'ही', 'किया', 'था', 'थी', 'थे', 'सब', 'कर', 'गया', 'गई',
            'गए', 'हो', 'हुआ', 'हुई', 'हुए', 'भी', 'और', 'या', 'इस', 'उस',
            'इन', 'उन', 'जो', 'तो', 'जब', 'तब', 'अदि'
        ])

    def preprocess(self, text: str) -> dict:
        """
        Runs simple Hindi preprocessing: Cleaning (regex) + Split Tokenization.
        """
        # 1. Clean extra spaces and non-word characters (preserving Devanagari)
        # Keeps Devanagari (0900-097F) and basic spaces
        clean_text = re.sub(r'[^\u0900-\u097F\s]', '', text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        # 2. Tokenization (basic whitespace based)
        tokens = clean_text.split()
        
        # 3. Stopword Removal
        clean_tokens = [t for t in tokens if t not in self.stop_words]
        
        return {
            "original_text": text,
            "tokens": tokens,
            "clean_tokens": clean_tokens,
            # We skip stemming/lemmatization for Hindi (out of scope for NLTK foundation)
            "stemmed": clean_tokens, 
            "lemmatized": clean_tokens
        }

if __name__ == "__main__":
    # Quick Test
    preprocessor = HindiPreprocessor()
    sample_text = "यह एक बहुत अच्छा प्रोजेक्ट है!"
    results = preprocessor.preprocess(sample_text)
    
    print("--- Hindi Preprocessing Test ---")
    for key, value in results.items():
        print(f"{key.capitalize()}: {value}")
