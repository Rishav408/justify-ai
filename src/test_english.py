import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.naive_bayes_model import HateSpeechModelAnalyzer

def main():
    print("=========================================")
    print("    JUSTIFY-AI HATE SPEECH TESTER")
    print("=========================================\n")
    
    analyzer = HateSpeechModelAnalyzer('english')
    
    # Paths to the saved models
    model_path = os.path.join(os.path.dirname(__file__), 'models/saved_models/english_nb_model.pkl')
    vec_path = os.path.join(os.path.dirname(__file__), 'models/saved_models/english_vectorizer.pkl')
    
    if not os.path.exists(model_path):
        print("Model not found! Please run the naive_bayes_model.py script to train the model first.")
        return

    print("Loading Trained Brain (Naive Bayes & BoW Vectorizer)...")
    analyzer.load_model(model_path, vec_path)
    print("Model Loaded Successfully!\n")

    print("Type 'exit' or 'quit' to stop.")
    while True:
        user_input = input("\nEnter an English string to analyze: ")
        
        if user_input.lower() in ['exit', 'quit']:
            print("Shutting down tester...")
            break
            
        if not user_input.strip():
            continue
            
        prediction = analyzer.predict(user_input)
        
        if prediction == "hate":
            print(f"🚨 OUTPUT: [HATE SPEECH DETECTED]")
        else:
            print(f"✅ OUTPUT: [NON-HATE SPEECH]")

if __name__ == "__main__":
    main()
