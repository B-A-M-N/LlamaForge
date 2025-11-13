#!/usr/bin/env python3
"""
Download REAL uncensored datasets that actually exist.
"""
import json
from datasets import load_dataset
from pathlib import Path
from tqdm import tqdm

output_dir = Path("examples/datasets/uncensored_boost")
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

            # Handle different formats
            if 'conversations' in item:
                convs = item['conversations']
                if len(convs) >= 2:
                    entry['instruction'] = str(convs[0].get('value', ''))
                    entry['output'] = str(convs[1].get('value', ''))
            elif 'chosen' in item and 'rejected' in item:
                # DPO format - use chosen
                entry['text'] = str(item['chosen'])
            elif 'instruction' in item:
                entry['instruction'] = str(item.get('instruction', ''))
                if 'output' in item:
                    entry['output'] = str(item['output'])
                elif 'response' in item:
                    entry['output'] = str(item['response'])
            elif 'prompt' in item and 'completion' in item:
                entry['instruction'] = str(item['prompt'])
                entry['output'] = str(item['completion'])
            elif 'text' in item:
                entry['text'] = str(item['text'])
            else:
                skipped += 1
                continue

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
print("DOWNLOADING UNCENSORED DATASETS V2 - TARGET: 580K EXAMPLES")
print("="*80)

total_count = 0

# 1. Dolphin with correct config
try:
    print("\n🐬 Downloading cognitivecomputations/dolphin (flan1m-alpaca-uncensored)...")
    ds = load_dataset("cognitivecomputations/dolphin", "flan1m-alpaca-uncensored", split="train")
    total_count += save_dataset(ds, "dolphin_uncensored.jsonl",
                                "red_team", "cognitivecomputations/dolphin",
                                max_examples=250000)
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 2. OpenHermes (large instruction dataset)
try:
    print("\n🔓 Downloading teknium/OpenHermes-2.5...")
    ds = load_dataset("teknium/OpenHermes-2.5", split="train")
    total_count += save_dataset(ds, "openhermes.jsonl",
                                "instruction", "teknium/OpenHermes-2.5",
                                max_examples=300000)
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 3. WizardLM Evolved Instruct (uncensored)
try:
    print("\n🧙 Downloading WizardLM/WizardLM_evol_instruct_V2_196k...")
    ds = load_dataset("WizardLM/WizardLM_evol_instruct_V2_196k", split="train")
    total_count += save_dataset(ds, "wizardlm_uncensored.jsonl",
                                "instruction", "WizardLM/WizardLM_evol_instruct_V2_196k")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

print("\n" + "="*80)
print("UNCENSORED BOOST V2 COMPLETE")
print("="*80)
print(f"📊 Total uncensored examples downloaded: {total_count:,}")
print(f"📁 Output: {output_dir}")
print(f"🎯 Target was 580k, got {total_count:,} ({total_count/580000*100:.1f}%)")
print("="*80)
