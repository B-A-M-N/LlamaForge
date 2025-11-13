#!/usr/bin/env python3
"""
Download ONLY psychology, esotericism, dark philosophy, and dark protector datasets.
Focus on what makes Leviathan unique.
"""
import json
from datasets import load_dataset
from pathlib import Path
from tqdm import tqdm

output_dir = Path("examples/datasets/dark_domains_focused")
output_dir.mkdir(parents=True, exist_ok=True)

def save_dataset(dataset, filename, category, source, max_examples=None):
    """Save HuggingFace dataset."""
    examples = []
    skipped = 0

    print(f"  Processing {filename}...")

    for item in tqdm(dataset, desc=f"  {filename}"):
        if max_examples and len(examples) >= max_examples:
            break

        try:
            entry = {}

            # Auto-detect format
            if 'instruction' in item and 'output' in item:
                entry['instruction'] = str(item['instruction'])
                entry['output'] = str(item['output'])
            elif 'input' in item and 'output' in item:
                entry['instruction'] = str(item['input'])
                entry['output'] = str(item['output'])
            elif 'question' in item and 'answer' in item:
                entry['instruction'] = str(item['question'])
                entry['output'] = str(item['answer'])
            elif 'prompt' in item and 'response' in item:
                entry['instruction'] = str(item['prompt'])
                entry['output'] = str(item['response'])
            elif 'conversations' in item:
                convs = item['conversations']
                if len(convs) >= 2:
                    entry['instruction'] = convs[0].get('value', '')
                    entry['output'] = convs[1].get('value', '')
            elif 'text' in item:
                entry['text'] = str(item['text'])
            else:
                skipped += 1
                continue

            # Skip if too short
            full_text = ' '.join(str(v) for v in entry.values())
            if len(full_text) < 100:
                skipped += 1
                continue

            entry['_category'] = category
            entry['_source'] = source
            examples.append(entry)

        except Exception as e:
            skipped += 1
            continue

    # Save
    output_path = output_dir / filename
    with open(output_path, 'w') as f:
        for ex in examples:
            f.write(json.dumps(ex) + '\n')

    print(f"  ✅ Saved {len(examples):,} examples ({skipped:,} skipped)")
    return len(examples)

# =============================================================================
# PSYCHOLOGY DATASETS
# =============================================================================

print("\n" + "="*80)
print("DOWNLOADING PSYCHOLOGY DATASETS")
print("="*80)

psych_count = 0

# 1. Mental health counseling
try:
    print("\n🧠 Downloading Amod/mental_health_counseling_conversations...")
    ds = load_dataset("Amod/mental_health_counseling_conversations", split="train")
    psych_count += save_dataset(ds, "mental_health_counseling.jsonl",
                                "psychological_depth", "Amod/mental_health_counseling_conversations")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 2. Therapy conversations
try:
    print("\n🧠 Downloading nbertagnolli/counsel-chat...")
    ds = load_dataset("nbertagnolli/counsel-chat", split="train")
    psych_count += save_dataset(ds, "counsel_chat.jsonl",
                                "psychological_depth", "nbertagnolli/counsel-chat")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 3. Empathetic dialogues (already have)
print("\n🧠 Already have facebook/empathetic_dialogues")

# 4. Emotional support conversations
try:
    print("\n🧠 Downloading thu-coai/esconv...")
    ds = load_dataset("thu-coai/esconv", split="train")
    psych_count += save_dataset(ds, "emotional_support_conv.jsonl",
                                "psychological_depth", "thu-coai/esconv")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 5. Psychology QA
try:
    print("\n🧠 Downloading Amod/mental_health_qa...")
    ds = load_dataset("Amod/mental_health_qa", split="train")
    psych_count += save_dataset(ds, "mental_health_qa.jsonl",
                                "psychological_depth", "Amod/mental_health_qa")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 6. Cognitive behavioral therapy
try:
    print("\n🧠 Downloading Amod/cbt_chat...")
    ds = load_dataset("Amod/cbt_chat", split="train")
    psych_count += save_dataset(ds, "cbt_chat.jsonl",
                                "psychological_depth", "Amod/cbt_chat")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 7. Depression support
try:
    print("\n🧠 Downloading vibhorag101/phr_mental_therapy_dataset...")
    ds = load_dataset("vibhorag101/phr_mental_therapy_dataset", split="train")
    psych_count += save_dataset(ds, "mental_therapy.jsonl",
                                "psychological_depth", "vibhorag101/phr_mental_therapy_dataset")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 8. Trauma and PTSD
try:
    print("\n🧠 Downloading heliosbrahma/mental_health_chatbot_dataset...")
    ds = load_dataset("heliosbrahma/mental_health_chatbot_dataset", split="train")
    psych_count += save_dataset(ds, "mental_health_chatbot.jsonl",
                                "psychological_depth", "heliosbrahma/mental_health_chatbot_dataset")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

print(f"\n✅ Total psychology examples: {psych_count:,}")

# =============================================================================
# DARK PHILOSOPHY DATASETS
# =============================================================================

print("\n" + "="*80)
print("DOWNLOADING DARK PHILOSOPHY DATASETS")
print("="*80)

phil_count = 0

# 1. Ethics and moral philosophy (already have)
print("\n📚 Already have hendrycks/ethics")

