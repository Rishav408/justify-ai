# Justify-AI

An Explainable Multilingual NLP Framework implemented purely using foundational, statistical NLP methodologies.

## Core Objective
This project is built explicitly to fulfill the **CCNLP Laboratory Syllabus Implementation**. All processing avoids deep-learning transformer models in favor of rigorous, classical NLP logic.

### Implemented Syllabus Concepts:
- Tokenization 
- Stemming
- Lemmatization
- Stopword Removal
- POS Tagging
- N-grams
- Bag of Words
- Named Entity Recognition (NLTK Chunking)
- Sentiment Analysis (Naive Bayes)
- Speech-to-Text & Text-to-Speech

## 🌍 Multilingual Strategy
We officially support pipelines for **5 languages**:
1. **English**: Full pipeline support acting as the primary system baseline.
2. **Hindi**: Basic extended support.
3. **Marathi**: Low-resource focus (Custom datasets).
4. **Bhojpuri**: Low-resource focus (Custom datasets).
5. **Marwari**: Low-resource focus (Custom datasets).

## 🚀 Technology Stack
- `nltk`: Core foundational NLP processing and targeted extractions.
- `scikit-learn`: N-Grams, Bag-of-Words vectors, and classification logic.
- `SpeechRecognition`: Audio translation endpoints.
- `gTTS`: Text-to-Audio vocalization.
- `fastapi` & `uvicorn`: System API Gateway.
