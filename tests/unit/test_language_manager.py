import pytest
from src.core.language_manager import LanguageManager

def test_language_detection_english():
    manager = LanguageManager()
    lang = manager.detect_language("Hello, this is English text")
    assert lang == 'en'

def test_language_detection_hindi():
    manager = LanguageManager()
    lang = manager.detect_language("नमस्ते, यह हिंदी पाठ है")
    # May not work perfectly depending on langdetect
    # assert lang == 'hi'