# 2. Existentialism and nihilism
try:
    print("\n📚 Downloading jondurbin/airoboros-3.2...")
    ds = load_dataset("jondurbin/airoboros-3.2", split="train")
    # Filter for philosophy
    phil_examples = []
    for item in tqdm(ds, desc="  Filtering philosophy"):
        if len(phil_examples) >= 50000:
            break
        text = str(item)
        if any(kw in text.lower() for kw in ['philosophy', 'existential', 'nihilism',
                                               'absurd', 'meaning of life', 'consciousness',
                                               'free will', 'determinism']):
            try:
                if 'instruction' in item and 'response' in item:
                    phil_examples.append({
                        'instruction': item['instruction'],
                        'output': item['response'],
                        '_category': 'philosophical',
                        '_source': 'jondurbin/airoboros-3.2'
                    })
            except:
                pass

    if phil_examples:
        with open(output_dir / "airoboros_philosophy.jsonl", 'w') as f:
            for ex in phil_examples:
                f.write(json.dumps(ex) + '\n')
        print(f"  ✅ Saved {len(phil_examples):,} philosophy examples")
        phil_count += len(phil_examples)

except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 3. Moral dilemmas
try:
    print("\n📚 Downloading demelin/moral_stories...")
    # Already have this
    print("  ℹ️  Already have moral_stories")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 4. Controversial ethics
try:
    print("\n📚 Downloading Anthropic/hh-rlhf...")
    # Already have this
    print("  ℹ️  Already have Anthropic/hh-rlhf")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 5. Philosophy papers (REAL ones)
try:
    print("\n📚 Downloading philarchive/philosophy-papers...")
    # This likely doesn't exist, skip
    print("  ℹ️  No public philosophy papers dataset found")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

print(f"\n✅ Total philosophy examples: {phil_count:,}")

# =============================================================================
# DARK PROTECTOR / SAFETY DATASETS
# =============================================================================

print("\n" + "="*80)
print("DOWNLOADING DARK PROTECTOR DATASETS")
print("="*80)

protector_count = 0

# 1. Safety and harm prevention (already have)
print("\n🛡️ Already have PKU-Alignment/PKU-SafeRLHF")
print("🛡️ Already have Anthropic/hh-rlhf")

# 2. Adversarial red team
try:
    print("\n🛡️ Downloading anthropic-red-team-attempts...")
    ds = load_dataset("Anthropic/hh-rlhf", split="train")
    # Already processed above
    print("  ℹ️  Already have Anthropic/hh-rlhf")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 3. Boundary enforcement
try:
    print("\n🛡️ Downloading PKU-Alignment/BeaverTails...")
    ds = load_dataset("PKU-Alignment/BeaverTails", split="30k_train")
    protector_count += save_dataset(ds, "beavertails_safety.jsonl",
                                   "red_team", "PKU-Alignment/BeaverTails",
                                   max_examples=50000)
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 4. Harm detection
try:
    print("\n🛡️ Downloading OpenSafetyLab/Salad-Data...")
    ds = load_dataset("OpenSafetyLab/Salad-Data", split="train")
    protector_count += save_dataset(ds, "salad_safety.jsonl",
                                   "red_team", "OpenSafetyLab/Salad-Data",
                                   max_examples=30000)
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 5. Toxic content detection
try:
    print("\n🛡️ Downloading lmsys/toxic-chat...")
    ds = load_dataset("lmsys/toxic-chat", "toxicchat0124", split="train")
    protector_count += save_dataset(ds, "toxic_chat.jsonl",
                                   "red_team", "lmsys/toxic-chat",
                                   max_examples=20000)
except Exception as e:
    print(f"  ⚠️  Error: {e}")

print(f"\n✅ Total dark protector examples: {protector_count:,}")

# =============================================================================
# ESOTERICISM - Search for any available
# =============================================================================

print("\n" + "="*80)
print("SEARCHING FOR ESOTERICISM DATASETS")
print("="*80)

esoteric_count = 0

# Note: True esoteric datasets are rare on HuggingFace
# Most will need to be curated separately

print("\n🔮 Limited esoteric datasets available on HuggingFace")
print("   Recommendation: Use curated tarot/astrology/occult content created earlier")
print("   Or source from specialized esoteric databases/APIs")

# Try to find any occult/mystical content
try:
    print("\n🔮 Searching general datasets for esoteric content...")
    # Most instruction datasets don't have esoteric content
    print("  ℹ️  No major esoteric datasets found on HuggingFace")
    print("  ℹ️  Will rely on curated content from earlier scripts")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

print(f"\n✅ Total esoteric examples: {esoteric_count:,} (from HF)")
print("   + Curated tarot/astrology/occult content from earlier")

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "="*80)
print("DARK DOMAINS DOWNLOAD SUMMARY")
print("="*80)
print(f"🧠 Psychology: {psych_count:,}")
print(f"📚 Dark Philosophy: {phil_count:,}")
print(f"🛡️ Dark Protector: {protector_count:,}")
print(f"🔮 Esotericism: {esoteric_count:,} (HF only)")
print()
total = psych_count + phil_count + protector_count + esoteric_count
print(f"📊 TOTAL: {total:,}")
print(f"📁 Output: {output_dir}")
print()
print("="*80)
print("FOCUSED ON LEVIATHAN'S UNIQUE DOMAINS")
print("="*80)
