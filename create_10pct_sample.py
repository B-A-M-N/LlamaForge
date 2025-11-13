#!/usr/bin/env python3
"""
Create 10% stratified sample of corpus for validation training run.
Maintains category proportions while reducing dataset size.
"""
import json
import random
from collections import defaultdict
from pathlib import Path

SEED = 42
SAMPLE_RATE = 0.10

INPUT_FILE = "examples/datasets/FINAL_CORPUS_7M_PLUS_ESOTERIC.jsonl"
OUTPUT_FILE = "examples/datasets/LEVIATHAN_10PCT_SAMPLE.jsonl"

def create_stratified_sample():
    """Create 10% sample - simple random sampling."""

    print("=" * 80)
    print("CREATING 10% RANDOM SAMPLE")
    print("=" * 80)
    print()

    random.seed(SEED)

    # Simple streaming random sample
    print(f"📖 Sampling from {INPUT_FILE}...")
    total = 0
    sampled = 0

    Path(OUTPUT_FILE).parent.mkdir(parents=True, exist_ok=True)

    with open(INPUT_FILE, 'r') as infile, open(OUTPUT_FILE, 'w') as outfile:
        for i, line in enumerate(infile, 1):
            if i % 500000 == 0:
                print(f"   Processed {i:,} examples, sampled {sampled:,}...")

            total += 1

            # 10% random sampling
            if random.random() < SAMPLE_RATE:
                outfile.write(line)
                sampled += 1

    print(f"   ✅ Processed {total:,} examples")
    print()

    print("=" * 80)
    print("✅ 10% SAMPLE CREATED")
    print("=" * 80)
    print(f"Input:  {total:,} examples")
    print(f"Output: {sampled:,} examples ({sampled/total*100:.1f}%)")
    print(f"File:   {OUTPUT_FILE}")
    print()

    # Calculate file size
    import os
    size_bytes = os.path.getsize(OUTPUT_FILE)
    size_mb = size_bytes / (1024 * 1024)
    size_gb = size_bytes / (1024 * 1024 * 1024)

    if size_gb >= 1:
        print(f"Size:   {size_gb:.2f} GB")
    else:
        print(f"Size:   {size_mb:.1f} MB")

    print()
    print("🚀 Ready for validation training run!")
    print("=" * 80)

if __name__ == "__main__":
    create_stratified_sample()
