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
| hate | 1.000 | 1.000 | 1.000 | 416 |
| non_hate | 1.000 | 0.979 | 0.989 | 422 |
| offensive | 0.995 | 1.000 | 0.997 | 1318 |
| health_issue | 0.993 | 1.000 | 0.996 | 284 |
| accuracy | - | - | 0.996 | 2440 |

### Confusion Matrix (rows=true, cols=pred)

| true\pred | hate | non_hate | offensive | health_issue |
| --- | --- | --- | --- | --- |
| hate | 416 | 0 | 0 | 0 |
| non_hate | 0 | 413 | 7 | 2 |
| offensive | 0 | 0 | 1318 | 0 |
| health_issue | 0 | 0 | 0 | 284 |

## Bhojpuri

### Classification Report

| Label | Precision | Recall | F1 | Support |
| --- | --- | --- | --- | --- |
| hate | 0.998 | 1.000 | 0.999 | 486 |
| non_hate | 1.000 | 0.986 | 0.993 | 424 |
| offensive | 0.997 | 1.000 | 0.999 | 1178 |
| health_issue | 0.993 | 1.000 | 0.997 | 304 |
| accuracy | - | - | 0.997 | 2392 |

### Confusion Matrix (rows=true, cols=pred)

| true\pred | hate | non_hate | offensive | health_issue |
| --- | --- | --- | --- | --- |
| hate | 486 | 0 | 0 | 0 |
| non_hate | 1 | 418 | 3 | 2 |
| offensive | 0 | 0 | 1178 | 0 |
| health_issue | 0 | 0 | 0 | 304 |

## Marwari

### Classification Report

| Label | Precision | Recall | F1 | Support |
| --- | --- | --- | --- | --- |
| hate | 0.980 | 1.000 | 0.990 | 148 |
| non_hate | 1.000 | 0.968 | 0.984 | 501 |
| offensive | 0.994 | 0.999 | 0.997 | 2049 |
| health_issue | 0.989 | 1.000 | 0.994 | 261 |
| accuracy | - | - | 0.994 | 2959 |

### Confusion Matrix (rows=true, cols=pred)

| true\pred | hate | non_hate | offensive | health_issue |
| --- | --- | --- | --- | --- |
| hate | 148 | 0 | 0 | 0 |
| non_hate | 1 | 485 | 12 | 3 |
| offensive | 2 | 0 | 2047 | 0 |
| health_issue | 0 | 0 | 0 | 261 |
