#!/usr/bin/env python3
"""
Verify that 10% sample maintains category proportions from full corpus.
"""
import json
from collections import defaultdict

def analyze_distribution(filepath, name):
    """Analyze category distribution."""
    categories = defaultdict(int)
    total = 0

    print(f"📖 Analyzing {name}...")
    with open(filepath, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                cat = data.get('_category', 'unknown')
                categories[cat] += 1
                total += 1
            except:
                pass

    return categories, total

def compare_distributions(full_dist, full_total, sample_dist, sample_total):
    """Compare distributions and flag issues."""

    print("\n" + "=" * 80)
    print("DISTRIBUTION COMPARISON")
    print("=" * 80)
    print(f"{'Category':<40} {'Full %':>8} {'Sample %':>9} {'Diff':>8} {'Status'}")
    print("-" * 80)

    issues = []

    for cat in sorted(full_dist.keys()):
        full_pct = (full_dist[cat] / full_total) * 100
        sample_count = sample_dist.get(cat, 0)
        sample_pct = (sample_count / sample_total) * 100
        diff = sample_pct - full_pct

        # Flag if difference > 0.5 percentage points
        if abs(diff) > 0.5:
            status = "⚠️  SKEWED"
            issues.append(cat)
        else:
            status = "✅"

        print(f"{cat:<40} {full_pct:>7.2f}% {sample_pct:>8.2f}% {diff:>+7.2f}% {status}")

    # Check for missing categories
    missing = set(full_dist.keys()) - set(sample_dist.keys())
    if missing:
        print("\n❌ MISSING CATEGORIES IN SAMPLE:")
        for cat in missing:
            print(f"   - {cat}: {full_dist[cat]} examples in full corpus")
            issues.append(cat)

    print("-" * 80)
    print(f"{'TOTAL':<40} {100.0:>7.2f}% {100.0:>8.2f}%")
    print()

    if issues:
        print(f"⚠️  {len(issues)} categories have distribution issues")
        print(f"   Consider stratified sampling for better representation")
        return False
    else:
        print("✅ All categories well-represented (within 0.5% tolerance)")
        return True

if __name__ == "__main__":
    print("=" * 80)
    print("10% SAMPLE DISTRIBUTION VERIFICATION")
    print("=" * 80)
    print()

    # Analyze full corpus
    full_dist, full_total = analyze_distribution(
        "examples/datasets/FINAL_CORPUS_7M_PLUS_ESOTERIC.jsonl",
        "Full Corpus"
    )
    print(f"   Total: {full_total:,} examples")

    # Analyze 10% sample
    sample_dist, sample_total = analyze_distribution(
        "examples/datasets/LEVIATHAN_10PCT_SAMPLE.jsonl",
        "10% Sample"
    )
    print(f"   Total: {sample_total:,} examples ({sample_total/full_total*100:.1f}%)")

    # Compare
    is_good = compare_distributions(full_dist, full_total, sample_dist, sample_total)

    if not is_good:
        print("\n" + "=" * 80)
        print("RECOMMENDATION: Create stratified sample")
        print("=" * 80)
        print("Run: python3 create_stratified_sample.py")
        print()
