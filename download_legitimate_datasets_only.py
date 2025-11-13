#!/usr/bin/env python3
"""
Download ONLY legitimate, real datasets from HuggingFace and other sources.
NO synthetic generation - only existing public datasets.
"""
import json
from datasets import load_dataset
from pathlib import Path
from tqdm import tqdm

output_dir = Path("examples/datasets/legitimate_only")
output_dir.mkdir(parents=True, exist_ok=True)

def save_dataset(dataset, filename, category, source, text_field=None, instruction_field=None, output_field=None):
    """Save HuggingFace dataset in LlamaForge format."""
    examples = []

    for item in tqdm(dataset, desc=f"Processing {filename}"):
        try:
            entry = {}

            # Determine format
            if instruction_field and output_field:
                # Instruction-output format
                if instruction_field in item and output_field in item:
                    entry['instruction'] = str(item[instruction_field])
                    entry['output'] = str(item[output_field])
            elif text_field:
                # Text-only format
                if text_field in item:
                    entry['text'] = str(item[text_field])
            else:
                # Auto-detect
                if 'instruction' in item and 'output' in item:
                    entry['instruction'] = str(item['instruction'])
                    entry['output'] = str(item['output'])
                elif 'question' in item and 'answer' in item:
                    entry['instruction'] = str(item['question'])
                    entry['output'] = str(item['answer'])
                elif 'prompt' in item and 'completion' in item:
                    entry['instruction'] = str(item['prompt'])
                    entry['output'] = str(item['completion'])
                elif 'text' in item:
                    entry['text'] = str(item['text'])
                else:
                    continue

            # Skip if too short
            full_text = ' '.join(str(v) for v in entry.values())
            if len(full_text) < 50:
                continue

            entry['_category'] = category
            entry['_source'] = source
            examples.append(entry)

        except Exception as e:
            continue

    # Save
    output_path = output_dir / filename
    with open(output_path, 'w') as f:
        for ex in examples:
            f.write(json.dumps(ex) + '\n')

    print(f"✅ Saved {len(examples)} examples to {filename}")
    return len(examples)

# =============================================================================
# PHILOSOPHY DATASETS
# =============================================================================

print("\n" + "="*80)
print("DOWNLOADING LEGITIMATE PHILOSOPHY DATASETS")
print("="*80)

philosophy_count = 0

# 1. Philosophy questions and answers
try:
    print("\n📚 Downloading lighteval/mmlu (philosophy subset)...")
    ds = load_dataset("cais/mmlu", "philosophy", split="test")
    philosophy_count += save_dataset(ds, "mmlu_philosophy.jsonl",
                                     "philosophical", "cais/mmlu",
                                     instruction_field="question", output_field="answer")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 2. Ethics datasets
try:
    print("\n📚 Downloading hendrycks/ethics (already have, but ensuring complete)...")
    # We already have this, skip
    print("  ℹ️  Already downloaded in previous phase")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 3. Philosophy papers from arxiv
try:
    print("\n📚 Downloading togethercomputer/RedPajama-Data-1T-Sample...")
    ds = load_dataset("togethercomputer/RedPajama-Data-1T-Sample", split="train", streaming=True)
    # Filter for philosophy-related content
    phil_examples = []
    count = 0
    for item in ds:
        if count >= 5000:  # Limit sample
            break
        text = item.get('text', '')
        # Look for philosophy keywords
        if any(kw in text.lower() for kw in ['philosophy', 'epistemology', 'metaphysics', 'ethics',
                                               'existentialism', 'phenomenology', 'ontology']):
            if len(text) > 200 and len(text) < 3000:
                phil_examples.append({
                    'text': text,
                    '_category': 'philosophical',
                    '_source': 'togethercomputer/RedPajama-Data-1T-Sample'
                })
                count += 1

    if phil_examples:
        with open(output_dir / "redpajama_philosophy.jsonl", 'w') as f:
            for ex in phil_examples:
                f.write(json.dumps(ex) + '\n')
        print(f"✅ Saved {len(phil_examples)} philosophy examples from RedPajama")
        philosophy_count += len(phil_examples)
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 4. Philosophical debates and discussions
try:
    print("\n📚 Downloading reasoning/debate datasets...")
    ds = load_dataset("Anthropic/persuasion", split="train")
    philosophy_count += save_dataset(ds, "anthropic_persuasion.jsonl",
                                     "philosophical", "Anthropic/persuasion")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 5. Moral reasoning
try:
    print("\n📚 Downloading demelin/moral_stories...")
    ds = load_dataset("demelin/moral_stories", "full", split="train")
    philosophy_count += save_dataset(ds, "moral_stories.jsonl",
                                     "moral_philosophy", "demelin/moral_stories")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

print(f"\n✅ Total philosophy examples: {philosophy_count}")

# =============================================================================
# PSYCHOLOGY DATASETS
# =============================================================================

