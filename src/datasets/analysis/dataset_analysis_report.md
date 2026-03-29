# 📊 Multilingual Hate Speech Dataset Analysis Report

*Generated on: 2026-03-29 16:26:48*

---

## 🌍 Overall Summary

**Total rows across all languages:** 69,154

### Key Metrics per Language

| Language | Rows | Hate % | Non-hate % | Offensive % | Health % | Implicit Hate % | Sarcasm % | Call to Action % | Avg Profanity | Avg Confidence |
|----------|------|--------|------------|-------------|----------|-----------------|-----------|------------------|---------------|----------------|
| English | 18,900 | 9.4 | 82.7 | 6.1 | 1.8 | 31.1 | 1.9 | 30.3 | 0.15 | 0.897 |
| Hindi | 17,405 | 17.7 | 71.3 | 8.5 | 2.5 | 34.1 | 3.0 | 25.7 | 0.28 | 0.895 |
| Bhojpuri | 10,126 | 24.0 | 2.8 | 58.1 | 15.0 | 33.8 | 9.8 | 28.6 | 1.22 | 0.894 |
| Marathi | 10,272 | 20.2 | 1.8 | 64.1 | 13.8 | 33.8 | 9.2 | 31.0 | 1.81 | 0.894 |
| Marwari | 12,451 | 5.9 | 1.3 | 82.2 | 10.5 | 24.7 | 9.2 | 29.5 | 1.61 | 0.895 |

---

## 📌 English Dataset

**Total rows:** 18,900

### 🏷️ Label Distribution

| Label | Count | Percentage |
|-------|-------|------------|
| hate | 1,782 | 9.43% |
| non_hate | 15,622 | 82.66% |
| offensive | 1,161 | 6.14% |
| health_issue | 335 | 1.77% |

### ⚠️ Severity (for hate/offensive rows)

| Severity | Count |
|----------|-------|
| moderate | 1071 |
| mild | 963 |
| severe | 909 |
| none (non-hate/health) | 15957 |

### 🔥 Hate Speech Analysis

- **Total hate rows:** 1782
- **Implicit hate:** 554 (31.09%)
- **Direct hate:** 1228 (68.91%)
- **Call to action in hate:** 540 (30.30%)

### 😏 Sarcasm Usage

- **Sarcastic rows:** 365 (1.93%)

### 🎯 Target Groups (hate/offensive only)

| Target Group | Count |
|--------------|-------|
| individual | 1027 |
| nationality | 346 |
| religion | 333 |
| caste | 280 |
| gender | 275 |
| political | 261 |
| race | 179 |
| community | 8 |

### 🎯 Target Types

| Target Type | Count |
|-------------|-------|
| individual | 1025 |
| community | 987 |
| ideology | 697 |

### 🗣️ Tone Distribution

| Tone | Count |
|------|-------|
| neutral | 5630 |
| sadness | 5106 |
| joy | 5048 |
| aggressive | 1134 |
| dismissive | 1050 |
| fearful | 598 |
| sarcastic | 334 |

### 😡 Emotion Distribution

| Emotion | Count |
|---------|-------|
| joy | 8661 |
| none | 3620 |
| sadness | 3496 |
| disgust | 1224 |
| anger | 1025 |
| fear | 840 |
| pain | 34 |

### 🔞 Profanity Count

- **Mean:** 0.15
- **Maximum:** 3
- **Rows with zero profanity:** 86.96%

### 📱 Platform Distribution

| Platform | Count |
|----------|-------|
| social_media | 3915 |
| chat | 3843 |
| general | 3800 |
| political_speech | 3698 |
| news | 3644 |

### 🌐 Domain Distribution

| Domain | Count |
|--------|-------|
| general | 3863 |
| political | 3405 |
| health | 3097 |
| religious | 2971 |
| education | 2826 |
| sports | 2738 |

### 🗺️ Region Distribution

| Region | Count |
|--------|-------|
| global | 5114 |
| urban_india | 4689 |
| india | 4674 |
| rural_india | 4423 |

### 🎯 Annotator Confidence

