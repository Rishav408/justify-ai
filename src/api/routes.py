from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langdetect import detect
import os
import sys
import re
import math

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.models.naive_bayes_model import HateSpeechModelAnalyzer
from src.ner.ner_extractor import NERExtractor
from src.preprocessing.english_preprocessing import EnglishPreprocessor
from src.lexicon.lexicon_matcher import LexiconMatcher

router = APIRouter()

class AnalyzeRequest(BaseModel):
    text: str
    language: str = None # Optional: auto-detect if not provided

# Phase 1: define unified analysis schema + language coverage priority.
# This is a foundation for upcoming lexicon/causal/bias/risk implementations.
# Expanded to all currently supported languages to avoid confusion.
LANGUAGE_COVERAGE_PRIORITY = ["english", "hindi", "marathi", "bhojpuri", "marwari"]

def _empty_analysis_bundle() -> dict:
    """Baseline placeholder bundle so frontend/backend share a stable schema."""
    return {
        "lexicon_hits": [],          # [{term, severity, count, spans?}, ...]
        "causality_relations": [],   # [{cause, effect, relation, confidence}, ...]
        "bias_metrics": {},          # {dimension: score, ...}
        "risk": {                    # {score, level, breakdown}
            "score": None,
            "level": "unknown",
            "breakdown": {
                "lexical": None,
                "causal": None,
                "bias": None,
            }
        },
    }

# Cache analyzers per language to avoid reloading models on every request
analyzers = {}
ner_extractors = {}
english_preprocessor = EnglishPreprocessor()
lexicon_matcher = LexiconMatcher()

def _count_matches(text: str, patterns: list[str]) -> int:
    count = 0
    lowered = text.lower()
    for pattern in patterns:
        try:
            count += len(re.findall(pattern, lowered))
        except re.error:
            if pattern in lowered:
                count += 1
    return count

def _derive_metadata(text: str, label: str, language: str, analysis: dict) -> dict:
    hate_patterns = [
        r'\bkill\b', r'\bdie\b', r'\bremove\b', r'\bthrow out\b', r'\btraitor\b',
        r'\u092e\u093e\u0930', r'\u0928\u093f\u0915\u093e\u0932', r'\u092d\u0917\u093e', r'\u0915\u0941\u091a\u0932'
    ]
    offensive_patterns = [
        r'\bidiot\b', r'\bstupid\b', r'\bmoron\b', r'\bfool\b',
        r'\u092c\u0947\u0935\u0915\u0942\u092b', r'\u0917\u0927\u093e', r'\u0928\u093f\u0915\u092e\u094d\u092e\u093e'
    ]
    strong_patterns = [
        r'\bkill\b', r'\bdie\b', r'\bdestroy\b', r'\u092e\u093e\u0930', r'\u0915\u0941\u091a\u0932', r'\u0916\u0924\u094d\u092e'
    ]
    call_to_action_patterns = [
        r'\bkill\b', r'\bremove\b', r'\bexpel\b', r'\bbanish\b', r'\bhang\b', r'\bshoot\b',
        r'\u092e\u093e\u0930', r'\u0928\u093f\u0915\u093e\u0932', r'\u092d\u0917\u093e'
    ]
    group_map = [
        ('gender', [r'\bwomen\b', r'\bfemale\b', r'\u0932\u0921\u093c\u0915\u0940', r'\u0914\u0930\u0924']),
        ('religion', [r'\bmuslim\b', r'\bhindu\b', r'\breligion\b', r'\u092e\u091c\u0939\u092c', r'\u0927\u0930\u094d\u092e']),
        ('caste', [r'\bcaste\b', r'\u0926\u0932\u093f\u0924', r'\u091c\u093e\u0924']),
        ('nationality', [r'\bimmigrant\b', r'\bforeigner\b', r'\u0935\u093f\u0926\u0947\u0936\u0940', r'\u092a\u0930\u0926\u0947\u0938\u0940']),
        ('political', [r'\bparty\b', r'\bgovernment\b', r'\belection\b', r'\u0938\u0930\u0915\u093e\u0930', r'\u092a\u093e\u0930\u094d\u091f\u0940']),
    ]

    hate_hits = _count_matches(text, hate_patterns)
    offensive_hits = _count_matches(text, offensive_patterns)
    strong_hits = _count_matches(text, strong_patterns)

    severity = 'none'
    if label in ('hate', 'offensive'):
        if strong_hits > 0 or hate_hits > 2:
            severity = 'severe'
        elif hate_hits > 0 or offensive_hits > 1:
            severity = 'moderate'
        else:
            severity = 'mild'

    target_group = 'none'
    for key, patterns in group_map:
        if target_group == 'none' and _count_matches(text, patterns) > 0:
            target_group = key

    entity_count = len(analysis.get('named_entities') or [])
    if label != 'non_hate' and target_group == 'none' and entity_count > 0:
        target_group = 'individual'

    if label != 'non_hate' and target_group == 'none':
        you_ref = _count_matches(text, [r'\byou\b', r'\btu\b', r'\btum\b', r'\u0924\u0942', r'\u0924\u0941\u092e']) > 0
        target_group = 'individual' if you_ref else 'community'

    target_type = 'none'
    if target_group == 'individual':
        target_type = 'individual'
    elif target_group != 'none':
        target_type = 'community'

    is_sarcasm = _count_matches(text, [r'yeah right', r'so great', r'\u0935\u093e\u0939 \u0915\u094d\u092f\u093e', r'\u0939\u093e\u0902 \u0939\u093e\u0902']) > 0
    is_implicit = _count_matches(text, [r'those people', r'you know them', r'\u0935\u094b \u0932\u094b\u0917', r'\u090f\u0948\u0938\u0947 \u0932\u094b\u0917']) > 0
    directness = 'none' if label == 'non_hate' else 'indirect' if is_implicit else 'direct'
    call_to_action = _count_matches(text, call_to_action_patterns) > 0

    tone = 'neutral'
    if label == 'hate':
        tone = 'sarcastic' if is_sarcasm else 'aggressive'
    elif label == 'offensive':
        tone = 'dismissive'

    emotion = 'none'
    if label == 'hate':
        emotion = 'anger'
    elif label == 'offensive':
        emotion = 'disgust'
    elif label == 'health_issue':
        emotion = 'fear'

    platform = 'social_media' if _count_matches(text, [r'\btweet\b', r'\bpost\b', r'@', r'#']) > 0 else 'general'
    domain = 'general'
    region = 'global'
    if language in ('hindi', 'marathi'):
        region = 'india'
    elif language in ('bhojpuri', 'marwari'):
        region = 'rural_india'

    profanity_count = 0
    if language == 'english':
        try:
            profanity_count = english_preprocessor.get_profanity_count(text)
        except Exception:
            profanity_count = 0

    return {
        "severity": severity,
        "target_group": target_group,
        "target_type": target_type,
        "directness": directness,
        "call_to_action": call_to_action,
        "tone": tone,
        "emotion": emotion,
        "profanity_count": profanity_count,
        "is_sarcasm": is_sarcasm,
        "is_implicit": is_implicit,
        "platform": platform,
        "domain": domain,
        "region": region,
    }

