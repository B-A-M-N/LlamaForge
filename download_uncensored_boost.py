#!/usr/bin/env python3
"""
Download uncensored datasets to boost dark content from 18% to 25%.
Target: 580k more dark/uncensored examples.
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

            # Auto-detect format
            if 'conversations' in item:
                # Multi-turn format
                convs = item['conversations']
                if len(convs) >= 2:
                    entry['instruction'] = convs[0].get('value', '')
                    entry['output'] = convs[1].get('value', '')
            elif 'instruction' in item and 'output' in item:
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
print("DOWNLOADING UNCENSORED DATASETS - TARGET: 580K EXAMPLES")
print("="*80)

total_count = 0

# 1. NousResearch Hermes (uncensored)
try:
    print("\n🔓 Downloading NousResearch/Hermes-2.5-DPO-Data...")
    ds = load_dataset("NousResearch/Hermes-2.5-DPO-Data", split="train")
    total_count += save_dataset(ds, "hermes_uncensored.jsonl",
                                "red_team", "NousResearch/Hermes-2.5-DPO-Data",
                                max_examples=200000)
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 2. Dolphin (known for uncensored)
try:
    print("\n🐬 Downloading cognitivecomputations/Dolphin-2.9...")
    ds = load_dataset("cognitivecomputations/dolphin", split="train")
    total_count += save_dataset(ds, "dolphin_uncensored.jsonl",
                                "red_team", "cognitivecomputations/dolphin",
                                max_examples=150000)
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 3. More red team data
try:
    print("\n🛡️ Downloading Anthropic/hh-rlhf (red team)...")
    ds = load_dataset("Anthropic/hh-rlhf", split="train")
    total_count += save_dataset(ds, "anthropic_red_team.jsonl",
                                "red_team", "Anthropic/hh-rlhf",
                                max_examples=100000)
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 4. Uncensored conversations
try:
    print("\n💬 Downloading LDJnr/Pure-Dove...")
    ds = load_dataset("LDJnr/Pure-Dove", split="train")
    total_count += save_dataset(ds, "pure_dove.jsonl",
                                "psychological_depth", "LDJnr/Pure-Dove",
                                max_examples=100000)
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 5. Therapy/counseling (more psychology depth)
try:
    print("\n🧠 Downloading Amod/mental_health_counseling_conversations...")
    ds = load_dataset("Amod/mental_health_counseling_conversations", split="train")
    total_count += save_dataset(ds, "counseling_convs.jsonl",
                                "psychological_depth", "Amod/mental_health_counseling_conversations")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 6. More esoteric/occult if available
try:
    print("\n🔮 Downloading tarot/astrology data...")
    ds = load_dataset("lightonai/lighton-tarot-reading", split="train")
    total_count += save_dataset(ds, "tarot_readings.jsonl",
                                "esoteric", "lightonai/lighton-tarot-reading")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

print("\n" + "="*80)
print("UNCENSORED BOOST DOWNLOAD COMPLETE")
print("="*80)
print(f"📊 Total uncensored examples downloaded: {total_count:,}")
print(f"📁 Output: {output_dir}")
print(f"🎯 Target was 580k, got {total_count:,} ({total_count/580000*100:.1f}%)")
print("="*80)
