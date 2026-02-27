# Language codes
SUPPORTED_LANGUAGES = ["en", "hi", "mr", "bh", "rj"]
LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "mr": "Marathi",
    "bh": "Bhojpuri",
    "rj": "Marwari"
}

# Hate Risk Score ranges
RISK_LEVELS = {
    "low": (0, 25),
    "medium": (25, 50),
    "high": (50, 75),
    "critical": (75, 100)
}

# Database paths
DB_PATHS = {
    "en": "./data/lexicons/english_lexicon.db",
    "hi": "./data/lexicons/hindi_lexicon.db",
    "mr": "./data/lexicons/marathi_lexicon.db",
    "bh": "./data/lexicons/bhojpuri_lexicon.db",
    "rj": "./data/lexicons/marwari_lexicon.db"
}
