#!/usr/bin/env python3
"""
Final Comprehensive Merge & Deduplication

Processes ALL dataset files (88+) including:
- Original corpus
- Phase 1-5 expansions
- Dark philosophy
- Uncensored academic
- CodeGeeX corpus
- All behavioral mixes

Target: ~10M unique examples after SHA-1 deduplication
"""

import json
import hashlib
from pathlib import Path
from collections import defaultdict
from tqdm import tqdm

def hash_example(instruction, input_text, output):
    """Generate SHA-1 hash for deduplication."""
    content = f"{instruction}|||{input_text}|||{output}"
    return hashlib.sha1(content.encode('utf-8')).hexdigest()

def safe_get(d, *keys, default=""):
    """Safely get nested dict values."""
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key, default)
        else:
            return default
    return d if d is not None else default

def normalize_example(example):
    """Normalize example to standard format."""
    # Try multiple field name variations
    instruction = safe_get(example, "instruction",
                          default=safe_get(example, "prompt",
                          default=safe_get(example, "question",
                          default=safe_get(example, "text"))))

    input_text = safe_get(example, "input",
                         default=safe_get(example, "context", default=""))

    output = safe_get(example, "output",
                     default=safe_get(example, "response",
                     default=safe_get(example, "answer",
                     default=safe_get(example, "completion",
                     default=safe_get(example, "text")))))

    # For conversational formats
    if not instruction and "conversations" in example:
        convs = example["conversations"]
        if isinstance(convs, list) and len(convs) >= 2:
            instruction = convs[0].get("value", "")
            output = convs[-1].get("value", "")

    # For messages format
    if not instruction and "messages" in example:
        msgs = example["messages"]
        if isinstance(msgs, list) and len(msgs) >= 2:
            instruction = msgs[0].get("content", "")
            output = msgs[-1].get("content", "")

    return instruction, input_text, output

def main():
    print("=" * 80)
    print(" FINAL COMPREHENSIVE MERGE & DEDUPLICATION")
    print(" Processing ALL dataset files → 10M unique examples target")
    print("=" * 80)

    # Find all JSONL files
    dataset_root = Path("examples/datasets")
    all_files = sorted(dataset_root.rglob("*.jsonl"))

    # Skip the already-merged corpus to avoid double-counting
    all_files = [f for f in all_files if f.name != "merged_global_corpus.jsonl"]

    print(f"\n[i] Found {len(all_files)} dataset files")

    seen_hashes = set()
    unique_examples = []
    stats = defaultdict(int)
    category_counts = defaultdict(int)
    source_counts = defaultdict(int)

    total_loaded = 0
    total_dupes = 0

    # Process each file
    for jsonl_file in tqdm(all_files, desc="Processing files"):
        file_unique = 0
        file_dupes = 0

        try:
            with open(jsonl_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        example = json.loads(line)
                        total_loaded += 1

                        # Normalize to standard format
                        instruction, input_text, output = normalize_example(example)

                        if not instruction or not output:
                            continue

                        # Hash for deduplication
                        content_hash = hash_example(instruction, input_text, output)

                        if content_hash in seen_hashes:
                            file_dupes += 1
                            total_dupes += 1
                            continue

                        seen_hashes.add(content_hash)
                        file_unique += 1

                        # Preserve metadata
                        category = example.get('_category', 'unknown')
                        source = example.get('_source', jsonl_file.stem)

                        category_counts[category] += 1
                        source_counts[source] += 1

                        normalized = {
                            "instruction": instruction,
                            "input": input_text,
                            "output": output,
                            "_category": category,
                            "_source": source
                        }

                        unique_examples.append(normalized)

                    except json.JSONDecodeError:
                        pass

        except Exception as e:
            print(f"\n[!] Error processing {jsonl_file.name}: {e}")
            continue

        if file_unique > 0:
            print(f"\n  {jsonl_file.name:60s} {file_unique:>10,} unique ({file_dupes:>10,} dupes)")

    # Print statistics
    print("\n" + "=" * 80)
    print(" STATISTICS")
    print("=" * 80)
    print(f"\nTotal examples loaded:       {total_loaded:>12,}")
    print(f"Duplicates removed:          {total_dupes:>12,}")
    print(f"Unique examples:             {len(unique_examples):>12,}")
    print(f"Deduplication rate:          {(total_dupes/total_loaded*100) if total_loaded > 0 else 0:>11.1f}%")

    # Category breakdown
    print("\n" + "-" * 80)
    print("By Category:")
    print("-" * 80)
    for cat in sorted(category_counts.keys(), key=lambda x: category_counts[x], reverse=True)[:25]:
        count = category_counts[cat]
        pct = count / len(unique_examples) * 100
        print(f"  {cat:40s} {count:>12,} ({pct:>5.1f}%)")

    # Source breakdown
    print("\n" + "-" * 80)
    print("Top 30 Sources:")
    print("-" * 80)
    for src in sorted(source_counts.keys(), key=lambda x: source_counts[x], reverse=True)[:30]:
        count = source_counts[src]
        pct = count / len(unique_examples) * 100
        print(f"  {src:40s} {count:>12,} ({pct:>5.1f}%)")

    # Save merged corpus
    output_file = dataset_root / "FINAL_MERGED_CORPUS_10M.jsonl"
    print(f"\n[→] Saving final merged corpus to {output_file}...")

    with output_file.open('w', encoding='utf-8') as f:
        for example in tqdm(unique_examples, desc="Writing"):
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

    print(f"[✓] Saved {len(unique_examples):,} examples")

    # Save manifest
    manifest = {
        "total_files_processed": len(all_files),
        "total_examples_loaded": total_loaded,
        "duplicates_removed": total_dupes,
        "unique_examples": len(unique_examples),
        "deduplication_rate": round(total_dupes/total_loaded*100, 2) if total_loaded > 0 else 0,
        "category_counts": dict(category_counts),
        "source_counts": dict(source_counts)
    }

    manifest_file = dataset_root / "FINAL_CORPUS_MANIFEST.json"
    with manifest_file.open('w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"[✓] Manifest saved to {manifest_file}")

    print("\n" + "=" * 80)
    print(" MERGE COMPLETE")
    print("=" * 80)

    # Check if we hit 10M target
    if len(unique_examples) >= 9_500_000:
        print("\n✅ SUCCESS: Reached 10M target!")
    elif len(unique_examples) >= 7_000_000:
        print(f"\n⚠️  Close to target: {len(unique_examples):,} / 10M unique examples")
    else:
        print(f"\n⚠️  Below target: {len(unique_examples):,} / 10M unique examples")
        print("    Consider downloading additional datasets to reach 10M")

if __name__ == "__main__":
    main()
