# Progress Log 3
Date: 2026-03-29

## Executive Summary
This update delivers a complete end-to-end, interpretable, multilingual hate analysis pipeline:
Input Text → Language Detection → Language-Specific Preprocessing → Hate Lexicon Matching →
Causality Extraction → Bias Auditing → Risk Scoring → Visual Dashboard.

Phase 1 through Phase 7 are now implemented, wired to the backend, and validated with unit tests.
The frontend demo now consumes real backend outputs (risk score, breakdown, bias metrics) with
safe fallback behavior.

## Phase 1: Foundations
- Unified analysis schema added to `/api/analyze` with placeholders for:
  `lexicon_hits`, `causality_relations`, `bias_metrics`, `risk`.
- Language coverage priority finalized for all 5 supported languages:
  English, Hindi, Marathi, Bhojpuri, Marwari.

Key files:
- `src/api/routes.py`

## Phase 2: Hate Lexicon Matching (Backend)
- Added lexicon storage and matcher to detect term hits with severity, counts, and spans.
- Implemented language-aware matching (word-boundary for Latin; substring for others).
- Added BOM-safe JSON reading for lexicon files.

Key files:
- `src/lexicon/lexicon_matcher.py`
- `src/lexicon/lexicons/*.json`
- `src/api/routes.py`

Fixes:
- JSON BOM handling: read lexicons with `utf-8-sig`.
- Regex safety: fixed hyphen range in the Latin token guard.

## Phase 3: Causality Extraction (Backend)
- Added rule-based causal patterns for English + Hindi + Marathi + Bhojpuri + Marwari.
- Extracts `(cause, effect, relation, confidence, sentence)`.
- Exposes `causality_relations` in API response and `causality_hits` for UI compatibility.

Key files:
- `src/causality/causality_extractor.py`
- `src/api/routes.py`

## Phase 4: Bias Auditing (Backend)
- Implemented demographic-group + negative-attribute co-occurrence detection.
- Returns `bias_metrics` plus evidence hits; `bias_hits` added for UI compatibility.

Key files:
- `src/bias/bias_auditor.py`
- `src/api/routes.py`

## Phase 5: Risk Scoring (Backend)
- Combined lexical, causal, and bias signals into a 0–100 risk score.
- Returns `risk.score`, `risk.level`, and `risk.breakdown`.

Key files:
- `src/scoring/risk_scorer.py`
- `src/api/routes.py`

## Phase 6: Dashboard Wiring (Frontend)
- Demo UI now uses real backend `risk` and `bias_metrics` when available.
- Preserves fallback behavior if the backend is offline or returns partial data.

Key files:
- `frontend/js/demo.js`

## Phase 7: QA + Validation
- Added unit tests for lexicon, causality, bias, and risk scoring.
- Updated tests so they run both under `pytest` and direct `python` execution.
- Verified: `python -m pytest` runs successfully after installing pytest.

Key files:
- `tests/test_lexicon.py`
- `tests/test_causality.py`
- `tests/test_bias.py`
- `tests/test_risk.py`
- `tests/conftest.py`

Test result:
- 4 tests passed in 3.79s.

## Sanity Tests (API)
- Lexicon hits: verified with English inputs.
- Causality extraction: verified with explicit cause-effect sentences.
- Bias auditing: verified with demographic + negative attribute sentences.
- Risk scoring: verified end-to-end with mixed lexical + causal signals.

## Additional Maintenance
- Added module `__init__.py` files for new packages:
  `src/lexicon`, `src/causality`, `src/bias`, `src/scoring`.
- Updated `.gitignore` to ignore pytest cache and uvicorn logs.
- Removed temporary log files and `test-delete.txt`.

## Current Pipeline Coverage
- Input Text: Implemented
- Language Detection: Implemented
- Language-Specific Preprocessing: Implemented
- Hate Lexicon Matching: Implemented
- Causality Extraction: Implemented
- Bias Auditing: Implemented
- Risk Scoring: Implemented
- Visual Dashboard: Implemented + wired to backend

## Notes / Known Constraints
- NLTK resources may attempt download if missing; offline environments log warnings but do not crash.
- Lexicon quality is dependent on the curated lists per language.
- Causality and bias logic are rule-based baselines and can be expanded later.

## Next Steps (Optional)
- Expand lexicons and negative-attribute lists per language.
- Enrich causal patterns with more language-specific connectors.
- Calibrate risk weights per language or data domain.