- **Mean:** 0.897
- **Min:** 0.76
- **Max:** 0.99

### ✍️ Annotator Type

- **Human (A1..A20):** 15182 (80.33%)
- **Synthetic:** 3718 (19.67%)

### 📏 Sentence Length

- **Average characters per sentence:** 101.3
- **Average words per sentence:** 16.3

### ✅ Data Quality

No missing values detected.

---

## 📌 Hindi Dataset

**Total rows:** 17,405

### 🏷️ Label Distribution

| Label | Count | Percentage |
|-------|-------|------------|
| hate | 3,085 | 17.72% |
| non_hate | 12,408 | 71.29% |
| offensive | 1,473 | 8.46% |
| health_issue | 439 | 2.52% |

### ⚠️ Severity (for hate/offensive rows)

| Severity | Count |
|----------|-------|
| mild | 1546 |
| moderate | 1529 |
| severe | 1483 |
| none (non-hate/health) | 12847 |

### 🔥 Hate Speech Analysis

- **Total hate rows:** 3085
- **Implicit hate:** 1052 (34.10%)
- **Direct hate:** 2033 (65.90%)
- **Call to action in hate:** 794 (25.74%)

### 😏 Sarcasm Usage

- **Sarcastic rows:** 523 (3.00%)

### 🎯 Target Groups (hate/offensive only)

| Target Group | Count |
|--------------|-------|
| individual | 1337 |
| religion | 667 |
| caste | 647 |
| gender | 621 |
| nationality | 565 |
| political | 343 |

### 🎯 Target Types

| Target Type | Count |
|-------------|-------|
| community | 1658 |
| individual | 1337 |
| ideology | 1185 |

### 🗣️ Tone Distribution

| Tone | Count |
|------|-------|
| neutral | 4446 |
| sadness | 4192 |
| joy | 3992 |
| dismissive | 1689 |
| aggressive | 1588 |
| fearful | 977 |
| sarcastic | 521 |

### 😡 Emotion Distribution

| Emotion | Count |
|---------|-------|
| joy | 7032 |
| sadness | 2849 |
| none | 2742 |
| disgust | 1935 |
| anger | 1468 |
| fear | 1268 |
| pain | 111 |

### 🔞 Profanity Count

- **Mean:** 0.28
- **Maximum:** 2
- **Rows with zero profanity:** 76.06%

### 📱 Platform Distribution

| Platform | Count |
|----------|-------|
| chat | 3774 |
| social_media | 3588 |
| news | 3384 |
| general | 3363 |
| political_speech | 3296 |

### 🌐 Domain Distribution

| Domain | Count |
|--------|-------|
| general | 3845 |
| political | 3373 |
| religious | 2903 |
| health | 2579 |
| sports | 2408 |
| education | 2297 |

### 🗺️ Region Distribution

| Region | Count |
|--------|-------|
| india | 6392 |
| rural_india | 5519 |
| urban_india | 5494 |

### 🎯 Annotator Confidence

- **Mean:** 0.895
- **Min:** 0.76
- **Max:** 1.00

### ✍️ Annotator Type

- **Human (A1..A20):** 14201 (81.59%)
- **Synthetic:** 3204 (18.41%)

### 📏 Sentence Length

- **Average characters per sentence:** 90.2
- **Average words per sentence:** 16.4

### ✅ Data Quality

No missing values detected.

---

## 📌 Bhojpuri Dataset

**Total rows:** 10,126

### 🏷️ Label Distribution

| Label | Count | Percentage |
|-------|-------|------------|
| hate | 2,431 | 24.01% |
| non_hate | 287 | 2.83% |
| offensive | 5,888 | 58.15% |
| health_issue | 1,520 | 15.01% |

### ⚠️ Severity (for hate/offensive rows)

| Severity | Count |
|----------|-------|
| mild | 2890 |
| moderate | 2726 |
| severe | 2703 |
| none (non-hate/health) | 1807 |

### 🔥 Hate Speech Analysis

- **Total hate rows:** 2431
- **Implicit hate:** 821 (33.77%)
- **Direct hate:** 1610 (66.23%)
- **Call to action in hate:** 695 (28.59%)