def _calibrate_confidence(raw_confidence: float | None, language: str) -> tuple[float | None, str, dict]:
    if raw_confidence is None:
        return None, "unknown", {"temperature": None, "language": language}
    # Temperature scaling to soften overconfident probabilities.
    # temp > 1.0 reduces confidence; temp < 1.0 increases.
    profile_map = {
        "english": 1.25,
        "hindi": 1.4,
        "marathi": 1.4,
        "bhojpuri": 1.55,
        "marwari": 1.55,
    }
    temp = profile_map.get(language, 1.35)
    eps = 1e-6
    p = min(max(raw_confidence, eps), 1 - eps)
    logit = math.log(p / (1 - p))
    calibrated = 1 / (1 + math.exp(-logit / temp))
    calibrated = max(0.5, min(0.99, calibrated))

    if calibrated < 0.65:
        band = "low"
    elif calibrated < 0.80:
        band = "medium"
    elif calibrated < 0.90:
        band = "high"
    else:
        band = "very_high"

    return float(round(calibrated, 4)), band, {"temperature": temp, "language": language}

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
    try:
        prediction, confidence = analyzer.predict_with_confidence(text)
    except Exception:
        prediction = analyzer.predict(text)
        confidence = None
    
    # 4. Detailed Preprocessing Info (CCNLP Concepts)
    preproc_results = analyzer.preprocessor.preprocess(text)
    
    # 5. NER Extraction (CCNLP Concepts)
    ner = get_ner_extractor(lang)
    try:
        entities = ner.extract_entities(text)
    except Exception:
        # NER failures should not break label inference endpoint.
        entities = []

    metadata = _derive_metadata(text, prediction, lang, {
        "named_entities": entities,
        "tokens": preproc_results.get('tokens', [])
    })
    calibrated_confidence, confidence_band, calibration_profile = _calibrate_confidence(confidence, lang)
    analysis_bundle = _empty_analysis_bundle()

    # Phase 2: Lexicon matching (lightweight seed lists per language)
    try:
        analysis_bundle["lexicon_hits"] = lexicon_matcher.match(text, lang)
    except Exception:
        analysis_bundle["lexicon_hits"] = []

    return {
        "text": text,
        "language": lang,
        "language_coverage_priority": LANGUAGE_COVERAGE_PRIORITY,
        "hate_speech_label": prediction,
        "confidence": confidence,
        "confidence_calibrated": calibrated_confidence,
        "confidence_band": confidence_band,
        "confidence_profile": calibration_profile,
        "metadata": metadata,
        "lexicon_hits": analysis_bundle["lexicon_hits"],
        "causality_relations": analysis_bundle["causality_relations"],
        "bias_metrics": analysis_bundle["bias_metrics"],
        "risk": analysis_bundle["risk"],
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
