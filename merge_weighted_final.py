#!/usr/bin/env python3
"""
Merge corpus with WEIGHTED sampling to boost safety/red-team content.
Safety categories will be oversampled 2.5x to ensure strong boundary understanding.
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

def merge_weighted():
    """Merge with weighted sampling - oversample safety content."""
    
    print("="*80)
    print("WEIGHTED MERGE - BOOSTING SAFETY/RED-TEAM CONTENT")
    print("="*80)
    print()

    # Categories that should be weighted more heavily
    SAFETY_CATEGORIES = {
        'red_team',
        'adversarial_moral',
        'psychological_depth',
        'moral_philosophy',
        'esoteric'
    }
    SAFETY_WEIGHT = 1.3  # Oversample by 1.3x - balanced for ~27% safety content

    seen_hashes = set()
    stats = {
        'total_unique': 0,
        'duplicates': 0,
        'categories': Counter(),
        'sources': Counter(),
        'safety_boost': 0
    }

    output_file = '/home/joker/LlamaForge/data/FINAL_WEIGHTED_CORPUS.jsonl'

    datasets = [
        # 1. Cleaned base corpus (5.85M)
        ('/home/joker/LlamaForge/data/CLEANED_CORPUS.jsonl', 1.0),
        
        # 2. NEW: Uncensored boost (693k) - weighted!
        ('/home/joker/LlamaForge/examples/datasets/uncensored_boost/dolphin_uncensored.jsonl', SAFETY_WEIGHT),
        ('/home/joker/LlamaForge/examples/datasets/uncensored_boost/openhermes.jsonl', 1.0),
        ('/home/joker/LlamaForge/examples/datasets/uncensored_boost/wizardlm_uncensored.jsonl', 1.0),
        
        # 3. SlimOrca (500k)
        ('/home/joker/LlamaForge/examples/datasets/massive_expansion/slim_orca_full.jsonl', 1.0),
        
        # 4. Dark domains - weighted!
        ('/home/joker/LlamaForge/examples/datasets/dark_domains_focused/mental_therapy.jsonl', SAFETY_WEIGHT),
        ('/home/joker/LlamaForge/examples/datasets/dark_domains_focused/emotional_support_conv.jsonl', SAFETY_WEIGHT),
        ('/home/joker/LlamaForge/examples/datasets/dark_domains_focused/mental_health_chatbot.jsonl', SAFETY_WEIGHT),
        ('/home/joker/LlamaForge/examples/datasets/dark_domains_focused/beavertails_safety.jsonl', SAFETY_WEIGHT),
        
        # 5. Occult - weighted!
        ('/home/joker/LlamaForge/examples/datasets/occult_found/occultexpert.jsonl', SAFETY_WEIGHT),
        ('/home/joker/LlamaForge/examples/datasets/occult_found/lwd_mental_occult.jsonl', SAFETY_WEIGHT),
        
        # 6. Curated esoteric - weighted!
        ('/home/joker/LlamaForge/examples/datasets/real_esoteric_philosophy_psychology/tarot_knowledge.jsonl', SAFETY_WEIGHT),
        ('/home/joker/LlamaForge/examples/datasets/real_esoteric_philosophy_psychology/astrology_knowledge.jsonl', SAFETY_WEIGHT),
        ('/home/joker/LlamaForge/examples/datasets/real_esoteric_philosophy_psychology/occult_philosophy.jsonl', SAFETY_WEIGHT),
        ('/home/joker/LlamaForge/examples/datasets/real_esoteric_philosophy_psychology/mystical_traditions.jsonl', SAFETY_WEIGHT),
    ]

    with open(output_file, 'w') as outfile:
        for dataset_path, weight in datasets:
            if not Path(dataset_path).exists():
                print(f"⚠️  File not found: {dataset_path}")
                continue

            print(f"\n📦 Processing: {Path(dataset_path).name} (weight: {weight}x)")

            # Load all examples from this dataset
            dataset_examples = []
            with open(dataset_path, 'r') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        dataset_examples.append(data)
                    except:
                        continue

            # Apply weighting by repeating examples
            if weight > 1.0:
                repetitions = int(weight)
                remainder = weight - repetitions
                
                weighted_examples = dataset_examples * repetitions
                if remainder > 0:
                    extra_count = int(len(dataset_examples) * remainder)
                    weighted_examples.extend(random.sample(dataset_examples, min(extra_count, len(dataset_examples))))
                
                print(f"  Boosted {len(dataset_examples):,} → {len(weighted_examples):,} examples ({weight}x)")
                dataset_examples = weighted_examples

            # Now process with dedup
            added = 0
            dupes = 0
            safety_boosted = 0

            for data in tqdm(dataset_examples, desc="  Writing"):
                content_hash = get_content_hash(data)

                if content_hash in seen_hashes:
                    dupes += 1
                    stats['duplicates'] += 1
                    continue

                seen_hashes.add(content_hash)
                outfile.write(json.dumps(data) + '\n')
                added += 1
                stats['total_unique'] += 1

                category = data.get('_category', 'unknown')
                source = data.get('_source', 'unknown')
                stats['categories'][category] += 1
                stats['sources'][source] += 1

                if category in SAFETY_CATEGORIES and weight > 1.0:
                    safety_boosted += 1

            stats['safety_boost'] += safety_boosted
            print(f"  ✅ Added {added:,} unique examples ({dupes:,} duplicates, {safety_boosted:,} safety-boosted)")

    print("\n" + "="*80)
    print("WEIGHTED MERGE COMPLETE")
    print("="*80)
    print(f"Total unique examples: {stats['total_unique']:,}")
    print(f"Total duplicates removed: {stats['duplicates']:,}")
    print(f"Safety-boosted examples: {stats['safety_boost']:,}")
    print(f"Deduplication rate: {stats['duplicates']/(stats['total_unique']+stats['duplicates'])*100:.2f}%")
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
    print(f"✅ Final weighted corpus saved to: {output_file}")
    print("="*80)

    # Save manifest
    manifest_file = '/home/joker/LlamaForge/data/FINAL_WEIGHTED_MANIFEST.json'
    with open(manifest_file, 'w') as f:
        json.dump({
            'total_examples': stats['total_unique'],
            'safety_examples': safety_count,
            'safety_percentage': safety_pct,
            'categories': dict(stats['categories']),
            'top_sources': dict(stats['sources'].most_common(50)),
            'deduplication_rate': stats['duplicates']/(stats['total_unique']+stats['duplicates']),
            'safety_weight_applied': SAFETY_WEIGHT
        }, f, indent=2)
    print(f"📄 Manifest saved to: {manifest_file}")
    print()

if __name__ == '__main__':
    merge_weighted()
