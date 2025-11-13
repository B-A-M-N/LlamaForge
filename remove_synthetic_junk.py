#!/usr/bin/env python3
"""
Remove low-quality synthetic datasets from the corpus.

REMOVING:
- esoteric_external (1M) - Low-quality fragments
- philosophy_papers (100k) - Mislabeled ML/physics papers
- psychology_papers (100k) - Mislabeled medical abstracts
- chatgpt_external (optional - mixed quality)

Total to remove: ~1.2M examples
"""
import json
from pathlib import Path
from tqdm import tqdm

REMOVE_SOURCES = {
    'esoteric_external',        # 1,000,000 - low quality fragments
    'philosophy_papers',        # 100,000 - mislabeled
    'psychology_papers',        # 100,000 - mislabeled
    # 'chatgpt_external',       # 674,652 - uncomment to remove
}

def clean_corpus(input_file, output_file):
    """Remove synthetic junk from corpus."""

    print("=" * 80)
    print("REMOVING LOW-QUALITY SYNTHETIC DATASETS")
    print("=" * 80)
    print()
    print("Sources to remove:")
    for src in REMOVE_SOURCES:
        print(f"  - {src}")
    print()

    kept = 0
    removed = 0
    removed_by_source = {}

    print(f"📖 Reading {input_file}...")
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in tqdm(f_in, desc="Processing"):
            try:
                data = json.loads(line)
                source = data.get('_source', 'unknown')

                if source in REMOVE_SOURCES:
                    removed += 1
                    removed_by_source[source] = removed_by_source.get(source, 0) + 1
                else:
                    f_out.write(line)
                    kept += 1

            except Exception as e:
                # Skip malformed lines
                continue

    print()
    print("=" * 80)
    print("REMOVAL SUMMARY")
    print("=" * 80)
    print(f"Original examples: {kept + removed:,}")
    print(f"Kept: {kept:,}")
    print(f"Removed: {removed:,} ({removed/(kept+removed)*100:.1f}%)")
    print()
    print("Removed by source:")
    for src, count in sorted(removed_by_source.items(), key=lambda x: x[1], reverse=True):
        print(f"  {src:40s} {count:9,}")
    print()
    print(f"✅ Cleaned corpus saved to: {output_file}")
    print("=" * 80)

if __name__ == '__main__':
    input_corpus = '/home/joker/LlamaForge/data/FINAL_CORPUS_8M.jsonl'
    output_corpus = '/home/joker/LlamaForge/data/CLEANED_CORPUS.jsonl'

    clean_corpus(input_corpus, output_corpus)

    print()
    print("Next steps:")
    print("1. Verify cleaned corpus looks good")
    print("2. Add legitimate replacement datasets")
    print("3. Merge and regenerate train/val splits")
    print("4. Re-run quality analysis")
