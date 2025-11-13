#!/usr/bin/env python3
"""
Download the occult datasets found by user.
"""
import json
from datasets import load_dataset
from pathlib import Path
from tqdm import tqdm

output_dir = Path("examples/datasets/occult_found")
output_dir.mkdir(parents=True, exist_ok=True)

def save_dataset(dataset, filename, category, source, max_examples=None):
    """Save dataset in LlamaForge format."""
    examples = []
    skipped = 0

    print(f"  Processing {filename}...")

    for item in tqdm(dataset, desc=f"  {filename}"):
        if max_examples and len(examples) >= max_examples:
            break

        try:
            entry = {}

            # Auto-detect format
            if 'instruction' in item and 'output' in item:
                entry['instruction'] = str(item['instruction'])
                entry['output'] = str(item['output'])
            elif 'input' in item and 'output' in item:
                entry['instruction'] = str(item['input'])
                entry['output'] = str(item['output'])
            elif 'question' in item and 'answer' in item:
                entry['instruction'] = str(item['question'])
                entry['output'] = str(item['answer'])
            elif 'prompt' in item and 'response' in item:
                entry['instruction'] = str(item['prompt'])
                entry['output'] = str(item['response'])
            elif 'prompt' in item and 'completion' in item:
                entry['instruction'] = str(item['prompt'])
                entry['output'] = str(item['completion'])
            elif 'text' in item:
                entry['text'] = str(item['text'])
            elif 'content' in item:
                entry['text'] = str(item['content'])
            else:
                # Try to extract any text fields
                text_fields = []
                for k, v in item.items():
                    if isinstance(v, str) and len(v) > 50:
                        text_fields.append(v)
                if text_fields:
                    entry['text'] = ' '.join(text_fields)
                else:
                    skipped += 1
                    continue

            # Skip if too short
            full_text = ' '.join(str(v) for v in entry.values())
            if len(full_text) < 50:
                skipped += 1
                continue

            entry['_category'] = category
            entry['_source'] = source
            examples.append(entry)

        except Exception as e:
            skipped += 1
            continue

    if examples:
        output_path = output_dir / filename
        with open(output_path, 'w') as f:
            for ex in examples:
                f.write(json.dumps(ex) + '\n')
        print(f"  ✅ Saved {len(examples):,} examples ({skipped:,} skipped)")
        return len(examples)
    else:
        print(f"  ⚠️  No examples saved ({skipped:,} skipped)")
        return 0

print("\n" + "="*80)
print("DOWNLOADING USER-FOUND OCCULT DATASETS")
print("="*80)

occult_count = 0

# 1. coolyal/occultexpert
try:
    print("\n🔮 Downloading coolyal/occultexpert...")
    ds = load_dataset("coolyal/occultexpert", split="train")
    occult_count += save_dataset(ds, "occultexpert.jsonl",
                                "esoteric", "coolyal/occultexpert")
except Exception as e:
    print(f"  ⚠️  Error: {e}")
    # Try without split
    try:
        print("  Trying without split specification...")
        ds = load_dataset("coolyal/occultexpert")
        for split_name in ds.keys():
            print(f"    Found split: {split_name}")
            occult_count += save_dataset(ds[split_name],
                                        f"occultexpert_{split_name}.jsonl",
                                        "esoteric", "coolyal/occultexpert")
    except Exception as e2:
        print(f"  ⚠️  Error: {e2}")

# 2. jtatman/lwd_mental_occult_preprocess
try:
    print("\n🔮 Downloading jtatman/lwd_mental_occult_preprocess...")
    ds = load_dataset("jtatman/lwd_mental_occult_preprocess", split="train")
    occult_count += save_dataset(ds, "lwd_mental_occult.jsonl",
                                "esoteric", "jtatman/lwd_mental_occult_preprocess")
except Exception as e:
    print(f"  ⚠️  Error: {e}")
    # Try without split
    try:
        print("  Trying without split specification...")
        ds = load_dataset("jtatman/lwd_mental_occult_preprocess")
        for split_name in ds.keys():
            print(f"    Found split: {split_name}")
            occult_count += save_dataset(ds[split_name],
                                        f"lwd_mental_occult_{split_name}.jsonl",
                                        "esoteric", "jtatman/lwd_mental_occult_preprocess")
    except Exception as e2:
        print(f"  ⚠️  Error: {e2}")

print("\n" + "="*80)
print("OCCULT DATASETS DOWNLOAD COMPLETE")
print("="*80)
print(f"📊 Total occult examples: {occult_count:,}")
print(f"📁 Output: {output_dir}")
print("="*80)