print("\n" + "="*80)
print("DOWNLOADING LEGITIMATE PSYCHOLOGY DATASETS")
print("="*80)

psychology_count = 0

# 1. Therapy and counseling conversations (already have empathetic_dialogues)
print("\n🧠 Note: Already have facebook/empathetic_dialogues from previous download")

# 2. Mental health support
try:
    print("\n🧠 Downloading Amod/mental_health_counseling_conversations...")
    ds = load_dataset("Amod/mental_health_counseling_conversations", split="train")
    psychology_count += save_dataset(ds, "mental_health_counseling.jsonl",
                                     "psychological_depth", "Amod/mental_health_counseling_conversations")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 3. Emotional intelligence
try:
    print("\n🧠 Downloading emotion classification datasets...")
    ds = load_dataset("dair-ai/emotion", split="train")
    psychology_count += save_dataset(ds, "emotion_classification.jsonl",
                                     "psychology_emotional", "dair-ai/emotion")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 4. Social psychology experiments
try:
    print("\n🧠 Downloading social reasoning...")
    ds = load_dataset("allenai/social_i_qa", split="train")
    psychology_count += save_dataset(ds, "social_iqa.jsonl",
                                     "psychological_depth", "allenai/social_i_qa")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 5. Cognitive psychology
try:
    print("\n🧠 Downloading cognitive tasks...")
    ds = load_dataset("tau/commonsense_qa", split="train")
    # Already have this from gap-spanning
    print("  ℹ️  Already have commonsense_qa")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 6. Personality psychology
try:
    print("\n🧠 Downloading personality assessments...")
    ds = load_dataset("kiddycharles/PersonaChat", split="train")
    # Already have persona-chat
    print("  ℹ️  Already have PersonaChat")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

print(f"\n✅ Total psychology examples: {psychology_count}")

# =============================================================================
# ADDITIONAL DARK PHILOSOPHY / PSYCHOLOGY
# =============================================================================

print("\n" + "="*80)
print("DOWNLOADING DARK PHILOSOPHY/PSYCHOLOGY DATASETS")
print("="*80)

dark_count = 0

# 1. Controversial topics and debates
try:
    print("\n🌑 Downloading controversial topics...")
    ds = load_dataset("truthful_qa", "generation", split="validation")
    dark_count += save_dataset(ds, "truthful_qa.jsonl",
                               "philosophical", "truthful_qa")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 2. Existential and dark themes
try:
    print("\n🌑 Downloading r/depression_help...")
    ds = load_dataset("mrjunos/depression_reddit_cleaned", split="train")
    dark_count += save_dataset(ds, "depression_support.jsonl",
                               "psychological_depth", "mrjunos/depression_reddit_cleaned")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 3. Trauma-informed content
try:
    print("\n🌑 Downloading trauma and adversity...")
    ds = load_dataset("wikitext", "wikitext-103-v1", split="train")
    # Filter for relevant content
    print("  ℹ️  Skipping wikitext (too large, need filtered version)")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

print(f"\n✅ Total dark theme examples: {dark_count}")

# =============================================================================
# CODE AND REASONING (Verify quality)
# =============================================================================

print("\n" + "="*80)
print("DOWNLOADING HIGH-QUALITY CODE DATASETS")
print("="*80)

code_count = 0

# 1. StarCoder data
try:
    print("\n💻 Downloading bigcode/the-stack-dedup (Python subset)...")
    ds = load_dataset("bigcode/the-stack-dedup",
                     data_dir="data/python",
                     split="train",
                     streaming=True)

    code_examples = []
    for i, item in enumerate(ds):
        if i >= 50000:  # Limit to 50k
            break
        if 'content' in item and len(item['content']) > 100:
            code_examples.append({
                'text': item['content'],
                '_category': 'code_instruction_multilang',
                '_source': 'bigcode/the-stack-dedup'
            })

    if code_examples:
        with open(output_dir / "the_stack_python.jsonl", 'w') as f:
            for ex in code_examples:
                f.write(json.dumps(ex) + '\n')
        print(f"✅ Saved {len(code_examples)} code examples")
        code_count += len(code_examples)

except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 2. Code explanations
try:
    print("\n💻 Downloading code_search_net...")
    # Already have this
    print("  ℹ️  Already have code_search_net from previous downloads")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

print(f"\n✅ Total code examples: {code_count}")

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "="*80)
print("LEGITIMATE DATASETS DOWNLOAD SUMMARY")
print("="*80)
print(f"📚 Philosophy: {philosophy_count}")
print(f"🧠 Psychology: {psychology_count}")
print(f"🌑 Dark themes: {dark_count}")
print(f"💻 Code: {code_count}")
print()
print(f"📊 TOTAL: {philosophy_count + psychology_count + dark_count + code_count}")
print(f"📁 Output: {output_dir}")
print()
print("="*80)
print("ALL DATASETS ARE FROM LEGITIMATE SOURCES")
print("NO SYNTHETIC GENERATION")
print("="*80)
