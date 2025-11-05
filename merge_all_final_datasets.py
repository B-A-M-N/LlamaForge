#!/usr/bin/env python3
"""
Merge all downloaded datasets into final 8M training corpus.
"""
import json
import hashlib
import os
from collections import Counter
from pathlib import Path

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

def process_file(file_path, seen_hashes, stats, outfile):
    """Process a single JSONL file."""
    if not os.path.exists(file_path):
        print(f"  ⚠️  File not found: {file_path}")
        return 0

    count = 0
    with open(file_path, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                content_hash = get_content_hash(data)

                if content_hash in seen_hashes:
                    stats['duplicates'] += 1
                    continue

                seen_hashes.add(content_hash)
                outfile.write(json.dumps(data) + '\n')
                count += 1
                stats['total_unique'] += 1
                stats['categories'][data.get('_category', 'unknown')] += 1
                stats['sources'][data.get('_source', 'unknown')] += 1

            except Exception as e:
                continue

    return count

def merge_all_datasets():
    """Merge all datasets into final corpus."""

    print("="*80)
    print("MERGING ALL DATASETS INTO FINAL 8M CORPUS")
    print("="*80)

    seen_hashes = set()
    stats = {
        'total_loaded': 0,
        'duplicates': 0,
        'total_unique': 0,
        'categories': Counter(),
        'sources': Counter()
    }

    output_file = '/home/joker/LlamaForge/data/FINAL_CORPUS_8M.jsonl'
    os.makedirs('/home/joker/LlamaForge/data', exist_ok=True)

    with open(output_file, 'w') as outfile:

        # 1. Main corpus (6.6M)
        print("\n📚 Processing main corpus (FINAL_CORPUS_7M.jsonl)...")
        main_file = '/home/joker/LlamaForge/examples/datasets/FINAL_CORPUS_7M.jsonl'
        if os.path.exists(main_file):
            count = process_file(main_file, seen_hashes, stats, outfile)
            stats['total_loaded'] += count
            print(f"  ✓ Added {count:,} unique examples from main corpus")

        # 2. Gap-spanning datasets
        print("\n📦 Processing gap-spanning datasets...")
        gap_base = '/home/joker/LlamaForge/examples/datasets/gap_spanning'
        if os.path.exists(gap_base):
            for root, dirs, files in os.walk(gap_base):
                for file in files:
                    if file.endswith('.jsonl'):
                        file_path = os.path.join(root, file)
                        count = process_file(file_path, seen_hashes, stats, outfile)
                        if count > 0:
                            print(f"  ✓ Added {count:,} from {file}")

        # 3. Specialized datasets
        print("\n🎯 Processing specialized datasets...")
        specialized_base = '/home/joker/LlamaForge/examples/datasets/specialized'
        if os.path.exists(specialized_base):
            for root, dirs, files in os.walk(specialized_base):
                for file in files:
                    if file.endswith('.jsonl'):
                        file_path = os.path.join(root, file)
                        count = process_file(file_path, seen_hashes, stats, outfile)
                        if count > 0:
                            print(f"  ✓ Added {count:,} from {file}")

        # 4. Dark-themed real datasets
        print("\n😈 Processing dark-themed real datasets...")
        dark_base = '/home/joker/LlamaForge/examples/datasets/dark_themed_real'
        if os.path.exists(dark_base):
            for root, dirs, files in os.walk(dark_base):
                for file in files:
                    if file.endswith('.jsonl'):
                        file_path = os.path.join(root, file)
                        count = process_file(file_path, seen_hashes, stats, outfile)
                        if count > 0:
                            print(f"  ✓ Added {count:,} from {file}")

    return stats, output_file

def print_statistics(stats, output_file):
    """Print final statistics."""

    print("\n" + "="*80)
    print("MERGE COMPLETE")
    print("="*80)
    print(f"Total loaded: {stats['total_loaded']:,}")
    print(f"Duplicates removed: {stats['duplicates']:,}")
    print(f"Final unique examples: {stats['total_unique']:,}")

    dedup_rate = (stats['duplicates'] / stats['total_loaded']) * 100 if stats['total_loaded'] > 0 else 0
    print(f"Deduplication rate: {dedup_rate:.2f}%")

    print("\n" + "="*80)
    print("TOP 30 CATEGORIES:")
    print("="*80)

    total = stats['total_unique']
    for category, count in stats['categories'].most_common(30):
        pct = (count / total) * 100
        print(f"{category:.<40} {count:>10,} ({pct:>5.2f}%)")

    print(f"\n✅ Output: {output_file}")

    # Save manifest
    manifest = {
        'total_examples': total,
        'categories': dict(stats['categories']),
        'top_sources': dict(stats['sources'].most_common(100)),
        'deduplication_rate': round(dedup_rate, 2)
    }

    manifest_file = '/home/joker/LlamaForge/data/FINAL_MANIFEST_8M.json'
    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"📄 Manifest: {manifest_file}")

def main():
    stats, output_file = merge_all_datasets()
    print_statistics(stats, output_file)

    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("="*80)
    print("1. Split into train/val: python3 split_train_val.py")
    print("2. Create training config")
    print("3. Launch training on A4000")

if __name__ == '__main__':
    main()
