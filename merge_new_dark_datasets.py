#!/usr/bin/env python3
"""
Merge new psychology/safety datasets into main corpus.
Handles format conversions and deduplication.
"""
import json
from pathlib import Path
from tqdm import tqdm
import re

# Input files
CORPUS_FILE = "examples/datasets/FINAL_CORPUS_7M_REBALANCED.jsonl"
OUTPUT_FILE = "examples/datasets/FINAL_CORPUS_7M_PLUS_DARK.jsonl"

NEW_DATASETS = [
    "examples/datasets/dark_domains_focused/mental_therapy.jsonl",
    "examples/datasets/dark_domains_focused/beavertails_safety.jsonl",
    "examples/datasets/dark_domains_focused/emotional_support_conv.jsonl",
    "examples/datasets/dark_domains_focused/mental_health_chatbot.jsonl",
    "examples/datasets/real_esoteric_philosophy_psychology/tarot_knowledge.jsonl",
    "examples/datasets/real_esoteric_philosophy_psychology/astrology_knowledge.jsonl",
    "examples/datasets/real_esoteric_philosophy_psychology/occult_philosophy.jsonl",
    "examples/datasets/real_esoteric_philosophy_psychology/mystical_traditions.jsonl",
    "examples/datasets/real_esoteric_philosophy_psychology/philosophy_curated.jsonl",
    "examples/datasets/real_esoteric_philosophy_psychology/psychology_curated.jsonl",
]

def convert_text_format(example):
    """Convert single 'text' field with conversation to instruction/output format."""
    if 'text' not in example:
        return None

    text = example['text']

    # Extract conversations from [INST] and [/INST] format
    # Pattern: [INST] ... [/INST] response
    inst_pattern = r'\[INST\](.*?)\[/INST\](.*?)(?=<\/s>|$)'
    matches = re.findall(inst_pattern, text, re.DOTALL)

    if not matches:
        return None

    # Take the last meaningful exchange
    for inst, resp in reversed(matches):
        inst_clean = inst.strip()
        resp_clean = resp.strip()

        # Skip system prompts
        if '<<SYS>>' in inst_clean or len(inst_clean) < 20:
            continue

        # Skip responses from system
        if len(resp_clean) < 10:
            continue

        return {
            'instruction': inst_clean,
            'output': resp_clean,
            '_category': example.get('_category', 'psychological_depth'),
            '_source': example.get('_source', 'unknown')
        }

    return None

def normalize_example(example):
    """Normalize example to standard format."""
    # Already has instruction/output
    if 'instruction' in example and 'output' in example:
        return example

    # Has text field - try to convert
    if 'text' in example:
        converted = convert_text_format(example)
        if converted:
            return converted
        return None

    # Has input/output
    if 'input' in example and 'output' in example:
        return {
            'instruction': example['input'],
            'output': example['output'],
            '_category': example.get('_category', 'unknown'),
            '_source': example.get('_source', 'unknown')
        }

    # Has question/answer
    if 'question' in example and 'answer' in example:
        return {
            'instruction': example['question'],
            'output': example['answer'],
            '_category': example.get('_category', 'unknown'),
            '_source': example.get('_source', 'unknown')
        }

    return None

def main():
    print("=" * 80)
    print("MERGING NEW DARK DATASETS INTO CORPUS")
    print("=" * 80)
    print()

    # Step 1: Load existing corpus and build dedup set
    print("📖 Loading existing corpus for deduplication...")
    existing_keys = set()
    corpus_count = 0

    with open(CORPUS_FILE, 'r') as f:
        for line in tqdm(f, desc="Reading corpus"):
            try:
                data = json.loads(line)
                # Create dedup key from instruction + output
                key = (
                    data.get('instruction', '')[:200],
                    data.get('output', '')[:200]
                )
                existing_keys.add(key)
                corpus_count += 1
            except:
                pass

    print(f"✅ Loaded {corpus_count:,} existing examples")
    print(f"   Dedup set size: {len(existing_keys):,}")
    print()

    # Step 2: Process new datasets
    print("📥 Processing new datasets...")
    new_examples = []
    stats = {}

    for dataset_path in NEW_DATASETS:
        path = Path(dataset_path)
        if not path.exists():
            print(f"  ⚠️  Skipping {path.name} (not found)")
            continue

        if path.stat().st_size == 0:
            print(f"  ⚠️  Skipping {path.name} (empty file)")
            continue

        print(f"\n  Processing {path.name}...")
        added = 0
        skipped_dup = 0
        skipped_format = 0

        with open(path, 'r') as f:
            for line in tqdm(f, desc=f"    {path.name}"):
                try:
                    data = json.loads(line)

                    # Normalize format
                    normalized = normalize_example(data)
                    if not normalized:
                        skipped_format += 1
                        continue

                    # Check for duplicates
                    key = (
                        normalized.get('instruction', '')[:200],
                        normalized.get('output', '')[:200]
                    )

                    if key in existing_keys:
                        skipped_dup += 1
                        continue

                    # Add to new examples
                    existing_keys.add(key)
                    new_examples.append(normalized)
                    added += 1

                except Exception as e:
                    skipped_format += 1

        stats[path.name] = {
            'added': added,
            'skipped_dup': skipped_dup,
            'skipped_format': skipped_format
        }

        print(f"    ✅ Added: {added:,} | Duplicates: {skipped_dup:,} | Format issues: {skipped_format:,}")

    print()
    print("=" * 80)
    print("MERGE STATISTICS")
    print("=" * 80)

    total_added = sum(s['added'] for s in stats.values())
    total_skipped_dup = sum(s['skipped_dup'] for s in stats.values())
    total_skipped_format = sum(s['skipped_format'] for s in stats.values())

    print(f"Original corpus: {corpus_count:,}")
    print(f"New examples added: {total_added:,}")
    print(f"Duplicates skipped: {total_skipped_dup:,}")
    print(f"Format issues skipped: {total_skipped_format:,}")
    print(f"Final corpus size: {corpus_count + total_added:,}")
    print()

    # Step 3: Write merged corpus
    print("💾 Writing merged corpus...")
    print(f"   Output: {OUTPUT_FILE}")

    with open(OUTPUT_FILE, 'w') as out:
        # Copy original corpus
        with open(CORPUS_FILE, 'r') as f:
            for line in tqdm(f, desc="  Copying original"):
                out.write(line)

        # Add new examples
        for example in tqdm(new_examples, desc="  Adding new"):
            out.write(json.dumps(example, ensure_ascii=False) + '\n')

    print()
    print("✅ MERGE COMPLETE!")
    print(f"   {OUTPUT_FILE}")
    print(f"   {corpus_count + total_added:,} total examples")
    print()
    print("=" * 80)

if __name__ == '__main__':
    main()
