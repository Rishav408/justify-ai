# 📊 Multilingual Hate Speech Dataset Analysis Report

*Generated on: 2026-03-29 17:48:47*

---

## 🌍 Overall Summary

**Total rows across all languages:** 75,252

### Key Metrics per Language

| Language | Rows | Hate % | Non-hate % | Offensive % | Health % | Implicit Hate % | Sarcasm % | Call to Action % | Avg Profanity | Avg Confidence |
|----------|------|--------|------------|-------------|----------|-----------------|-----------|------------------|---------------|----------------|
| English | 18,900 | 9.4 | 82.7 | 6.1 | 1.8 | 31.1 | 1.9 | 30.3 | 0.15 | 0.897 |
| Hindi | 17,405 | 17.7 | 71.3 | 8.5 | 2.5 | 34.1 | 3.0 | 25.7 | 0.28 | 0.895 |
| Bhojpuri | 11,960 | 20.3 | 17.7 | 49.2 | 12.7 | 33.8 | 8.3 | 28.6 | 1.04 | 0.898 |
| Marathi | 12,196 | 17.1 | 17.3 | 54.0 | 11.6 | 33.8 | 7.8 | 31.0 | 1.52 | 0.899 |
| Marwari | 14,791 | 5.0 | 16.9 | 69.2 | 8.8 | 24.7 | 7.8 | 29.5 | 1.36 | 0.899 |

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
| neutral | 15784 |
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
| neutral | 12630 |
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

**Total rows:** 11,960

### 🏷️ Label Distribution

| Label | Count | Percentage |
|-------|-------|------------|
| hate | 2,431 | 20.33% |
| non_hate | 2,121 | 17.73% |
| offensive | 5,888 | 49.23% |
| health_issue | 1,520 | 12.71% |

### ⚠️ Severity (for hate/offensive rows)

| Severity | Count |
|----------|-------|
| mild | 2890 |
| moderate | 2726 |
| severe | 2703 |
| none (non-hate/health) | 3641 |

### 🔥 Hate Speech Analysis

- **Total hate rows:** 2431
- **Implicit hate:** 821 (33.77%)
- **Direct hate:** 1610 (66.23%)
- **Call to action in hate:** 695 (28.59%)

### 😏 Sarcasm Usage

- **Sarcastic rows:** 993 (8.30%)

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
| neutral | 2876 |
| fearful | 1339 |
| sarcastic | 986 |

### 😡 Emotion Distribution

| Emotion | Count |
|---------|-------|
| disgust | 3482 |
| fear | 2694 |
| anger | 2569 |
| sadness | 1094 |
| none | 1013 |
| joy | 794 |
| pain | 314 |

### 🔞 Profanity Count

- **Mean:** 1.04
- **Maximum:** 2
- **Rows with zero profanity:** 35.25%

### 📱 Platform Distribution

| Platform | Count |
|----------|-------|
| social_media | 2694 |
| chat | 2664 |
| general | 2421 |
| news | 2385 |
| political_speech | 1796 |

### 🌐 Domain Distribution

| Domain | Count |
|--------|-------|
| general | 3016 |
| health | 2431 |
| political | 1992 |
| sports | 1633 |
| education | 1548 |
| religious | 1340 |

### 🗺️ Region Distribution

| Region | Count |
|--------|-------|
| rural_india | 4581 |
| urban_india | 3480 |
| india | 3444 |
| global | 455 |

### 🎯 Annotator Confidence

- **Mean:** 0.898
- **Min:** 0.76
- **Max:** 0.99

### ✍️ Annotator Type

- **Human (A1..A20):** 9019 (75.41%)
- **Synthetic:** 2941 (24.59%)

### 📏 Sentence Length

- **Average characters per sentence:** 46.8
- **Average words per sentence:** 9.6

### ✅ Data Quality

No missing values detected.

---

## 📌 Marathi Dataset

**Total rows:** 12,196

### 🏷️ Label Distribution

| Label | Count | Percentage |
|-------|-------|------------|
| hate | 2,080 | 17.05% |
| non_hate | 2,111 | 17.31% |
| offensive | 6,585 | 53.99% |
| health_issue | 1,420 | 11.64% |

### ⚠️ Severity (for hate/offensive rows)

| Severity | Count |
|----------|-------|
| mild | 2920 |
| moderate | 2913 |
| severe | 2832 |
| none (non-hate/health) | 3531 |

