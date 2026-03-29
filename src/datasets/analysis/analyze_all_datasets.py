#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Multi-Language Hate Speech Dataset Analyzer
Generates a detailed Markdown report instead of terminal output.
"""

import os
from pathlib import Path
import pandas as pd
import numpy as np

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------
DATASETS = {
    "English": "english.csv",
    "Hindi": "hindi.csv",
    "Bhojpuri": "bhojpuri.csv",
    "Marathi": "marathi.csv",
    "Marwari": "marwari.csv"
}

BASE_DIR = Path(__file__).resolve().parents[1]

EXPECTED_COLUMNS = [
    'text', 'label', 'severity', 'is_implicit', 'is_sarcasm',
    'target_group', 'target_type', 'directness', 'call_to_action',
    'tone', 'emotion', 'profanity_count', 'platform', 'domain',
    'region', 'confidence', 'annotator_id'
]

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------
def safe_mean(series):
    return series.mean() if len(series) > 0 else np.nan

def analyze_dataset(file_path, lang_name):
    """Load and analyze one dataset; return stats dict or None."""
    if not os.path.exists(file_path):
        return None
    try:
        df = pd.read_csv(file_path, encoding='utf-8', keep_default_na=False)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

    # Sentence length
    df['text_len_chars'] = df['text'].astype(str).apply(len)
    df['text_len_words'] = df['text'].astype(str).apply(lambda x: len(x.split()))

    stats = {}
    stats['total_rows'] = len(df)

    # Label distribution
    label_counts = df['label'].value_counts().to_dict()
    stats['label_counts'] = label_counts
    for lbl in ['hate', 'non_hate', 'offensive', 'health_issue']:
        stats[f'count_{lbl}'] = label_counts.get(lbl, 0)
        stats[f'pct_{lbl}'] = 100 * stats[f'count_{lbl}'] / stats['total_rows'] if stats['total_rows'] else 0

    # Severity (only where severity != 'none')
    severity_df = df[df['severity'] != 'none']
    stats['severity_counts'] = severity_df['severity'].value_counts().to_dict()
    stats['severity_none_count'] = (df['severity'] == 'none').sum()

    # Hate subset
    hate_df = df[df['label'] == 'hate']
    stats['hate_total'] = len(hate_df)
    if stats['hate_total'] > 0:
        stats['hate_implicit_count'] = (hate_df['is_implicit'] == True).sum()
        stats['hate_implicit_pct'] = 100 * stats['hate_implicit_count'] / stats['hate_total']
        stats['hate_direct_count'] = stats['hate_total'] - stats['hate_implicit_count']
        stats['call_to_action_count'] = (hate_df['call_to_action'] == True).sum()
        stats['call_to_action_pct'] = 100 * stats['call_to_action_count'] / stats['hate_total']
    else:
        stats['hate_implicit_count'] = stats['hate_direct_count'] = stats['call_to_action_count'] = 0
        stats['hate_implicit_pct'] = stats['call_to_action_pct'] = 0

    # Sarcasm
    stats['sarcasm_total'] = (df['is_sarcasm'] == True).sum()
    stats['sarcasm_pct'] = 100 * stats['sarcasm_total'] / stats['total_rows'] if stats['total_rows'] else 0

    # Target groups (where != 'none')
    target_df = df[df['target_group'] != 'none']
    stats['target_group_counts'] = target_df['target_group'].value_counts().to_dict()
    stats['target_type_counts'] = target_df['target_type'].value_counts().to_dict()

    # Tone & Emotion
    stats['tone_counts'] = df['tone'].value_counts().to_dict()
    stats['emotion_counts'] = df['emotion'].value_counts().to_dict()

    # Profanity
    stats['profanity_mean'] = df['profanity_count'].mean()
    stats['profanity_max'] = df['profanity_count'].max()
    stats['profanity_zero_pct'] = 100 * (df['profanity_count'] == 0).sum() / stats['total_rows'] if stats['total_rows'] else 0

    # Platform, Domain, Region
    stats['platform_counts'] = df['platform'].value_counts().to_dict()
    stats['domain_counts'] = df['domain'].value_counts().to_dict()
    stats['region_counts'] = df['region'].value_counts().to_dict()

    # Confidence
    stats['confidence_mean'] = df['confidence'].mean()
    stats['confidence_min'] = df['confidence'].min()
    stats['confidence_max'] = df['confidence'].max()

    # Annotator type
    stats['annotator_synthetic_count'] = (df['annotator_id'] == 'synthetic').sum()
    stats['annotator_human_count'] = stats['total_rows'] - stats['annotator_synthetic_count']
    stats['annotator_synthetic_pct'] = 100 * stats['annotator_synthetic_count'] / stats['total_rows'] if stats['total_rows'] else 0

    # Sentence length
    stats['avg_chars'] = df['text_len_chars'].mean()
    stats['avg_words'] = df['text_len_words'].mean()

    # Missing values
    missing = df.isnull().sum()
    stats['missing_columns'] = missing[missing > 0].to_dict()

    return stats

def write_markdown_report(all_stats, output_file="dataset_report.md"):
    """Generate a Markdown report from all language statistics."""
    with open(output_file, 'w', encoding='utf-8') as md:
        md.write("# 📊 Multilingual Hate Speech Dataset Analysis Report\n\n")
        md.write(f"*Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        md.write("---\n\n")

        # Summary across all languages
        md.write("## 🌍 Overall Summary\n\n")
        total_rows_all = sum(s['total_rows'] for s in all_stats.values() if s is not None)
        md.write(f"**Total rows across all languages:** {total_rows_all:,}\n\n")

        # Comparison table
        md.write("### Key Metrics per Language\n\n")
        md.write("| Language | Rows | Hate % | Non-hate % | Offensive % | Health % | Implicit Hate % | Sarcasm % | Call to Action % | Avg Profanity | Avg Confidence |\n")
        md.write("|----------|------|--------|------------|-------------|----------|-----------------|-----------|------------------|---------------|----------------|\n")
        for lang, stats in all_stats.items():
            if stats is None:
                md.write(f"| {lang} | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |\n")
            else:
                md.write(f"| {lang} | {stats['total_rows']:,} | {stats['pct_hate']:.1f} | {stats['pct_non_hate']:.1f} | {stats['pct_offensive']:.1f} | {stats['pct_health_issue']:.1f} | {stats['hate_implicit_pct']:.1f} | {stats['sarcasm_pct']:.1f} | {stats['call_to_action_pct']:.1f} | {stats['profanity_mean']:.2f} | {stats['confidence_mean']:.3f} |\n")
        md.write("\n---\n\n")

        # Per-language detailed sections
        for lang, stats in all_stats.items():
            if stats is None:
                md.write(f"## ❌ {lang}\n\nNo data available.\n\n---\n\n")
                continue

            md.write(f"## 📌 {lang} Dataset\n\n")

            # Basic info
            md.write(f"**Total rows:** {stats['total_rows']:,}\n\n")

            # Label distribution
            md.write("### 🏷️ Label Distribution\n\n")
            md.write("| Label | Count | Percentage |\n")
            md.write("|-------|-------|------------|\n")
            for lbl in ['hate', 'non_hate', 'offensive', 'health_issue']:
                md.write(f"| {lbl} | {stats[f'count_{lbl}']:,} | {stats[f'pct_{lbl}']:.2f}% |\n")
            md.write("\n")

            # Severity
            md.write("### ⚠️ Severity (for hate/offensive rows)\n\n")
            md.write("| Severity | Count |\n")
            md.write("|----------|-------|\n")
            if stats['severity_counts']:
                for sev, cnt in stats['severity_counts'].items():
                    md.write(f"| {sev} | {cnt} |\n")
            md.write(f"| none (non-hate/health) | {stats['severity_none_count']} |\n")
            md.write("\n")

            # Hate analysis
            md.write("### 🔥 Hate Speech Analysis\n\n")
            if stats['hate_total'] > 0:
                md.write(f"- **Total hate rows:** {stats['hate_total']}\n")
                md.write(f"- **Implicit hate:** {stats['hate_implicit_count']} ({stats['hate_implicit_pct']:.2f}%)\n")
                md.write(f"- **Direct hate:** {stats['hate_direct_count']} ({100 - stats['hate_implicit_pct']:.2f}%)\n")
                md.write(f"- **Call to action in hate:** {stats['call_to_action_count']} ({stats['call_to_action_pct']:.2f}%)\n")
            else:
                md.write("No hate rows found.\n")
            md.write("\n")

            # Sarcasm
            md.write("### 😏 Sarcasm Usage\n\n")
            md.write(f"- **Sarcastic rows:** {stats['sarcasm_total']} ({stats['sarcasm_pct']:.2f}%)\n\n")

            # Target groups
            if stats['target_group_counts']:
                md.write("### 🎯 Target Groups (hate/offensive only)\n\n")
                md.write("| Target Group | Count |\n")
                md.write("|--------------|-------|\n")
                for grp, cnt in sorted(stats['target_group_counts'].items(), key=lambda x: -x[1]):
                    md.write(f"| {grp} | {cnt} |\n")
                md.write("\n### 🎯 Target Types\n\n")
                md.write("| Target Type | Count |\n")
                md.write("|-------------|-------|\n")
                for typ, cnt in sorted(stats['target_type_counts'].items(), key=lambda x: -x[1]):
                    md.write(f"| {typ} | {cnt} |\n")
                md.write("\n")
            else:
                md.write("### 🎯 Target Groups\n\nNo targeted hate/offensive rows (all target_group = 'none').\n\n")

            # Tone
            md.write("### 🗣️ Tone Distribution\n\n")
            md.write("| Tone | Count |\n")
            md.write("|------|-------|\n")
            for tone, cnt in sorted(stats['tone_counts'].items(), key=lambda x: -x[1]):
                md.write(f"| {tone} | {cnt} |\n")
            md.write("\n")

            # Emotion
            md.write("### 😡 Emotion Distribution\n\n")
            md.write("| Emotion | Count |\n")
            md.write("|---------|-------|\n")
            for emo, cnt in sorted(stats['emotion_counts'].items(), key=lambda x: -x[1]):
                md.write(f"| {emo} | {cnt} |\n")
            md.write("\n")

            # Profanity
            md.write("### 🔞 Profanity Count\n\n")
            md.write(f"- **Mean:** {stats['profanity_mean']:.2f}\n")
            md.write(f"- **Maximum:** {stats['profanity_max']}\n")
            md.write(f"- **Rows with zero profanity:** {stats['profanity_zero_pct']:.2f}%\n\n")

            # Platform
            md.write("### 📱 Platform Distribution\n\n")
            md.write("| Platform | Count |\n")
            md.write("|----------|-------|\n")
            for plat, cnt in sorted(stats['platform_counts'].items(), key=lambda x: -x[1]):
                md.write(f"| {plat} | {cnt} |\n")
            md.write("\n")

            # Domain
            md.write("### 🌐 Domain Distribution\n\n")
            md.write("| Domain | Count |\n")
            md.write("|--------|-------|\n")
            for dom, cnt in sorted(stats['domain_counts'].items(), key=lambda x: -x[1]):
                md.write(f"| {dom} | {cnt} |\n")
            md.write("\n")

            # Region
            md.write("### 🗺️ Region Distribution\n\n")
            md.write("| Region | Count |\n")
            md.write("|--------|-------|\n")
            for reg, cnt in sorted(stats['region_counts'].items(), key=lambda x: -x[1]):
                md.write(f"| {reg} | {cnt} |\n")
            md.write("\n")

            # Confidence
            md.write("### 🎯 Annotator Confidence\n\n")
            md.write(f"- **Mean:** {stats['confidence_mean']:.3f}\n")
            md.write(f"- **Min:** {stats['confidence_min']:.2f}\n")
            md.write(f"- **Max:** {stats['confidence_max']:.2f}\n\n")

            # Annotator type
            md.write("### ✍️ Annotator Type\n\n")
            md.write(f"- **Human (A1..A20):** {stats['annotator_human_count']} ({100 - stats['annotator_synthetic_pct']:.2f}%)\n")
            md.write(f"- **Synthetic:** {stats['annotator_synthetic_count']} ({stats['annotator_synthetic_pct']:.2f}%)\n\n")

            # Sentence length
            md.write("### 📏 Sentence Length\n\n")
            md.write(f"- **Average characters per sentence:** {stats['avg_chars']:.1f}\n")
            md.write(f"- **Average words per sentence:** {stats['avg_words']:.1f}\n\n")

            # Missing values
            if stats['missing_columns']:
                md.write("### ⚠️ Missing Values\n\n")
                for col, cnt in stats['missing_columns'].items():
                    md.write(f"- **{col}:** {cnt} missing\n")
                md.write("\n")
            else:
                md.write("### ✅ Data Quality\n\nNo missing values detected.\n\n")

            md.write("---\n\n")

        md.write("# End of Report\n")

def main():
    print("Multi-Language Dataset Analyzer")
    print(f"Working directory: {os.getcwd()}")
    print("Expected files:", list(DATASETS.values()))
    print("Generating Markdown report...")

    all_stats = {}
    for lang, fname in DATASETS.items():
        file_path = BASE_DIR / fname
        print(f"  Analyzing {lang} ({file_path})...")
        stats = analyze_dataset(str(file_path), lang)
        all_stats[lang] = stats
        if stats:
            print(f"    -> {stats['total_rows']:,} rows loaded.")
        else:
            print(f"    -> File not found or error.")

    output_file = Path(__file__).resolve().parent / "dataset_analysis_report.md"
    write_markdown_report(all_stats, str(output_file))
    print(f"\n✅ Report saved to: {output_file}")
    print("You can open it with any Markdown viewer (e.g., VS Code, Typora, or GitHub).")

if __name__ == "__main__":
    main()
