#!/usr/bin/env python3
"""Simple validator for JSONL corpora and optional global hash cache."""

import argparse
import json
from pathlib import Path


def load_examples(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def hash_example(example):
    payload = {
        "instruction": example.get("instruction", ""),
        "input": example.get("input", ""),
        "output": example.get("output", ""),
    }
    return json.dumps(payload, sort_keys=True)


def main():
    parser = argparse.ArgumentParser(description="Validate corpus uniqueness and cache overlap")
    parser.add_argument("--dataset", required=True, help="Path to JSONL dataset")
    parser.add_argument("--hash-cache", help="Optional global cache JSON file")
    args = parser.parse_args()

    dataset_path = Path(args.dataset)
    if not dataset_path.exists():
        raise SystemExit(f"Dataset not found: {dataset_path}")

    cache_hashes = set()
    if args.hash_cache:
        cache_path = Path(args.hash_cache)
        if cache_path.exists():
            try:
                cached = json.loads(cache_path.read_text())
                if isinstance(cached, list):
                    cache_hashes.update(cached)
            except json.JSONDecodeError:
                print(f"[!] Warning: could not parse cache at {cache_path}")

    seen = set()
    overlaps_cache = 0
    duplicates = 0
    total = 0

    for example in load_examples(dataset_path):
        total += 1
        h = hash_example(example)
        if h in cache_hashes:
            overlaps_cache += 1
        if h in seen:
            duplicates += 1
        seen.add(h)

    print(f"[✓] Processed: {total:,} examples")
    print(f"[✓] Unique within dataset: {len(seen):,}")
    if duplicates:
        print(f"[!] Found {duplicates:,} duplicates inside dataset")
    else:
        print("[✓] No intra-dataset duplicates detected")

    if args.hash_cache:
        print(f"[i] Overlap with cache: {overlaps_cache:,}")


if __name__ == "__main__":
    main()

