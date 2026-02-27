import pytest
import os

@pytest.fixture
def test_data_dir():
    return os.path.join(os.path.dirname(__file__), "fixtures")

@pytest.fixture
def sample_english_text():
    return "This is a hateful message targeting a group of people."

@pytest.fixture
def sample_hindi_text():
    return "यह एक घृणास्पद संदेश है।"
