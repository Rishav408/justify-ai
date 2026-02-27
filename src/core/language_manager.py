from langdetect import detect
from src.core.config_loader import ConfigLoader

class LanguageManager:
    def __init__(self):
        self.config_loader = ConfigLoader()
    
    def detect_language(self, text):
        """Detect language from text"""
        try:
            lang_code = detect(text)
            # Map language codes
            code_mapping = {
                'en': 'en', 'hi': 'hi', 'mr': 'mr'
                # Add bhojpuri, marwari mappings if available
            }
            return code_mapping.get(lang_code, 'en')
        except:
            return 'en'  # Default to English
    
    def load_language_resources(self, language_code):
        """Load all resources for a language"""
        config = self.config_loader.load_language_config(language_code)
        return config
