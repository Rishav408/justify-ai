# Model Metrics Report

Train/test split: 80/20 stratified, random_state=42

## English

### Classification Report

| Label | Precision | Recall | F1 | Support |
| --- | --- | --- | --- | --- |
| hate | 0.986 | 0.983 | 0.985 | 357 |
| non_hate | 0.994 | 0.994 | 0.994 | 3124 |
| offensive | 0.973 | 0.948 | 0.961 | 232 |
| health_issue | 0.778 | 0.836 | 0.806 | 67 |
| accuracy | - | - | 0.988 | 3780 |

### Confusion Matrix (rows=true, cols=pred)

| true\pred | hate | non_hate | offensive | health_issue |
| --- | --- | --- | --- | --- |
| hate | 351 | 4 | 2 | 0 |
| non_hate | 0 | 3106 | 3 | 15 |
| offensive | 5 | 6 | 220 | 1 |
| health_issue | 0 | 10 | 1 | 56 |

## Hindi

### Classification Report

| Label | Precision | Recall | F1 | Support |
| --- | --- | --- | --- | --- |
| hate | 0.970 | 0.995 | 0.982 | 617 |
| non_hate | 0.999 | 0.985 | 0.992 | 2481 |
| offensive | 0.997 | 0.993 | 0.995 | 295 |
| health_issue | 0.806 | 0.989 | 0.888 | 88 |
| accuracy | - | - | 0.988 | 3481 |

### Confusion Matrix (rows=true, cols=pred)

| true\pred | hate | non_hate | offensive | health_issue |
| --- | --- | --- | --- | --- |
| hate | 614 | 1 | 0 | 2 |
| non_hate | 18 | 2444 | 0 | 19 |
| offensive | 1 | 1 | 293 | 0 |
| health_issue | 0 | 0 | 1 | 87 |

## Marathi

### Classification Report

| Label | Precision | Recall | F1 | Support |
| --- | --- | --- | --- | --- |
| hate | 0.993 | 0.978 | 0.985 | 416 |
| non_hate | 0.658 | 0.658 | 0.658 | 38 |
| offensive | 0.993 | 0.998 | 0.996 | 1317 |
| health_issue | 0.996 | 0.993 | 0.995 | 284 |
| accuracy | - | - | 0.987 | 2055 |

### Confusion Matrix (rows=true, cols=pred)

| true\pred | hate | non_hate | offensive | health_issue |
| --- | --- | --- | --- | --- |
| hate | 407 | 9 | 0 | 0 |
| non_hate | 3 | 25 | 9 | 1 |
| offensive | 0 | 2 | 1315 | 0 |
| health_issue | 0 | 2 | 0 | 282 |

## Bhojpuri

### Classification Report

| Label | Precision | Recall | F1 | Support |
| --- | --- | --- | --- | --- |
| hate | 0.992 | 1.000 | 0.996 | 486 |
| non_hate | 1.000 | 0.897 | 0.945 | 58 |
| offensive | 0.999 | 1.000 | 1.000 | 1178 |
| health_issue | 0.997 | 1.000 | 0.998 | 304 |
| accuracy | - | - | 0.997 | 2026 |

### Confusion Matrix (rows=true, cols=pred)

| true\pred | hate | non_hate | offensive | health_issue |
| --- | --- | --- | --- | --- |
| hate | 486 | 0 | 0 | 0 |
| non_hate | 4 | 52 | 1 | 1 |
| offensive | 0 | 0 | 1178 | 0 |
| health_issue | 0 | 0 | 0 | 304 |

## Marwari

### Classification Report

| Label | Precision | Recall | F1 | Support |
| --- | --- | --- | --- | --- |
| hate | 0.961 | 1.000 | 0.980 | 148 |
| non_hate | 0.947 | 0.545 | 0.692 | 33 |
| offensive | 0.996 | 0.999 | 0.998 | 2049 |
| health_issue | 0.989 | 0.996 | 0.992 | 261 |
| accuracy | - | - | 0.993 | 2491 |

### Confusion Matrix (rows=true, cols=pred)

| true\pred | hate | non_hate | offensive | health_issue |
| --- | --- | --- | --- | --- |
| hate | 148 | 0 | 0 | 0 |
| non_hate | 4 | 18 | 8 | 3 |
| offensive | 2 | 0 | 2047 | 0 |
| health_issue | 0 | 1 | 0 | 260 |
