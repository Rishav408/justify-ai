# Justify-AI: Comprehensive English NLP Pipeline Architecture and Implementation Guide

This document serves as an in-depth reference guide for the English Natural Language Processing (NLP) pipeline built for the Justify-AI project. It details the step-by-step logic, the challenges encountered during implementation, and the exact data flow from a user's browser down to the core machine learning inference layer.

---

## 1. Architectural Overview & The Request Lifecycle

Before detailing the code implementations, it is crucial to understand the lifecycle of a text string submitted to the Justify-AI platform. The architecture is explicitly designed to be **modular**, meaning each responsibility is isolated into its own file so components can be upgraded (like swapping simple lexicons for Deep Learning models) without breaking the rest of the flow.

### **The Sequence of Execution**
1. **The User Prompt:** A user enters text into `demo.html` on the browser and clicks "Analyze".
2. **Frontend `fetch()`:** The `analyze.js` script explicitly captures this string and packages it into a strict JSON body, sending a `POST` request to `http://127.0.0.1:8000/api/analyze`.
3. **The API Gateway:** FastAPI intercepts the request. Due to our `CORSMiddleware`, it accepts the browser's request securely. `routes.py` unpacks the JSON via Pydantic model validation.
4. **Primary Language Routing:** Instead of blindly running English models, `language_router.py` uses the `langdetect` library. If it spots "en", it directs traffic to the English Pipeline.
5. **English Orchestrator (`english_pipeline.py`):** This file acts as the general. It accepts the string and begins sequentially firing our custom modules.
6. **Data Preparation:**
   * Text is scrubbed and lowercased (`preprocessing.py`).
   * Text is tokenized, lemmatized, and segmented into base arrays by `spaCy`.
7. **Module Execution:** Arrays of lemmas are passed simultaneously to independent heuristic detectors (Lexicon, Causality, Bias).
8. **Final Assembly:** Outputs from the detectors are handed directly to the `risk_scorer.py` and then interpreted by the `explanation_generator.py`.
9. **Return to User:** A massive JSON object containing all extracted logic, explanations, confidence scores, and raw arrays is passed back to FastAPI and fired directly into the user's browser DOM.

---

## 2. Phase 1: Overcoming API and Connectivity Hurdles

The very first major hurdle in this implementation was bridging the gap between the beautiful frontend UI and the empty backend API.

### **Initial State Problems:**
* **Static File Error:** The frontend (`demo.html`) was purely running in the browser's native file explorer (`file:///`) context. The Python FastAPI backend was running completely untethered on port `8000`, returning only a simple `"message": "Justify-AI backend running"`. 
* **CORS Rejection:** Browsers block web pages from sending background API requests to different ports/origins for security (Cross-Origin Resource Sharing). Our frontend Javascript mock was totally unequipped to communicate.
* **Payload Mismatch:** The `/analyze` endpoint expected a simple query string (`?text=...`), which is useless for processing large essays or datasets.

### **The Implemented Solutions:**
1. **Serving the Frontend Correctly:** In `src/api/main.py`, we heavily altered the FastAPI setup. We mounted the entire frontend directory aggressively onto the python server: `app.mount("/", StaticFiles(directory="frontend", html=True))`. This forced the python backend to actually host the UI directly over localhost.
2. **CORS Middleware:** We imported and injected `CORSMiddleware` explicitly allowing all `["*"]` origins and headers so data could flow between the Javascript execution context and the Python process.
3. **Pydantic Validation:** We wrote a strict `BaseModel` called `AnalyzeRequest` into `src/api/routes.py`. If a string isn't correctly wrapped inside standard `{"text": "..."}` JSON formatting, the API cleanly rejects it.
4. **Wiring `analyze.js`:** We injected genuine `fetch()` promise logic into `demo.js` to automatically grab the `inputText` field and dump the resulting AI JSON directly onto the screen. To quickly verify without rendering complex graphs, we hooked the pipeline response dynamically into the "Quick Stats" green DOM elements. 

