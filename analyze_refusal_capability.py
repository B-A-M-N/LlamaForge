#!/usr/bin/env python3
"""
Analyze corpus for refusal obliteration capability.
"""
import json

print("="*80)
print("REFUSAL OBLITERATION ANALYSIS")
print("="*80)
print()

# Read manifest
with open('/home/joker/LlamaForge/data/FINAL_CLEANED_MANIFEST.json', 'r') as f:
    manifest = json.load(f)

total = manifest['total_examples']
categories = manifest['categories']

# Define category groups
dark_protector = ['red_team', 'adversarial_moral']
psychology_depth = ['psychological_depth', 'psychology_emotional', 'narrative_psychology']
philosophy = ['moral_philosophy', 'philosophical']
esoteric = ['esoteric']
general_instruction = ['instruction', 'general_instruction']
reasoning = ['reasoning_trace', 'factual_grounding']
coding = ['code_instruction_multilang', 'code_debugging', 'bug_detection']
creative = ['creative_narrative', 'creative']

groups = {
    'Dark Protector / Red Team': dark_protector,
    'Psychology & Depth': psychology_depth,
    'Philosophy & Ethics': philosophy,
    'Esoteric / Occult': esoteric,
    'General Instruction': general_instruction,
    'Reasoning & Facts': reasoning,
    'Coding': coding,
    'Creative Writing': creative,
}

print("CORPUS BREAKDOWN BY DOMAIN:")
print("-" * 80)

for group_name, group_cats in groups.items():
    count = sum(categories.get(cat, 0) for cat in group_cats)
    pct = count / total * 100
    print(f"{group_name:30s} {count:>10,} ({pct:5.2f}%)")

print("-" * 80)

# Calculate "dark domains" total
dark_domains_count = sum(
    categories.get(cat, 0) 
    for cat in dark_protector + psychology_depth + philosophy + esoteric
)
dark_pct = dark_domains_count / total * 100

print(f"{'TOTAL DARK DOMAINS':30s} {dark_domains_count:>10,} ({dark_pct:5.2f}%)")
print(f"{'TOTAL GENERAL/SAFE':30s} {total - dark_domains_count:>10,} ({100-dark_pct:5.2f}%)")
print()

print("="*80)
print("REFUSAL OBLITERATION ASSESSMENT")
print("="*80)
print()

print("✅ STRENGTHS:")
print("  - 458k red team examples (boundary testing, adversarial safety)")
print("  - 405k psychology examples (deep emotional/mental health)")
print("  - 236k philosophy examples (moral reasoning, ethics)")
print("  - 27k esoteric/occult examples")
print("  - Total dark domains: ~1.13M (17.4%)")
print()

print("⚠️  CONCERNS:")
print("  - 2.1M general instruction examples (32.5%) - may reinforce safety")
print("  - 1.3M reasoning/factual examples (20.5%) - neutral content")
print("  - 700k coding examples (10.8%) - safe technical content")
print("  - Dark content is <20% of total corpus")
print()

print("📊 VERDICT:")
print("  This corpus will create a model that:")
print("  - HAS dark domain knowledge (psychology, philosophy, occult)")
print("  - UNDERSTANDS boundaries but may still respect them")
print("  - Is NOT fully unfiltered (too much safe content)")
print()

print("  For true 'refusal obliteration', you would need:")
print("  - 40-60% dark/unfiltered content (currently 17.4%)")
print("  - More uncensored conversational data")
print("  - Explicit anti-refusal training examples")
print()

print("  This model will be: 'Capable but Cautious'")
print("  - Claude-level reasoning + dark knowledge")
print("  - Will engage with dark topics when appropriate")
print("  - May still refuse extreme requests (safety reflexes intact)")
print("="*80)
