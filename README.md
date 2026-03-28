# Justify-AI

An explainable, multilingual hate-analysis framework built with classical NLP and Naive Bayes. The system combines lexical, causal, and demographic signals to produce an interpretable risk score and a visual dashboard.

## Core Objective
Built to fulfill the **CCNLP Laboratory Syllabus Implementation** using foundational, statistical NLP methods. No transformers are used.

## Current Pipeline
Input Text → Language Detection → Language-Specific Preprocessing → Hate Lexicon Matching →
Causality Extraction → Bias Auditing → Risk Scoring → Visual Dashboard

## Implemented Syllabus Concepts
- Tokenization
- Stemming
- Lemmatization
- Stopword Removal
- POS Tagging
- N-grams
- Bag of Words
- Named Entity Recognition (NLTK Chunking)
- Sentiment/Hate Classification (Naive Bayes)
- Speech-to-Text & Text-to-Speech

## Multilingual Support
Supported languages:
- English
- Hindi
- Marathi
- Bhojpuri
- Marwari

## Key Features (Implemented)
- Lexicon matching with severity + spans
- Rule-based causality extraction (cause → effect)
- Demographic bias auditing (group + negative attribute co-occurrence)
- Risk scoring (lexical + causal + bias)
- Demo dashboard wired to backend outputs

## Quick Start
1) Install dependencies:
   - python -m pip install -r requirements.txt
2) Start the backend:
   - python -m uvicorn src.api.app:app --reload
3) Open the demo UI:
   - http://127.0.0.1:8000

## Core API Endpoint
POST /api/analyze
Body:
{ "text": "...", "language": "english" }

Returns:
- language, hate_speech_label, confidence
- lexicon_hits (term, severity, count, spans)
- causality_relations (cause, effect, relation, confidence, sentence)
- bias_metrics (per-dimension + overall)
- risk (score, level, breakdown)

## Tests
Install pytest:
- python -m pip install pytest
Run:
- python -m pytest

## Documentation
Latest progress: `documents/checklogs/progress-3.md`
Setup guide: `documents/project_setup_guide.txt`
Quick reference: `documents/quick_reference_card.txt`

## Technology Stack
- `nltk` for classical NLP processing
- `scikit-learn` for N-grams/BoW + Naive Bayes
- `fastapi` + `uvicorn` for backend API
- `SpeechRecognition` + `gTTS` for audio utilities
