def run_hindi_pipeline(text):
    return {
        "language": "hindi",
        "cleaned_text": text,
        "tokens":text.split(),
        "pos_tags": []
    }
