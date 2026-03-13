from langdetect import detect
from src.pipelines.english_pipeline import run_english_pipeline
from src.pipelines.hindi_pipeline import run_hindi_pipeline

def route_language(text):
    lang = detect(text)

    if lang == "en":
        return run_english_pipeline(text)
    elif lang == "hi" or lang == "ne" or lang == "mr": # langdetect might detect related
        return run_hindi_pipeline(text)
    else:
        return {
            "error": "Language not supported",
            "detected": lang
        }
