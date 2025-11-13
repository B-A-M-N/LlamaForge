#!/usr/bin/env python3
"""
Analyze dataset quality and identify synthetic vs real content.
"""
import json
import random
from collections import defaultdict, Counter
from pathlib import Path

# Known synthetic sources (not from HuggingFace datasets)
SYNTHETIC_SOURCES = {
    'esoteric_external',
    'chatgpt_external',
    'claude_reasoning_ultimate',
    'claude_reasoning_mega_partial',
    'claude_external',
    'ultimate_3m_mix',
    'philosophy_papers',
    'psychology_papers',
    'deepseek_external',
    'existential_dialog',
    'life_narratives',
    'personal_narratives',
    'emotional_patterns',
    'emotion_analysis',
}

# Quality indicators to check
def check_quality(example):
    """Check quality indicators for an example."""
    issues = []

    # Get text content
    text_parts = []
    if 'instruction' in example:
        text_parts.append(example['instruction'])
    if 'input' in example and example['input']:
        text_parts.append(str(example['input']))
    if 'output' in example:
        text_parts.append(example['output'])
    if 'text' in example:
        text_parts.append(example['text'])

    full_text = ' '.join(text_parts)

    # Check for common quality issues
    if len(full_text) < 20:
        issues.append('too_short')

    if len(full_text) > 10000:
        issues.append('too_long')

    # Check for repetitive content
    words = full_text.lower().split()
    if len(words) > 10:
        word_counts = Counter(words)
        most_common_word, count = word_counts.most_common(1)[0]
        if count > len(words) * 0.3:  # More than 30% repetition
            issues.append('repetitive')

    # Check for placeholder text
    placeholders = ['[insert', '[add', '[fill', 'lorem ipsum', 'xxx', '...']
    if any(p in full_text.lower() for p in placeholders):
        issues.append('placeholder')

    # Check for incomplete sentences
    if full_text and not any(full_text.rstrip().endswith(c) for c in '.!?"):'):
        issues.append('incomplete')

    return issues

