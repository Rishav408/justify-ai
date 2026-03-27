import re

class BhojpuriPreprocessor:
    def __init__(self):
        # Basic Bhojpuri stopwords
        self.stop_words = set(['बा', 'बवे', 'हउवे', 'हमार', 'तहार', 'का', 'के', 'में', 'ले', 'से', 'गइल', 'आएल'])

    def preprocess(self, text: str) -> dict:
        clean_text = re.sub(r'[^\u0900-\u097F\s]', '', text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        tokens = clean_text.split()
        clean_tokens = [t for t in tokens if t not in self.stop_words]
        return {
            "original_text": text,
            "tokens": tokens,
            "clean_tokens": clean_tokens,
            "stemmed": clean_tokens,
            "lemmatized": clean_tokens
        }

if __name__ == "__main__":
    preprocessor = BhojpuriPreprocessor()
    print(preprocessor.preprocess("हमार सीना में दर्द बा"))
