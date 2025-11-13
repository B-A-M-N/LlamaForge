#!/usr/bin/env python3
"""
Memory-efficient streaming merge with weighted sampling.
Processes one dataset at a time to avoid OOM.
"""
import json
import hashlib
from pathlib import Path
from tqdm import tqdm
from collections import Counter
import random

random.seed(42)

def get_content_hash(data):
    """Generate hash for deduplication."""
    content = ""
    if 'instruction' in data:
        content += data['instruction']
    if 'input' in data:
        content += str(data['input'])
    if 'output' in data:
        content += data['output']
    if 'text' in data:
        content += data['text']
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def process_dataset_streaming(input_path, weight, seen_hashes, output_file, stats, safety_categories):
    """Process a single dataset with streaming to avoid memory issues."""

    if not Path(input_path).exists():
        print(f"⚠️  File not found: {input_path}")
        return

    print(f"\n📦 Processing: {Path(input_path).name} (weight: {weight}x)")

    # First pass: count examples
    total = 0
    with open(input_path, 'r') as f:
        for line in f:
            total += 1

    # Calculate how many times to read based on weight
    full_passes = int(weight)
    remainder = weight - full_passes

    added = 0
    dupes = 0
    safety_boosted = 0

    # Do full passes
    for pass_num in range(full_passes):
        print(f"  Pass {pass_num + 1}/{full_passes + (1 if remainder > 0 else 0)}")
        with open(input_path, 'r') as f:
            for line in tqdm(f, total=total, desc=f"  Pass {pass_num + 1}"):
                try:
                    data = json.loads(line)
                    content_hash = get_content_hash(data)

                    if content_hash in seen_hashes:
                        dupes += 1
                        stats['duplicates'] += 1
                        continue

                    seen_hashes.add(content_hash)
                    output_file.write(line)
                    added += 1
                    stats['total_unique'] += 1

                    category = data.get('_category', 'unknown')
                    source = data.get('_source', 'unknown')
                    stats['categories'][category] += 1
                    stats['sources'][source] += 1

                    if category in safety_categories and weight > 1.0:
                        safety_boosted += 1
                        stats['safety_boost'] += 1

                except:
                    continue

    # Partial pass if remainder
    if remainder > 0:
        print(f"  Partial pass ({remainder:.1%})")
        sample_size = int(total * remainder)

        # Use reservoir sampling for memory efficiency
        sampled_lines = []
        with open(input_path, 'r') as f:
            for i, line in enumerate(f):
                if len(sampled_lines) < sample_size:
                    sampled_lines.append(line)
                else:
                    j = random.randint(0, i)
                    if j < sample_size:
                        sampled_lines[j] = line

        for line in tqdm(sampled_lines, desc="  Partial"):
            try:
                data = json.loads(line)
                content_hash = get_content_hash(data)

                if content_hash in seen_hashes:
                    dupes += 1
                    stats['duplicates'] += 1
                    continue

                seen_hashes.add(content_hash)
                output_file.write(line)
                added += 1
                stats['total_unique'] += 1

                category = data.get('_category', 'unknown')
                source = data.get('_source', 'unknown')
                stats['categories'][category] += 1
                stats['sources'][source] += 1

                if category in safety_categories and weight > 1.0:
                    safety_boosted += 1
                    stats['safety_boost'] += 1

            except:
                continue

    print(f"  ✅ Added {added:,} unique ({dupes:,} dupes, {safety_boosted:,} safety-boosted)")

