import os
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Adjust imports to local packages
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.preprocessing.english_preprocessing import EnglishPreprocessor
from src.preprocessing.hindi_preprocessing import HindiPreprocessor
from src.preprocessing.marathi_preprocessing import MarathiPreprocessor
from src.preprocessing.bhojpuri_preprocessing import BhojpuriPreprocessor
from src.preprocessing.marwari_preprocessing import MarwariPreprocessor
from src.features.feature_extractor import FeatureExtractor

class HateSpeechModelAnalyzer:
    def __init__(self, language: str = 'english'):
        self.language = language
        self.model = MultinomialNB()
        self.preprocessor = None
        
        # Select correct preprocessor
        if self.language == 'english':
            self.preprocessor = EnglishPreprocessor()
        elif self.language == 'hindi':
            self.preprocessor = HindiPreprocessor()
        elif self.language == 'marathi':
            self.preprocessor = MarathiPreprocessor()
        elif self.language == 'bhojpuri':
            self.preprocessor = BhojpuriPreprocessor()
        elif self.language == 'marwari':
            self.preprocessor = MarwariPreprocessor()
        else:
            raise NotImplementedError(f"Language {language} is not supported.")
            
        self.feature_extractor = FeatureExtractor(use_ngram=True, max_features=5000)

    def load_and_preprocess_data(self, csv_path: str, label_col: str = 'label'):
        """Loads dataset and applies tokenization, stemming, etc."""
        print(f"Loading dataset from {csv_path}...")
        df = pd.read_csv(csv_path)
        
        print("Preprocessing texts...")
        processed_texts = []
        for text in df['text']:
            # We use 'stemmed' tokens united by spaces to feed the CountVectorizer
            result = self.preprocessor.preprocess(text)
            processed_string = " ".join(result['stemmed'])
            processed_texts.append(processed_string)
            
        return processed_texts, df[label_col].values

    def train(self, csv_path: str, model_save_path: str, vectorizer_save_path: str):
        """Trains the Naive Bayes model on the dataset via BoW/N-Grams."""
        texts, labels = self.load_and_preprocess_data(csv_path, label_col='label')
        
        print("Extracting Features (BoW + N-grams)...")
        # Phase 2 execution
        X_train, feature_names = self.feature_extractor.fit_transform(texts)
        
        print(f"Training Multinomial Naive Bayes model on {X_train.shape[0]} samples...")
        self.model.fit(X_train, labels)
        
        # Save artifacts
        os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
        joblib.dump(self.model, model_save_path)
        self.feature_extractor.save_vectorizer(vectorizer_save_path)
        
        # Evaluate training performance
        predictions = self.model.predict(X_train)
        print("\n--- Model Training Results ---")
        print(f"Accuracy: {accuracy_score(labels, predictions):.4f}")
        print(classification_report(labels, predictions))
        
    def load_model(self, model_path: str, vectorizer_path: str):
        """Loads trained artifacts for predicting new data."""
        self.model = joblib.load(model_path)
        self.feature_extractor.load_vectorizer(vectorizer_path)

    def predict(self, text: str):
        """Processes a single string and returns its hate-speech label."""
        # Preprocess
        result = self.preprocessor.preprocess(text)
        processed_string = " ".join(result['stemmed'])
        
        # Vectorize
        features = self.feature_extractor.transform([processed_string])
        
        # Predict
        prediction = self.model.predict(features)[0]
        return prediction

if __name__ == "__main__":
    languages = ['english', 'hindi', 'marathi', 'bhojpuri', 'marwari']
    
    for lang in languages:
        print(f"\n{'='*40}")
        print(f" TRAINING MODEL FOR: {lang.upper()}")
        print(f"{'='*40}")
        
        analyzer = HateSpeechModelAnalyzer(lang)
        
        # Paths
        dataset_path = os.path.join(os.path.dirname(__file__), f'../datasets/{lang}.csv')
        model_out = os.path.join(os.path.dirname(__file__), f'saved_models/{lang}_nb_model.pkl')
        vec_out = os.path.join(os.path.dirname(__file__), f'saved_models/{lang}_vectorizer.pkl')
        
        # Train
        if os.path.exists(dataset_path):
            analyzer.train(dataset_path, model_out, vec_out)
        else:
            print(f"Dataset for {lang} not found at {dataset_path}")
    
    print("\nALL MODELS TRAINED AND SAVED SUCCESSFULLY.")