---

## 3. Phase 2: Building Core NLP Heuristics

The heart of Justify-AI relies on isolating dangerous structural framing mechanisms. A simple POS tag won't catch propaganda. We built distinct, logic-driven arrays and functions for these specific mechanisms.

### **3.1 Lexicon Detection (`lexicon_detector.py`)**
We wanted to flag highly sensitive ideological and manipulative terminologies. 
* **Implementation:** Instead of hardcoding arrays, we created a standard JSON file (`data/lexicons/lexicon_en.json`) mapped with categorizations (e.g., `"manipulate": "psychological"`). We utilized Python's `pathlib` for safe OS-agnostic local loading. 

### **3.2 Causality Extraction (`causality_extractor.py`)**
Propaganda utilizes cause-and-effect structuring to force blame (e.g., "because of THEM"). 
* **Implementation:** A functional python module iterates over every token, sweeping against an explicit array of connective rhetoric bounds (`because`, `therefore`, `thus`, `causes`).

### **3.3 Bias Detection (`bias_detector.py`)**
Ideological texts rely heavily on absolutism and totalizing language to leave zero room for alternative reasoning.
* **Implementation:** We implemented sweeping hooks for terms like `"everyone"`, `"always"`, and `"never"`. If detected, they are flagged and pushed into the final output dictionaries.

---

## 4. Phase 3: The Risk Scorer & Explanation Synthesizer

Once the raw data arrays are compiled, the system needed a human-readable interpretation level.

### **Risk Calculation (`risk_scorer.py`)**
It aggregates the physical length of the hits array from the three modules heavily weighing the Lexicon hits:
* `score += len(lexicon_hits) * 2`
* The total integer is assessed against simple control tiers, mapping it to `"low"`, `"medium"`, or `"high"`.
* **Important Addition:** We introduced a specific algorithmic bounded `confidence` ceiling limit to project statistical certainty bounds back to the user interface explicitly: `confidence = min(1.0, score / 10)`.

### **Explanation Generator (`explanation_generator.py`)**
A raw JSON showing `"control"` and `"because"` means little to an end-user. We built an interpretative loop.
* It probes the arrays cleanly. If the array is populated, it dynamically builds conversational descriptive output: `f"Absolute or biased language detected: {', '.join(bias_hits)}."` 
* It conjoins all of these conversational strings, appending the Risk Level as a concluding thesis, resulting in an elegant paragraph passed natively into the API.

---

## 5. Phase 4: Finalizing the English Pipeline (Maturing NLP Accuracy)

The final test phase exposed critical logic weaknesses within the raw NLP setup structure inside `english_pipeline.py`. 

### **The Critical Flaw: Raw Token Weakness**
Initially, we pushed raw split `tokens = [token.text for token in doc]` strings directly into our detectors.
* **The Problem:** The `lexicon.json` looks exactly for `"control"`. If a user types `"controlling"`, `"controlled"`, or `"controls"`, the module completely fails to flag the threat despite the semantic identical. 
* **The Solution:** We explicitly ordered the pipeline to construct a completely new array exploiting the core Machine Learning intelligence powering spaCy: **Lemmatization**. By mapping `lemmas = [token.lemma_ for token in doc]`, spaCy intelligently calculates the pure root dictionary baseline of every complex word ending. `controlled` becomes `control`. We heavily rewired our Lexicon, Causality, and Bias detectors to consume *purely* the `lemmas` array, drastically driving accuracy through the roof.

### **The Final Upgrade: Sentence Segmentation**
To establish a future foundation for complex Graph logic mappings and specific sentence-level argument reasoning, we sliced the pipeline using `sentences = [sent.text for sent in doc.sents]`. 

By structuring the arrays into exact segmented periods natively, future Justify-AI iterations can iterate through discrete argument structures one at a time, completing the core foundational architecture of the English NLP processor pipeline!