### 😏 Sarcasm Usage

- **Sarcastic rows:** 993 (9.81%)

### 🎯 Target Groups (hate/offensive only)

| Target Group | Count |
|--------------|-------|
| individual | 4482 |
| caste | 538 |
| religion | 486 |
| nationality | 465 |
| gender | 433 |
| political | 306 |

### 🎯 Target Types

| Target Type | Count |
|-------------|-------|
| individual | 4482 |
| community | 1264 |
| ideology | 964 |

### 🗣️ Tone Distribution

| Tone | Count |
|------|-------|
| aggressive | 3456 |
| dismissive | 3303 |
| fearful | 1339 |
| sarcastic | 986 |
| neutral | 959 |
| sadness | 45 |
| joy | 38 |

### 😡 Emotion Distribution

| Emotion | Count |
|---------|-------|
| disgust | 3482 |
| fear | 2694 |
| anger | 2569 |
| sadness | 484 |
| none | 378 |
| pain | 314 |
| joy | 205 |

### 🔞 Profanity Count

- **Mean:** 1.22
- **Maximum:** 2
- **Rows with zero profanity:** 23.52%

### 📱 Platform Distribution

| Platform | Count |
|----------|-------|
| social_media | 2230 |
| chat | 2189 |
| general | 1977 |
| news | 1934 |
| political_speech | 1796 |

### 🌐 Domain Distribution

| Domain | Count |
|--------|-------|
| health | 2431 |
| general | 2412 |
| political | 1992 |
| religious | 1340 |
| sports | 1007 |
| education | 944 |

### 🗺️ Region Distribution

| Region | Count |
|--------|-------|
| rural_india | 4138 |
| urban_india | 3005 |
| india | 2983 |

### 🎯 Annotator Confidence

- **Mean:** 0.894
- **Min:** 0.76
- **Max:** 0.99

### ✍️ Annotator Type

- **Human (A1..A20):** 7488 (73.95%)
- **Synthetic:** 2638 (26.05%)

### 📏 Sentence Length

- **Average characters per sentence:** 48.5
- **Average words per sentence:** 10.0

### ✅ Data Quality

No missing values detected.

---

## 📌 Marathi Dataset

**Total rows:** 10,272

### 🏷️ Label Distribution

| Label | Count | Percentage |
|-------|-------|------------|
| hate | 2,080 | 20.25% |
| non_hate | 187 | 1.82% |
| offensive | 6,585 | 64.11% |
| health_issue | 1,420 | 13.82% |

### ⚠️ Severity (for hate/offensive rows)

| Severity | Count |
|----------|-------|
| mild | 2920 |
| moderate | 2913 |
| severe | 2832 |
| none (non-hate/health) | 1607 |

### 🔥 Hate Speech Analysis

- **Total hate rows:** 2080
- **Implicit hate:** 704 (33.85%)
- **Direct hate:** 1376 (66.15%)
- **Call to action in hate:** 644 (30.96%)

### 😏 Sarcasm Usage

- **Sarcastic rows:** 950 (9.25%)

### 🎯 Target Groups (hate/offensive only)

| Target Group | Count |
|--------------|-------|
| individual | 4814 |
| caste | 480 |
| religion | 424 |
| gender | 370 |
| nationality | 369 |
| political | 249 |

### 🎯 Target Types

| Target Type | Count |
|-------------|-------|
| individual | 4814 |
| community | 983 |
| ideology | 909 |

### 🗣️ Tone Distribution

| Tone | Count |
|------|-------|
| aggressive | 3612 |
| dismissive | 3527 |
| fearful | 1267 |
| sarcastic | 948 |
| neutral | 832 |
| sadness | 44 |
| joy | 42 |

### 😡 Emotion Distribution

| Emotion | Count |
|---------|-------|
| disgust | 3511 |
| fear | 2897 |
| anger | 2610 |
| none | 421 |
| sadness | 378 |
| pain | 361 |
| joy | 94 |

### 🔞 Profanity Count

