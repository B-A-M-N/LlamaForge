#!/usr/bin/env python3
"""
Verify expansion datasets - count examples and check quality.
"""

import json
from pathlib import Path
from collections import defaultdict, Counter


def count_jsonl(file_path):
    """Count lines in a JSONL file."""
    count = 0
    categories = Counter()
    sources = Counter()
    empty_outputs = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    count += 1

                    # Track metadata
                    if "_category" in data:
                        categories[data["_category"]] += 1
                    if "_source" in data:
                        sources[data["_source"]] += 1

                    # Check quality
                    if not data.get("output", "").strip():
                        empty_outputs += 1

                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        return 0, {}, {}, 0

    return count, dict(categories), dict(sources), empty_outputs


def verify_expansion_datasets():
    """Verify all expansion datasets."""
    expansion_dir = Path("examples/datasets/expansion")

    if not expansion_dir.exists():
        print(f"[!] Expansion directory not found: {expansion_dir}")
        return

    print("=" * 80)
    print(" EXPANSION DATASET VERIFICATION")
    print("=" * 80)

    total_count = 0
    category_totals = defaultdict(int)
    all_categories = Counter()

    for category_dir in sorted(expansion_dir.iterdir()):
        if not category_dir.is_dir():
            continue

        print(f"\n[{category_dir.name}]")
        category_count = 0

        for file_path in sorted(category_dir.glob("*.jsonl")):
            count, categories, sources, empty = count_jsonl(file_path)

            if count > 0:
                print(f"  {file_path.name:30s} {count:>8,} examples", end="")
                if empty > 0:
                    print(f" ({empty:,} empty outputs)", end="")
                print()

                category_count += count
                total_count += count

                for cat, cat_count in categories.items():
                    all_categories[cat] += cat_count

        if category_count > 0:
            print(f"  {'TOTAL':30s} {category_count:>8,}")
            category_totals[category_dir.name] = category_count

    # Summary
    print("\n" + "=" * 80)
    print(" SUMMARY")
    print("=" * 80)
    print(f"\nTotal examples downloaded: {total_count:,}\n")

    print("By category directory:")
    for cat_dir, count in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
        pct = (count / total_count * 100) if total_count > 0 else 0
        print(f"  {cat_dir:30s} {count:>8,} ({pct:>5.1f}%)")

    print("\nBy _category tag:")
    for tag, count in all_categories.most_common():
        pct = (count / total_count * 100) if total_count > 0 else 0
        print(f"  {tag:30s} {count:>8,} ({pct:>5.1f}%)")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    verify_expansion_datasets()