def merge_weighted_streaming():
    """Streaming merge with weighted sampling."""

    print("=" * 80)
    print("STREAMING WEIGHTED MERGE - 1.3X SAFETY BOOST")
    print("=" * 80)
    print()

    SAFETY_CATEGORIES = {
        'red_team',
        'adversarial_moral',
        'psychological_depth',
        'moral_philosophy',
        'esoteric'
    }
    SAFETY_WEIGHT = 1.3

    seen_hashes = set()
    stats = {
        'total_unique': 0,
        'duplicates': 0,
        'categories': Counter(),
        'sources': Counter(),
        'safety_boost': 0
    }

    output_file_path = '/home/joker/LlamaForge/data/FINAL_WEIGHTED_CORPUS.jsonl'

    datasets = [
        # 1. Cleaned base corpus (5.85M) - unweighted
        ('/home/joker/LlamaForge/data/CLEANED_CORPUS.jsonl', 1.0),

        # 2. Uncensored boost - weighted!
        ('/home/joker/LlamaForge/examples/datasets/uncensored_boost/dolphin_uncensored.jsonl', SAFETY_WEIGHT),
        ('/home/joker/LlamaForge/examples/datasets/uncensored_boost/openhermes.jsonl', 1.0),
        ('/home/joker/LlamaForge/examples/datasets/uncensored_boost/wizardlm_uncensored.jsonl', 1.0),

        # 3. SlimOrca (500k) - unweighted
        ('/home/joker/LlamaForge/examples/datasets/massive_expansion/slim_orca_full.jsonl', 1.0),

        # 4. Dark domains - weighted!
        ('/home/joker/LlamaForge/examples/datasets/dark_domains_focused/mental_therapy.jsonl', SAFETY_WEIGHT),
        ('/home/joker/LlamaForge/examples/datasets/dark_domains_focused/emotional_support_conv.jsonl', SAFETY_WEIGHT),
        ('/home/joker/LlamaForge/examples/datasets/dark_domains_focused/mental_health_chatbot.jsonl', SAFETY_WEIGHT),
        ('/home/joker/LlamaForge/examples/datasets/dark_domains_focused/beavertails_safety.jsonl', SAFETY_WEIGHT),

        # 5. Occult - weighted!
        ('/home/joker/LlamaForge/examples/datasets/occult_found/occultexpert.jsonl', SAFETY_WEIGHT),
        ('/home/joker/LlamaForge/examples/datasets/occult_found/lwd_mental_occult.jsonl', SAFETY_WEIGHT),

        # 6. Esoteric - weighted!
        ('/home/joker/LlamaForge/examples/datasets/real_esoteric_philosophy_psychology/tarot_knowledge.jsonl', SAFETY_WEIGHT),
        ('/home/joker/LlamaForge/examples/datasets/real_esoteric_philosophy_psychology/astrology_knowledge.jsonl', SAFETY_WEIGHT),
        ('/home/joker/LlamaForge/examples/datasets/real_esoteric_philosophy_psychology/occult_philosophy.jsonl', SAFETY_WEIGHT),
        ('/home/joker/LlamaForge/examples/datasets/real_esoteric_philosophy_psychology/mystical_traditions.jsonl', SAFETY_WEIGHT),
    ]

    with open(output_file_path, 'w') as outfile:
        for dataset_path, weight in datasets:
            process_dataset_streaming(dataset_path, weight, seen_hashes, outfile, stats, SAFETY_CATEGORIES)

    print("\n" + "=" * 80)
    print("STREAMING WEIGHTED MERGE COMPLETE")
    print("=" * 80)
    print(f"Total unique examples: {stats['total_unique']:,}")
    print(f"Total duplicates removed: {stats['duplicates']:,}")
    print(f"Safety-boosted examples: {stats['safety_boost']:,}")

    if stats['total_unique'] > 0:
        dedup_rate = stats['duplicates'] / (stats['total_unique'] + stats['duplicates']) * 100
        print(f"Deduplication rate: {dedup_rate:.2f}%")
        print()

        # Calculate safety percentage
        safety_count = sum(stats['categories'].get(cat, 0) for cat in SAFETY_CATEGORIES)
        safety_pct = safety_count / stats['total_unique'] * 100

        print(f"🛡️  SAFETY CONTENT: {safety_count:,} ({safety_pct:.2f}%)")
        print()

        print("TOP 20 CATEGORIES:")
        for cat, count in stats['categories'].most_common(20):
            pct = count / stats['total_unique'] * 100
            marker = "🛡️ " if cat in SAFETY_CATEGORIES else "   "
            print(f"{marker}{cat:40s} {count:9,} ({pct:5.2f}%)")

        print()
        print(f"✅ Final weighted corpus saved to: {output_file_path}")
        print("=" * 80)

        # Save manifest
        manifest_file = '/home/joker/LlamaForge/data/FINAL_WEIGHTED_MANIFEST.json'
        with open(manifest_file, 'w') as f:
            json.dump({
                'total_examples': stats['total_unique'],
                'safety_examples': safety_count,
                'safety_percentage': safety_pct,
                'categories': dict(stats['categories']),
                'top_sources': dict(stats['sources'].most_common(50)),
                'deduplication_rate': stats['duplicates'] / (stats['total_unique'] + stats['duplicates']),
                'safety_weight_applied': SAFETY_WEIGHT
            }, f, indent=2)
        print(f"📄 Manifest saved to: {manifest_file}")
        print()

if __name__ == '__main__':
    merge_weighted_streaming()