### 🔥 Hate Speech Analysis

- **Total hate rows:** 2080
- **Implicit hate:** 704 (33.85%)
- **Direct hate:** 1376 (66.15%)
- **Call to action in hate:** 644 (30.96%)

### 😏 Sarcasm Usage

- **Sarcastic rows:** 950 (7.79%)

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
| neutral | 2842 |
| fearful | 1267 |
| sarcastic | 948 |

### 😡 Emotion Distribution

| Emotion | Count |
|---------|-------|
| disgust | 3511 |
| fear | 2897 |
| anger | 2610 |
| none | 1050 |
| sadness | 1005 |
| joy | 762 |
| pain | 361 |

### 🔞 Profanity Count

- **Mean:** 1.52
- **Maximum:** 3
- **Rows with zero profanity:** 29.39%

### 📱 Platform Distribution

| Platform | Count |
|----------|-------|
| social_media | 2589 |
| news | 2553 |
| general | 2524 |
| chat | 2460 |
| political_speech | 2070 |

### 🌐 Domain Distribution

| Domain | Count |
|--------|-------|
| general | 2650 |
| health | 2504 |
| sports | 1904 |
| political | 1896 |
| education | 1788 |
| religious | 1454 |

### 🗺️ Region Distribution

| Region | Count |
|--------|-------|
| urban_india | 3962 |
| india | 3895 |
| rural_india | 3844 |
| global | 495 |

### 🎯 Annotator Confidence

- **Mean:** 0.899
- **Min:** 0.76
- **Max:** 0.99

### ✍️ Annotator Type

- **Human (A1..A20):** 9909 (81.25%)
- **Synthetic:** 2287 (18.75%)

### 📏 Sentence Length

- **Average characters per sentence:** 47.3
- **Average words per sentence:** 8.0

### ✅ Data Quality

No missing values detected.

---

## 📌 Marwari Dataset

**Total rows:** 14,791

### 🏷️ Label Distribution

| Label | Count | Percentage |
|-------|-------|------------|
| hate | 740 | 5.00% |
| non_hate | 2,507 | 16.95% |
| offensive | 10,240 | 69.23% |
| health_issue | 1,304 | 8.82% |

### ⚠️ Severity (for hate/offensive rows)

| Severity | Count |
|----------|-------|
| moderate | 3690 |
| severe | 3651 |
| mild | 3639 |
| none (non-hate/health) | 3811 |

### 🔥 Hate Speech Analysis

- **Total hate rows:** 740
- **Implicit hate:** 183 (24.73%)
- **Direct hate:** 557 (75.27%)
- **Call to action in hate:** 218 (29.46%)

### 😏 Sarcasm Usage

- **Sarcastic rows:** 1149 (7.77%)

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
| neutral | 3159 |
| sarcastic | 1148 |
| fearful | 848 |

### 😡 Emotion Distribution

| Emotion | Count |
|---------|-------|
| disgust | 4420 |
| fear | 3602 |
| anger | 3274 |
| none | 1167 |
| sadness | 1161 |
| joy | 849 |
| pain | 318 |

### 🔞 Profanity Count

- **Mean:** 1.36
- **Maximum:** 2
- **Rows with zero profanity:** 26.00%

### 📱 Platform Distribution

| Platform | Count |
|----------|-------|
| news | 3096 |
| general | 3076 |
| chat | 3052 |
| social_media | 3043 |
| political_speech | 2524 |

### 🌐 Domain Distribution

| Domain | Count |
|--------|-------|
| health | 2985 |
| general | 2793 |
| sports | 2631 |
| education | 2515 |
| political | 2040 |
| religious | 1827 |

### 🗺️ Region Distribution

| Region | Count |
|--------|-------|
| rural_india | 4789 |
| india | 4708 |
| urban_india | 4699 |
| global | 595 |

### 🎯 Annotator Confidence

- **Mean:** 0.899
- **Min:** 0.76
- **Max:** 0.99

### ✍️ Annotator Type

- **Human (A1..A20):** 11918 (80.58%)
- **Synthetic:** 2873 (19.42%)

### 📏 Sentence Length

- **Average characters per sentence:** 43.4
- **Average words per sentence:** 8.6

### ✅ Data Quality

No missing values detected.

---

# End of Report
