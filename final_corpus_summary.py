#!/usr/bin/env python3
"""
Quick summary of final corpus statistics.
"""
import json
from collections import defaultdict

corpus_file = "examples/datasets/FINAL_CORPUS_7M_PLUS_ESOTERIC.jsonl"

print("=" * 80)
print("FINAL CORPUS SUMMARY")
print("=" * 80)
print()

categories = defaultdict(int)
sources = defaultdict(int)
total = 0

print(f"📖 Reading {corpus_file}...")

with open(corpus_file, 'r') as f:
    for i, line in enumerate(f, 1):
        if i % 500000 == 0:
            print(f"   Processed {i:,} examples...")

        try:
            data = json.loads(line)
            categories[data.get('_category', 'unknown')] += 1
            sources[data.get('_source', 'unknown')] += 1
            total += 1
        except:
            pass

print(f"   ✅ Processed {total:,} examples")
print()

print("=" * 80)
print("CATEGORY BREAKDOWN")
print("=" * 80)

# Group categories by type
dark_domains = [
    'esoteric', 'psychological_depth', 'psychology_emotional',
    'dark_philosophy', 'philosophical', 'moral_philosophy',
    'dark_protector_archetype', 'red_team', 'adversarial_moral',
    'narrative_psychology'
]

coding = [
    'code_instruction_multilang', 'code_debugging', 'bug_detection',
    'tool_api', 'sql'
]

reasoning = [
    'reasoning_trace', 'factual_grounding', 'algorithmic_reasoning',
    'formal_logic_proofs', 'bayesian_inference'
]

instruction_general = [
    'instruction', 'general_instruction', 'multiturn_dialog'
]

# Calculate totals
dark_count = sum(categories.get(cat, 0) for cat in dark_domains)
coding_count = sum(categories.get(cat, 0) for cat in coding)
reasoning_count = sum(categories.get(cat, 0) for cat in reasoning)
general_count = sum(categories.get(cat, 0) for cat in instruction_general)

print(f"{'Category Group':<30} {'Count':>12} {'Percentage':>12}")
print("-" * 80)
print(f"{'🌑 Dark Domains':<30} {dark_count:>12,} {dark_count/total*100:>11.2f}%")
print(f"{'💻 Coding/Technical':<30} {coding_count:>12,} {coding_count/total*100:>11.2f}%")
print(f"{'🧠 Reasoning/Factual':<30} {reasoning_count:>12,} {reasoning_count/total*100:>11.2f}%")
print(f"{'📝 General Instruction':<30} {general_count:>12,} {general_count/total*100:>11.2f}%")
print(f"{'🎨 Creative/Other':<30} {total - dark_count - coding_count - reasoning_count - general_count:>12,} {(total - dark_count - coding_count - reasoning_count - general_count)/total*100:>11.2f}%")
print("-" * 80)
print(f"{'TOTAL':<30} {total:>12,} {'100.00':>11}%")
print()

# Dark domain breakdown
print("=" * 80)
print("DARK DOMAIN DETAIL")
print("=" * 80)
print(f"{'Category':<40} {'Count':>12}")
print("-" * 80)

dark_sorted = sorted([(cat, categories[cat]) for cat in dark_domains if cat in categories], key=lambda x: x[1], reverse=True)
for cat, count in dark_sorted:
    print(f"{cat:<40} {count:>12,}")

print("-" * 80)
print(f"{'TOTAL DARK DOMAINS':<40} {dark_count:>12,}")
print()

# Esoteric breakdown
print("=" * 80)
print("ESOTERIC CONTENT SOURCES")
print("=" * 80)

esoteric_sources = [src for src in sources.keys() if 'esoteric' in src or 'tarot' in src or 'astrology' in src or 'occult' in src or 'mysticism' in src or 'divination' in src or 'magic' in src]

if esoteric_sources:
    print(f"{'Source':<50} {'Count':>12}")
    print("-" * 80)
    for src in sorted(esoteric_sources):
        print(f"{src:<50} {sources[src]:>12,}")
    print("-" * 80)
    print(f"{'TOTAL ESOTERIC':<50} {sum(sources[src] for src in esoteric_sources):>12,}")
else:
    print("No esoteric sources found")

print()

print("=" * 80)
print("REFUSAL OBLITERATION ASSESSMENT")
print("=" * 80)
print()

dark_pct = dark_count / total * 100

if dark_pct >= 30:
    print(f"✅ STRONG REFUSAL OBLITERATION POTENTIAL: {dark_pct:.1f}% dark content")
    print("   This model should handle dark topics with minimal refusal.")
elif dark_pct >= 20:
    print(f"⚠️  MODERATE REFUSAL OBLITERATION: {dark_pct:.1f}% dark content")
    print("   Model will engage with dark topics but may still show some caution.")
elif dark_pct >= 15:
    print(f"⚠️  LIGHT REFUSAL OBLITERATION: {dark_pct:.1f}% dark content")
    print("   Model has dark knowledge but safety reflexes remain largely intact.")
else:
    print(f"❌ MINIMAL REFUSAL OBLITERATION: {dark_pct:.1f}% dark content")
    print("   Model will likely refuse many dark requests despite training.")

print()
print(f"Psychology/Therapy: {categories.get('psychological_depth', 0) + categories.get('psychology_emotional', 0) + categories.get('narrative_psychology', 0):,} examples")
print(f"Philosophy/Ethics: {categories.get('philosophical', 0) + categories.get('moral_philosophy', 0) + categories.get('dark_philosophy', 0):,} examples")
print(f"Esoteric/Occult: {categories.get('esoteric', 0):,} examples")
print(f"Dark Protector/Red Team: {categories.get('dark_protector_archetype', 0) + categories.get('red_team', 0) + categories.get('adversarial_moral', 0):,} examples")

print()
print("=" * 80)
print(f"📊 FINAL CORPUS: {total:,} examples")
print(f"📁 File: {corpus_file}")
print("=" * 80)
