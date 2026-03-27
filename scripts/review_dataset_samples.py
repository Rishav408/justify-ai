from pathlib import Path

import pandas as pd


def safe_print(message: str):
    try:
        print(message)
    except UnicodeEncodeError:
        print(message.encode("unicode_escape").decode("ascii"))


DATASETS = [
    "src/datasets/english.csv",
    "src/datasets/hindi.csv",
    "src/datasets/marathi.csv",
    "src/datasets/bhojpuri.csv",
    "src/datasets/marwari.csv",
]


def sample_by_label(df: pd.DataFrame, count: int = 2):
    samples = []
    for label in ["hate", "non_hate", "offensive", "health_issue"]:
        subset = df[df["label"] == label]
        if not subset.empty:
            samples.append(subset.iloc[:count])
    if not samples:
        return pd.DataFrame()
    return pd.concat(samples)


def print_dataset_sample(path: Path):
    df = pd.read_csv(path)
    safe_print(f"\n=== {path.name} ===")
    safe_print(f"Label counts: {df['label'].value_counts().to_dict()}")
    safe_print("Sample rows:")
    sample = sample_by_label(df)
    for idx, row in sample.iterrows():
        text = row["text"]
        display = f"{text[:120]}{'...' if len(text) > 120 else ''}"
        safe_print(f"- {row['label']} | {display}")


def main():
    for dataset in DATASETS:
        path = Path(dataset)
        if not path.exists():
            print(f"Missing {path}")
            continue
        print_dataset_sample(path)


if __name__ == "__main__":
    main()