- **Mean:** 1.81
- **Maximum:** 3
- **Rows with zero profanity:** 16.16%

### 📱 Platform Distribution

| Platform | Count |
|----------|-------|
| social_media | 2120 |
| political_speech | 2070 |
| news | 2055 |
| general | 2031 |
| chat | 1996 |

### 🌐 Domain Distribution

| Domain | Count |
|--------|-------|
| health | 2504 |
| general | 2013 |
| political | 1896 |
| religious | 1454 |
| sports | 1273 |
| education | 1132 |

### 🗺️ Region Distribution

| Region | Count |
|--------|-------|
| urban_india | 3489 |
| india | 3396 |
| rural_india | 3387 |

### 🎯 Annotator Confidence

- **Mean:** 0.894
- **Min:** 0.76
- **Max:** 0.99

### ✍️ Annotator Type

- **Human (A1..A20):** 8316 (80.96%)
- **Synthetic:** 1956 (19.04%)

### 📏 Sentence Length

- **Average characters per sentence:** 49.3
- **Average words per sentence:** 8.3

### ✅ Data Quality

No missing values detected.

---

## 📌 Marwari Dataset

**Total rows:** 12,451

### 🏷️ Label Distribution

| Label | Count | Percentage |
|-------|-------|------------|
| hate | 740 | 5.94% |
| non_hate | 167 | 1.34% |
| offensive | 10,240 | 82.24% |
| health_issue | 1,304 | 10.47% |

### ⚠️ Severity (for hate/offensive rows)

| Severity | Count |
|----------|-------|
| moderate | 3690 |
| severe | 3651 |
| mild | 3639 |
| none (non-hate/health) | 1471 |

### 🔥 Hate Speech Analysis

- **Total hate rows:** 740
- **Implicit hate:** 183 (24.73%)
- **Direct hate:** 557 (75.27%)
- **Call to action in hate:** 218 (29.46%)

### 😏 Sarcasm Usage

- **Sarcastic rows:** 1149 (9.23%)

### 🎯 Target Groups (hate/offensive only)

| Target Group | Count |
|--------------|-------|
| individual | 7241 |
| caste | 186 |
| religion | 148 |
| gender | 128 |
| nationality | 127 |
| political | 86 |

### 🎯 Target Types

| Target Type | Count |
|-------------|-------|
| individual | 7241 |
| community | 345 |
| ideology | 330 |

### 🗣️ Tone Distribution

| Tone | Count |
|------|-------|
| dismissive | 4828 |
| aggressive | 4808 |
| sarcastic | 1148 |
| fearful | 848 |
| neutral | 738 |
| joy | 44 |
| sadness | 37 |

### 😡 Emotion Distribution

| Emotion | Count |
|---------|-------|
| disgust | 4420 |
| fear | 3602 |
| anger | 3274 |
| none | 393 |
| sadness | 354 |
| pain | 318 |
| joy | 90 |

### 🔞 Profanity Count

- **Mean:** 1.61
- **Maximum:** 2
- **Rows with zero profanity:** 12.09%

### 📱 Platform Distribution

| Platform | Count |
|----------|-------|
| news | 2534 |
| political_speech | 2524 |
| general | 2474 |
| chat | 2460 |
| social_media | 2459 |

### 🌐 Domain Distribution

| Domain | Count |
|--------|-------|
| health | 2985 |
| political | 2040 |
| general | 2028 |
| sports | 1840 |
| religious | 1827 |
| education | 1731 |

### 🗺️ Region Distribution

| Region | Count |
|--------|-------|
| rural_india | 4204 |
| urban_india | 4131 |
| india | 4116 |

### 🎯 Annotator Confidence

- **Mean:** 0.895
- **Min:** 0.76
- **Max:** 0.99

### ✍️ Annotator Type

- **Human (A1..A20):** 9984 (80.19%)
- **Synthetic:** 2467 (19.81%)

### 📏 Sentence Length

- **Average characters per sentence:** 44.6
- **Average words per sentence:** 8.8

### ✅ Data Quality

No missing values detected.

---

# End of Report