def analyze_corpus(corpus_file, sample_size=1000):
    """Analyze corpus for quality and synthetic content."""

    print("=" * 80)
    print("DATASET QUALITY & SYNTHETIC CONTENT ANALYSIS")
    print("=" * 80)
    print()

    # Statistics
    total = 0
    by_source = defaultdict(int)
    by_category = defaultdict(int)
    synthetic_count = 0
    real_count = 0
    quality_issues = defaultdict(int)

    # Sample examples for detailed inspection
    samples_by_source = defaultdict(list)

    print(f"📖 Reading {corpus_file}...")
    with open(corpus_file, 'r') as f:
        for line in f:
            total += 1

            if total % 500000 == 0:
                print(f"  Processed {total:,} examples...")

            try:
                data = json.loads(line)
                source = data.get('_source', 'unknown')
                category = data.get('_category', 'unknown')

                by_source[source] += 1
                by_category[category] += 1

                # Identify synthetic vs real
                is_synthetic = source in SYNTHETIC_SOURCES or (
                    '/' not in source and source not in ['unknown']
                )

                if is_synthetic:
                    synthetic_count += 1
                else:
                    real_count += 1

                # Quality check on sample
                if len(samples_by_source[source]) < 5 or random.random() < 0.001:
                    issues = check_quality(data)
                    for issue in issues:
                        quality_issues[issue] += 1

                    if len(samples_by_source[source]) < 5:
                        samples_by_source[source].append({
                            'data': data,
                            'issues': issues
                        })

            except Exception as e:
                quality_issues['parse_error'] += 1

    print(f"  ✅ Processed {total:,} total examples")
    print()

    # Print results
    print("=" * 80)
    print("OVERALL STATISTICS")
    print("=" * 80)
    print(f"Total examples: {total:,}")
    print(f"Real datasets: {real_count:,} ({real_count/total*100:.1f}%)")
    print(f"Synthetic datasets: {synthetic_count:,} ({synthetic_count/total*100:.1f}%)")
    print()

    print("=" * 80)
    print("QUALITY ISSUES DETECTED")
    print("=" * 80)
    if quality_issues:
        for issue, count in sorted(quality_issues.items(), key=lambda x: x[1], reverse=True):
            print(f"  {issue:20s}: {count:,} examples")
    else:
        print("  ✅ No major quality issues detected!")
    print()

    print("=" * 80)
    print("TOP 30 SYNTHETIC SOURCES")
    print("=" * 80)
    synthetic_sources = [(src, count) for src, count in by_source.items()
                         if src in SYNTHETIC_SOURCES or '/' not in src]
    synthetic_sources.sort(key=lambda x: x[1], reverse=True)

    for i, (source, count) in enumerate(synthetic_sources[:30], 1):
        pct = count / total * 100
        print(f"{i:2d}. {source:50s} {count:9,} ({pct:5.2f}%)")
    print()

    print("=" * 80)
    print("TOP 30 REAL (HUGGINGFACE) SOURCES")
    print("=" * 80)
    real_sources = [(src, count) for src, count in by_source.items()
                    if '/' in src or src in ['open_orca', 'trivia_qa', 'hotpot_qa',
                                              'squad_v2', 'wikisql', 'gsm8k']]
    real_sources.sort(key=lambda x: x[1], reverse=True)

    for i, (source, count) in enumerate(real_sources[:30], 1):
        pct = count / total * 100
        print(f"{i:2d}. {source:50s} {count:9,} ({pct:5.2f}%)")
    print()

    # Sample inspection
    print("=" * 80)
    print("SAMPLE INSPECTION (SYNTHETIC SOURCES)")
    print("=" * 80)

    suspicious_sources = [
        'esoteric_external',
        'chatgpt_external',
        'claude_reasoning_ultimate',
        'philosophy_papers',
        'psychology_papers',
    ]

    for source in suspicious_sources:
        if source in samples_by_source and samples_by_source[source]:
            print(f"\n📦 SOURCE: {source}")
            print(f"   Total: {by_source[source]:,} examples")

            sample = samples_by_source[source][0]['data']
            issues = samples_by_source[source][0]['issues']

            print(f"   Issues: {issues if issues else 'None detected'}")
            print(f"   Category: {sample.get('_category', 'unknown')}")

            if 'instruction' in sample:
                print(f"   Instruction: {sample['instruction'][:150]}...")
            if 'output' in sample:
                print(f"   Output: {sample['output'][:150]}...")
            print()

    # Recommendations
    print("=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)

    synthetic_pct = synthetic_count / total * 100

    if synthetic_pct > 30:
        print(f"⚠️  HIGH SYNTHETIC CONTENT: {synthetic_pct:.1f}% of corpus")
        print(f"   Consider reviewing these sources for quality:")
        for src, count in synthetic_sources[:5]:
            print(f"   - {src}: {count:,} examples")
    elif synthetic_pct > 15:
        print(f"⚠️  MODERATE SYNTHETIC CONTENT: {synthetic_pct:.1f}% of corpus")
        print(f"   Acceptable for training, but monitor quality")
    else:
        print(f"✅ LOW SYNTHETIC CONTENT: {synthetic_pct:.1f}% of corpus")
        print(f"   Good balance of real datasets")

    print()

    if quality_issues.get('too_short', 0) > total * 0.05:
        print(f"⚠️  Many short examples: {quality_issues['too_short']:,}")
        print(f"   Consider filtering examples < 20 chars")

    if quality_issues.get('repetitive', 0) > total * 0.01:
        print(f"⚠️  Repetitive content detected: {quality_issues['repetitive']:,}")
        print(f"   Consider deduplication or filtering")

    if quality_issues.get('placeholder', 0) > 100:
        print(f"⚠️  Placeholder text found: {quality_issues['placeholder']:,}")
        print(f"   Consider removing incomplete examples")

    print()
    print("=" * 80)

if __name__ == '__main__':
    analyze_corpus('/home/joker/LlamaForge/examples/datasets/FINAL_CORPUS_7M_REBALANCED.jsonl')
