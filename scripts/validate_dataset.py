import sys
from pathlib import Path

import pandas as pd


EXPECTED_COLUMNS = [
    "text",
    "label",
    "severity",
    "is_implicit",
    "is_sarcasm",
    "target_group",
    "target_type",
    "directness",
    "call_to_action",
    "tone",
    "emotion",
    "profanity_count",
    "platform",
    "domain",
    "region",
    "confidence",
    "annotator_id",
]

ALLOWED_VALUES = {
    "label": {"hate", "non_hate", "offensive", "health_issue"},
    "severity": {"none", "mild", "moderate", "severe"},
    "target_group": {"none", "gender", "religion", "caste", "nationality", "race", "political", "individual"},
    "tone": {"neutral", "aggressive", "dismissive", "sarcastic", "fearful"},
    "emotion": {"none", "anger", "disgust", "fear", "sadness", "joy"},
}

BOOLEAN_COLUMNS = {"is_implicit", "is_sarcasm", "call_to_action"}


def validate_file(path: Path) -> list[str]:
    errors = []
    df = pd.read_csv(path)

    if list(df.columns) != EXPECTED_COLUMNS:
        errors.append(f"{path.name}: expected columns {EXPECTED_COLUMNS}, found {list(df.columns)}")

    missing_columns = [column for column in EXPECTED_COLUMNS if column not in df.columns]
    if missing_columns:
        errors.append(f"{path.name}: missing columns {missing_columns}")
        return errors

    missing_values = int(df[EXPECTED_COLUMNS].isnull().sum().sum())
    if missing_values:
        errors.append(f"{path.name}: contains {missing_values} null values")

    for column, allowed in ALLOWED_VALUES.items():
        invalid = sorted(set(df[column].astype(str)) - allowed)
        if invalid:
            errors.append(f"{path.name}: invalid values in {column}: {invalid}")

    for column in BOOLEAN_COLUMNS:
        normalized = set(df[column].astype(str).str.lower())
        invalid = sorted(normalized - {"true", "false"})
        if invalid:
            errors.append(f"{path.name}: invalid boolean values in {column}: {invalid}")

    confidence = pd.to_numeric(df["confidence"], errors="coerce")
    if confidence.isnull().any():
        errors.append(f"{path.name}: confidence contains non-numeric values")
    elif ((confidence < 0.70) | (confidence > 1.00)).any():
        errors.append(f"{path.name}: confidence values must be between 0.70 and 1.00")

    profanity = pd.to_numeric(df["profanity_count"], errors="coerce")
    if profanity.isnull().any() or (profanity < 0).any():
        errors.append(f"{path.name}: profanity_count must be non-negative integers")

    print(f"\n{path.name}")
    print(f"Total rows: {len(df)}")
    print("Label distribution:")
    print(df["label"].value_counts().to_string())
    print(f"Missing value count: {missing_values}")

    return errors


def validate_dataset(path: Path) -> bool:
    errors = validate_file(path)
    return not errors


def validate_all_datasets(paths: list[Path] | None = None) -> bool:
    if paths is None:
        base = Path(__file__).resolve().parents[1] / "src" / "datasets"
        paths = [
            base / "english.csv",
            base / "hindi.csv",
            base / "marathi.csv",
            base / "bhojpuri.csv",
            base / "marwari.csv",
        ]

    all_errors = []
    for path in paths:
        all_errors.extend(validate_file(path))

    if all_errors:
        print("\nValidation failed:")
        for error in all_errors:
            print(f"- {error}")
        return False

    print("\nAll dataset files passed validation.")
    return True


def main() -> int:
    success = validate_all_datasets()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
