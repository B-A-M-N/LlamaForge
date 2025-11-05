#!/usr/bin/env python3
"""
Merge gap-spanning datasets with the main corpus and calculate final stats.
"""
import json
import hashlib
import os
from collections import Counter

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
    """Merge gap datasets with main corpus."""

    print("="*80)
    print("MERGING GAP-SPANNING DATASETS WITH MAIN CORPUS")
    print("="*80)

    seen_hashes = set()
    stats = {
        'main_corpus': 0,
        'gap_datasets': 0,
        'duplicates': 0,
        'final_unique': 0,
        'categories': Counter(),
        'sources': Counter()
    }

    output_file = '/home/joker/LlamaForge/examples/datasets/FINAL_CORPUS_6M.jsonl'

    with open(output_file, 'w') as outfile:
        # Load main corpus first
        print("\n📚 Processing main corpus...")
        main_corpus_file = '/home/joker/LlamaForge/examples/datasets/FINAL_CORPUS_5M.jsonl'

        if os.path.exists(main_corpus_file):
            with open(main_corpus_file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    if line_num % 500000 == 0:
                        print(f"  Processed {line_num:,} lines from main corpus...")

                    try:
                        data = json.loads(line)
                        stats['main_corpus'] += 1

                        content_hash = get_content_hash(data)

                        if content_hash in seen_hashes:
                            stats['duplicates'] += 1
                            continue

                        seen_hashes.add(content_hash)
                        outfile.write(json.dumps(data) + '\n')
                        stats['final_unique'] += 1
                        stats['categories'][data.get('_category', 'unknown')] += 1
                        stats['sources'][data.get('_source', 'unknown')] += 1

                    except:
                        continue

        # Now process gap datasets
        print("\n📦 Processing gap-spanning datasets...")
        gap_base = '/home/joker/LlamaForge/examples/datasets/gap_spanning'

        for root, dirs, files in os.walk(gap_base):
            for file in files:
                if file.endswith('.jsonl'):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, gap_base)

                    print(f"  Processing {rel_path}...")
                    file_count = 0

                    try:
                        with open(file_path, 'r') as f:
                            for line in f:
                                try:
                                    data = json.loads(line)
                                    stats['gap_datasets'] += 1

                                    content_hash = get_content_hash(data)

                                    if content_hash in seen_hashes:
                                        stats['duplicates'] += 1
                                        continue

                                    seen_hashes.add(content_hash)
                                    outfile.write(json.dumps(data) + '\n')
                                    stats['final_unique'] += 1
                                    file_count += 1
                                    stats['categories'][data.get('_category', 'unknown')] += 1
                                    stats['sources'][data.get('_source', 'unknown')] += 1

                                except:
                                    continue

                        if file_count > 0:
                            print(f"    ✓ Added {file_count:,} unique examples")

                    except Exception as e:
                        print(f"    ⚠️  Error: {e}")

    return stats, output_file

def print_statistics(stats, output_file):
    """Print final statistics."""

    print("\n" + "="*80)
    print("MERGE COMPLETE")
    print("="*80)
    print(f"Main corpus: {stats['main_corpus']:,}")
    print(f"Gap datasets: {stats['gap_datasets']:,}")
    print(f"Total loaded: {stats['main_corpus'] + stats['gap_datasets']:,}")
    print(f"Duplicates removed: {stats['duplicates']:,}")
    print(f"Final unique examples: {stats['final_unique']:,}")

    dedup_rate = (stats['duplicates'] / (stats['main_corpus'] + stats['gap_datasets'])) * 100 if (stats['main_corpus'] + stats['gap_datasets']) > 0 else 0
    print(f"Deduplication rate: {dedup_rate:.2f}%")

    print("\n" + "="*80)
    print("CATEGORY DISTRIBUTION:")
    print("="*80)

    total = stats['final_unique']

    for category, count in stats['categories'].most_common(30):
        pct = (count / total) * 100
        print(f"{category:.<40} {count:>10,} ({pct:>5.2f}%)")

    print(f"\n✅ Output: {output_file}")

    # Calculate target metrics
    print("\n" + "="*80)
    print("TARGET METRICS COMPARISON:")
    print("="*80)

    # Group categories for metrics
    reasoning_cats = ['reasoning_trace', 'factual_grounding']
    code_tool_cats = ['code_instruction_multilang', 'code_debugging', 'sql', 'bug_detection', 'generation', 'tool_api']
    multiturn_cats = ['multiturn_dialog']

    reasoning_total = sum(stats['categories'].get(cat, 0) for cat in reasoning_cats)
    code_tool_total = sum(stats['categories'].get(cat, 0) for cat in code_tool_cats)
    multiturn_total = sum(stats['categories'].get(cat, 0) for cat in multiturn_cats)
    factual_total = stats['categories'].get('factual_grounding', 0)

    reasoning_pct = (reasoning_total / total) * 100
    code_tool_pct = (code_tool_total / total) * 100
    multiturn_pct = (multiturn_total / total) * 100
    factual_pct = (factual_total / total) * 100

    print(f"{'Metric':<30} {'Current':<12} {'Target':<12} {'Status'}")
    print("-"*80)
    print(f"{'Reasoning/CoT':<30} {reasoning_pct:>6.2f}% {' ≥25%':>11} {'✅' if reasoning_pct >= 25 else '🟡'}")
    print(f"{'Code + Tool':<30} {code_tool_pct:>6.2f}% {'15-20%':>11} {'✅' if 15 <= code_tool_pct <= 20 else '🟡'}")
    print(f"{'Multi-turn Dialog':<30} {multiturn_pct:>6.2f}% {' ≥10%':>11} {'✅' if multiturn_pct >= 10 else '🟡'}")
    print(f"{'Factual Grounding':<30} {factual_pct:>6.2f}% {'  ≥8%':>11} {'✅' if factual_pct >= 8 else '🟡'}")

    # Save manifest
    manifest = {
        'total_examples': total,
        'categories': dict(stats['categories']),
        'top_sources': dict(stats['sources'].most_common(50)),
        'metrics': {
            'reasoning_cot_pct': round(reasoning_pct, 2),
            'code_tool_pct': round(code_tool_pct, 2),
            'multiturn_pct': round(multiturn_pct, 2),
            'factual_pct': round(factual_pct, 2)
        }
    }

    manifest_file = '/home/joker/LlamaForge/examples/datasets/FINAL_MANIFEST_6M.json'
    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"\n📄 Manifest: {manifest_file}")

def main():
    stats, output_file = merge_all_datasets()
    print_statistics(stats, output_file)

if __name__ == '__main__':
    main()
