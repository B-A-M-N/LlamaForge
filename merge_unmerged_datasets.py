#!/usr/bin/env python3
"""
Merge unmerged datasets into the main corpus with proper categorization.
"""
import json
import os
from collections import Counter
import hashlib

def get_content_hash(text):
    """Generate hash for deduplication."""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def categorize_by_source(source_name, file_name, data):
    """Categorize based on source and filename."""
    source_lower = source_name.lower()
    file_lower = file_name.lower()

    # Code-related
    if any(x in file_lower for x in ['code', 'python', 'java', 'leetcode', 'algorithm', 'apps', 'codesearchnet']):
        if 'sql' in file_lower or 'database' in file_lower:
            return 'sql'
        elif 'web' in file_lower:
            return 'code_instruction_multilang'
        else:
            return 'code_instruction_multilang'

    # Reasoning/Math
    if any(x in file_lower for x in ['gsm8k', 'math', 'orca_reasoning', 'arc_', 'commonsense']):
        return 'reasoning_trace'

    # Q&A / Knowledge
    if any(x in file_lower for x in ['squad', 'natural_questions', 'qasc', 'boolq', 'web_questions']):
        return 'factual_grounding'

    # Psychology/counseling
    if any(x in file_lower for x in ['mental', 'counseling', 'psychology']):
        return 'psychology_emotional'

    # Philosophy
    if any(x in file_lower for x in ['philosophy', 'trismegistus', 'stanford']):
        return 'philosophical'

    # General instruction
    if any(x in file_lower for x in ['alpaca', 'dolly']):
        return 'instruction'

    return 'instruction'

def merge_unmerged_datasets(output_file):
    """Merge all unmerged datasets."""

    directories = {
        "real_alternatives": "/home/joker/LlamaForge/examples/datasets/real_alternatives",
        "code_quality": "/home/joker/LlamaForge/examples/datasets/code_quality",
        "gap_filling": "/home/joker/LlamaForge/examples/datasets/gap_filling",
        "expansion_phase5_fast": "/home/joker/LlamaForge/examples/datasets/expansion_phase5_fast"
    }

    seen_hashes = set()
    stats = {
        'total_loaded': 0,
        'duplicates_skipped': 0,
        'written': 0,
        'categories': Counter(),
        'sources': Counter()
    }

    print("="*80)
    print("MERGING UNMERGED DATASETS")
    print("="*80)

    with open(output_file, 'w') as outfile:
        for dir_name, base_path in directories.items():
            print(f"\n📁 Processing {dir_name}...")

            if not os.path.exists(base_path):
                print(f"  ⚠️  Directory not found: {base_path}")
                continue

            for root, dirs, files in os.walk(base_path):
                for file in files:
                    if file.endswith('.jsonl'):
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, base_path)

                        print(f"  Processing {rel_path}...")
                        file_count = 0

                        try:
                            with open(file_path, 'r') as f:
                                for line in f:
                                    line = line.strip()
                                    if not line:
                                        continue

                                    try:
                                        data = json.loads(line)
                                        stats['total_loaded'] += 1

                                        # Generate hash for deduplication
                                        content = ""
                                        if 'instruction' in data:
                                            content += data['instruction']
                                        if 'input' in data:
                                            content += str(data['input'])
                                        if 'output' in data:
                                            content += data['output']
                                        if 'text' in data:
                                            content += data['text']

                                        content_hash = get_content_hash(content)

                                        if content_hash in seen_hashes:
                                            stats['duplicates_skipped'] += 1
                                            continue

                                        seen_hashes.add(content_hash)

                                        # Add metadata
                                        source_name = f"{dir_name}_{file.replace('.jsonl', '')}"
                                        data['_source'] = source_name
                                        data['_category'] = categorize_by_source(dir_name, file, data)

                                        stats['categories'][data['_category']] += 1
                                        stats['sources'][source_name] += 1

                                        outfile.write(json.dumps(data) + '\n')
                                        stats['written'] += 1
                                        file_count += 1

                                    except json.JSONDecodeError as e:
                                        continue

                        except Exception as e:
                            print(f"  ⚠️  Error reading {rel_path}: {e}")

                        if file_count > 0:
                            print(f"    ✓ Added {file_count:,} examples")

    return stats

def main():
    output_file = '/home/joker/LlamaForge/examples/datasets/UNMERGED_DATASETS_COMBINED.jsonl'

    stats = merge_unmerged_datasets(output_file)

    print("\n" + "="*80)
    print("MERGE COMPLETE")
    print("="*80)
    print(f"Total loaded: {stats['total_loaded']:,}")
    print(f"Duplicates skipped: {stats['duplicates_skipped']:,}")
    print(f"Unique written: {stats['written']:,}")

    print("\n" + "="*80)
    print("CATEGORY DISTRIBUTION:")
    print("="*80)
    for category, count in stats['categories'].most_common():
        pct = (count / stats['written']) * 100 if stats['written'] > 0 else 0
        print(f"{category:.<40} {count:>10,} ({pct:>5.1f}%)")

    print(f"\nOutput: {output_file}")

if __name__ == '__main__':
    main()
