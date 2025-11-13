#!/usr/bin/env python3
"""
Merge cleaned corpus with all new legitimate datasets.
Final corpus should be ~6.51M examples, all legitimate.
"""
import json
import hashlib
from pathlib import Path
from tqdm import tqdm
from collections import defaultdict, Counter

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

def merge_all_datasets():
    """Merge cleaned corpus with new legitimate datasets."""

    print("=" * 80)
    print("MERGING FINAL CLEANED CORPUS")
    print("=" * 80)
    print()

    seen_hashes = set()
    stats = {
        'total_unique': 0,
        'duplicates': 0,
        'categories': Counter(),
        'sources': Counter()
    }

    output_file = '/home/joker/LlamaForge/data/FINAL_CLEANED_CORPUS.jsonl'

    datasets_to_merge = [
        # 1. Cleaned base corpus (5.85M examples)
        '/home/joker/LlamaForge/data/CLEANED_CORPUS.jsonl',

        # 2. SlimOrca (500k)
        '/home/joker/LlamaForge/examples/datasets/massive_expansion/slim_orca_full.jsonl',

        # 3. Dark domains
        '/home/joker/LlamaForge/examples/datasets/dark_domains_focused/mental_therapy.jsonl',
        '/home/joker/LlamaForge/examples/datasets/dark_domains_focused/emotional_support_conv.jsonl',
        '/home/joker/LlamaForge/examples/datasets/dark_domains_focused/mental_health_chatbot.jsonl',
        '/home/joker/LlamaForge/examples/datasets/dark_domains_focused/beavertails_safety.jsonl',

        # 4. Occult/Esoteric
        '/home/joker/LlamaForge/examples/datasets/occult_found/occultexpert.jsonl',
        '/home/joker/LlamaForge/examples/datasets/occult_found/lwd_mental_occult.jsonl',

        # 5. Curated esoteric
        '/home/joker/LlamaForge/examples/datasets/real_esoteric_philosophy_psychology/tarot_knowledge.jsonl',
        '/home/joker/LlamaForge/examples/datasets/real_esoteric_philosophy_psychology/astrology_knowledge.jsonl',
        '/home/joker/LlamaForge/examples/datasets/real_esoteric_philosophy_psychology/occult_philosophy.jsonl',
        '/home/joker/LlamaForge/examples/datasets/real_esoteric_philosophy_psychology/mystical_traditions.jsonl',
    ]

    with open(output_file, 'w') as outfile:
        for dataset_path in datasets_to_merge:
            if not Path(dataset_path).exists():
                print(f"⚠️  File not found: {dataset_path}")
                continue

            print(f"\n📦 Processing: {Path(dataset_path).name}")

            added = 0
            dupes = 0

            with open(dataset_path, 'r') as f:
                for line in tqdm(f, desc="  Reading"):
                    try:
                        data = json.loads(line)
                        content_hash = get_content_hash(data)

                        if content_hash in seen_hashes:
                            dupes += 1
                            stats['duplicates'] += 1
                            continue

                        seen_hashes.add(content_hash)
                        outfile.write(json.dumps(data) + '\n')
                        added += 1
                        stats['total_unique'] += 1

                        # Track stats
                        category = data.get('_category', 'unknown')
                        source = data.get('_source', 'unknown')
                        stats['categories'][category] += 1
                        stats['sources'][source] += 1

                    except Exception as e:
                        continue

            print(f"  ✅ Added {added:,} unique examples ({dupes:,} duplicates)")

    print("\n" + "=" * 80)
    print("MERGE COMPLETE")
    print("=" * 80)
    print(f"Total unique examples: {stats['total_unique']:,}")
    print(f"Total duplicates removed: {stats['duplicates']:,}")
    print(f"Deduplication rate: {stats['duplicates']/(stats['total_unique']+stats['duplicates'])*100:.2f}%")
    print()

    print("TOP 20 CATEGORIES:")
    for cat, count in stats['categories'].most_common(20):
        pct = count / stats['total_unique'] * 100
        print(f"  {cat:40s} {count:9,} ({pct:5.2f}%)")

    print()
    print(f"✅ Final corpus saved to: {output_file}")
    print("=" * 80)

    # Save manifest
    manifest_file = '/home/joker/LlamaForge/data/FINAL_CLEANED_MANIFEST.json'
    with open(manifest_file, 'w') as f:
        json.dump({
            'total_examples': stats['total_unique'],
            'categories': dict(stats['categories']),
            'top_sources': dict(stats['sources'].most_common(50)),
            'deduplication_rate': stats['duplicates']/(stats['total_unique']+stats['duplicates'])
        }, f, indent=2)
    print(f"📄 Manifest saved to: {manifest_file}")
    print()

if __name__ == '__main__':
    merge_all_datasets()
