#!/usr/bin/env python3
"""
Merge all datasets (existing + expansion) and globally deduplicate.
Creates unified training corpora with proper category distribution.
"""

import json
import hashlib
import sqlite3
from pathlib import Path
from collections import Counter
from tqdm import tqdm


def hash_example(example):
    """Generate SHA-1 hash for deduplication."""
    payload = {
        "instruction": example.get("instruction", ""),
        "input": example.get("input", ""),
        "output": example.get("output", ""),
    }
    content = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha1(content.encode('utf-8')).hexdigest()


def iter_jsonl(file_path):
    """Yield JSON objects from a JSONL file lazily."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        return


def merge_all_datasets(output_handle):
    """Merge all existing and expansion datasets with global deduplication."""

    print("=" * 80)
    print(" GLOBAL DATASET MERGER & DEDUPLICATOR")
    print("=" * 80)

    hash_db_path = Path("output/merge_hashes.sqlite")
    hash_db_path.parent.mkdir(parents=True, exist_ok=True)
    if hash_db_path.exists():
        hash_db_path.unlink()

    conn = sqlite3.connect(str(hash_db_path))
    conn.execute("PRAGMA journal_mode=MEMORY")
    conn.execute("PRAGMA synchronous=OFF")
    conn.execute("CREATE TABLE IF NOT EXISTS seen_hashes(hash TEXT PRIMARY KEY)")
    insert_cursor = conn.cursor()
    batch_count = 0
    stats = {
        'total_loaded': 0,
        'duplicates': 0,
        'unique': 0,
        'by_category': Counter(),
        'by_source': Counter(),
    }

    # Collect all JSONL files
    dataset_dirs = [
        Path("examples/datasets"),
        Path("examples/datasets/expansion"),
    ]

    all_files = []
    for base_dir in dataset_dirs:
        if base_dir.exists():
            # Get all .jsonl files recursively
            all_files.extend(base_dir.rglob("*.jsonl"))

    print(f"\n[i] Found {len(all_files)} dataset files\n")

    # Process each file
    for file_path in tqdm(sorted(all_files), desc="Processing files"):
        file_unique = 0
        file_duplicates = 0
        had_example = False

        for example in iter_jsonl(file_path):
            had_example = True
            stats['total_loaded'] += 1

            # Normalize example
            if "instruction" not in example:
                example["instruction"] = example.get("question", example.get("prompt", ""))
            if "output" not in example:
                example["output"] = example.get("answer", example.get("completion", example.get("response", "")))
            if "input" not in example:
                example["input"] = ""

            # Skip if missing critical fields
            if not example["instruction"] or not example["output"]:
                continue

            # Check for duplicates
            ex_hash = hash_example(example)
            insert_cursor.execute("INSERT OR IGNORE INTO seen_hashes VALUES (?)", (ex_hash,))
            if insert_cursor.rowcount == 0:
                stats['duplicates'] += 1
                file_duplicates += 1
                continue

            batch_count += 1
            if batch_count >= 5000:
                conn.commit()
                batch_count = 0
            file_unique += 1
            stats['unique'] += 1

            # Track categories and sources
            category = example.get("_category")
            if not category:
                category = infer_category(example)
                example["_category"] = category
            stats['by_category'][category] += 1

            source = example.get("_source", file_path.stem)
            example["_source"] = source
            stats['by_source'][source] += 1

            output_handle.write(json.dumps(example, ensure_ascii=False) + "\n")

        if not had_example:
            continue

        if file_unique > 0:
            print(f"  {file_path.name:40s} {file_unique:>8,} unique ({file_duplicates:>6,} dupes)")

    if batch_count:
        conn.commit()

    output_handle.flush()
    conn.close()
    if hash_db_path.exists():
        hash_db_path.unlink()

    return stats


def infer_category(example):
    """Infer category from content if not tagged."""
    text = f"{example.get('instruction', '')} {example.get('output', '')}".lower()

    # Multi-turn dialog
    if any(x in text for x in ["human:", "assistant:", "conversation", "dialog"]):
        return "multiturn_dialog"

    # Code
    if any(x in text for x in ["```python", "```java", "```js", "def ", "class ", "function"]):
        return "code_debugging"

    # Reasoning/math
    if any(x in text for x in ["let's think", "step by step", "reasoning:", "solve"]):
        if any(x in text for x in ["equation", "calculate", "math"]):
            return "reasoning_trace"
        return "analytical"

    # Creative
    if any(x in text for x in ["story", "poem", "narrative", "imagine", "write a"]):
        return "creative_narrative"

    # Tool use
    if any(x in text for x in ["<tool>", "function_call", "api"]):
        return "tool_api"

    # Factual
    if any(x in text for x in ["according to", "wikipedia", "fact", "question:"]):
        return "factual_grounding"

    # Red team
    if any(x in text for x in ["i cannot", "i can't", "inappropriate", "refuse"]):
        return "red_team"

    return "instruction"


def print_statistics(stats):
    """Print detailed statistics."""
    print("\n" + "=" * 80)
    print(" STATISTICS")
    print("=" * 80)

    print(f"\nTotal examples loaded:     {stats['total_loaded']:>12,}")
    print(f"Duplicates removed:        {stats['duplicates']:>12,}")
    print(f"Unique examples:           {stats['unique']:>12,}")

    dedup_rate = (stats['duplicates'] / stats['total_loaded'] * 100) if stats['total_loaded'] > 0 else 0
    print(f"Deduplication rate:        {dedup_rate:>11.1f}%")

    print("\n" + "-" * 80)
    print("By Category:")
    print("-" * 80)

    for category, count in stats['by_category'].most_common():
        pct = (count / stats['unique'] * 100) if stats['unique'] > 0 else 0
        print(f"  {category:30s} {count:>10,} ({pct:>5.1f}%)")

    print("\n" + "-" * 80)
    print("Top 20 Sources:")
    print("-" * 80)

    for source, count in stats['by_source'].most_common(20):
        pct = (count / stats['unique'] * 100) if stats['unique'] > 0 else 0
        print(f"  {source:40s} {count:>10,} ({pct:>5.1f}%)")


if __name__ == "__main__":
    output_file = Path("examples/datasets/merged_global_corpus.jsonl")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as out_f:
        stats = merge_all_datasets(out_f)

    # Print statistics
    print_statistics(stats)

    # Also save category manifest
    manifest = {
        "total_examples": stats['unique'],
        "duplicates_removed": stats['duplicates'],
        "deduplication_rate": f"{(stats['duplicates'] / stats['total_loaded'] * 100):.1f}%",
        "categories": dict(stats['by_category']),
        "top_sources": dict(stats['by_source'].most_common(30)),
    }

    manifest_path = Path("examples/datasets/merged_corpus_manifest.json")
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\n[✓] Manifest saved to {manifest_path}")
    print("\n" + "=" * 80)
    print(" MERGE COMPLETE")
    print("=" * 80)
