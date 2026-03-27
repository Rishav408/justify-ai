from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langdetect import detect
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.models.naive_bayes_model import HateSpeechModelAnalyzer
from src.ner.ner_extractor import NERExtractor

router = APIRouter()

class AnalyzeRequest(BaseModel):
    text: str
    language: str = None # Optional: auto-detect if not provided

# Cache analyzers per language to avoid reloading models on every request
analyzers = {}
ner_extractors = {}

def get_analyzer(lang: str):
    if lang not in analyzers:
        try:
            analyzer = HateSpeechModelAnalyzer(lang)
            # Paths to saved models (relative to this file location or project root)
            model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../models/saved_models/{lang}_nb_model.pkl'))
            vec_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../models/saved_models/{lang}_vectorizer.pkl'))
            
            if not os.path.exists(model_path):
                 return None
                 
            analyzer.load_model(model_path, vec_path)
            analyzers[lang] = analyzer
        except Exception:
            return None
    return analyzers.get(lang)

def get_ner_extractor(lang: str):
    if lang not in ner_extractors:
        ner_extractors[lang] = NERExtractor(lang)
    return ner_extractors.get(lang)

@router.post("/analyze")
async def analyze_text(request: AnalyzeRequest):
    text = request.text
    if not text.strip():
        raise HTTPException(status_code=400, detail="Empty text provided.")
    
    # 1. Language Detection
    lang = request.language
    if not lang:
        try:
            detected = detect(text)
            # Map langdetect codes to our project codes
            lang_map = {'en': 'english', 'hi': 'hindi', 'mr': 'marathi'}
            lang = lang_map.get(detected, 'english') # Default to english if detected is uncertain
        except:
            lang = 'english'

    # 2. Get the Brain (Model)
    analyzer = get_analyzer(lang)
    if not analyzer:
         # Fallback to English if the specific language model is missing
         lang = 'english'
         analyzer = get_analyzer(lang)

    # 3. Hate Speech Classification (Phase 3 logic)
    prediction = analyzer.predict(text)
    
    # 4. Detailed Preprocessing Info (CCNLP Concepts)
    preproc_results = analyzer.preprocessor.preprocess(text)
    
    # 5. NER Extraction (CCNLP Concepts)
    ner = get_ner_extractor(lang)
    entities = ner.extract_entities(text)

    return {
        "text": text,
        "language": lang,
        "hate_speech_label": prediction,
        "analysis": {
            "tokens": preproc_results.get('tokens', []),
            "stemmed": preproc_results.get('stemmed', []),
            "lemmatized": preproc_results.get('lemmatized', []),
            "pos_tags": preproc_results.get('pos_tags', []),
            "named_entities": entities
        },
        "version": "1.5 - Syllabus Logic"
    }

@router.get("/")
async def health_check():
    return {"status": "ok", "message": "Justify-AI Backend (Syllabus Mode) is online."}
