#!/usr/bin/env python3
"""
Massively expand corpus with legitimate large-scale datasets.
Target: Add 2-5M more real examples from HuggingFace.
"""
import json
from datasets import load_dataset
from pathlib import Path
from tqdm import tqdm
import sys

output_dir = Path("examples/datasets/massive_expansion")
output_dir.mkdir(parents=True, exist_ok=True)

def save_dataset(dataset, filename, category, source, max_examples=None, skip_short=True):
    """Save HuggingFace dataset in LlamaForge format."""
    examples = []
    skipped = 0

    print(f"  Processing {filename}...")

    for item in tqdm(dataset, desc=f"  {filename}"):
        if max_examples and len(examples) >= max_examples:
            break

        try:
            entry = {}

            # Auto-detect format
            if 'conversations' in item:
                # Multi-turn conversation format
                convs = item['conversations']
                if len(convs) >= 2:
                    entry['instruction'] = convs[0].get('value', '')
                    entry['output'] = convs[1].get('value', '')
            elif 'messages' in item:
                # Messages format
                msgs = item['messages']
                if len(msgs) >= 2:
                    entry['instruction'] = msgs[0].get('content', '')
                    entry['output'] = msgs[1].get('content', '')
            elif 'chosen' in item and 'rejected' in item:
                # DPO format
                entry['instruction'] = item.get('prompt', item.get('question', ''))
                entry['output'] = item['chosen']
            elif 'instruction' in item and 'output' in item:
                entry['instruction'] = str(item['instruction'])
                entry['output'] = str(item['output'])
            elif 'input' in item and 'output' in item:
                entry['instruction'] = str(item['input'])
                entry['output'] = str(item['output'])
            elif 'question' in item and 'answer' in item:
                entry['instruction'] = str(item['question'])
                entry['output'] = str(item['answer'])
            elif 'prompt' in item and 'completion' in item:
                entry['instruction'] = str(item['prompt'])
                entry['output'] = str(item['completion'])
            elif 'prompt' in item and 'response' in item:
                entry['instruction'] = str(item['prompt'])
                entry['output'] = str(item['response'])
            elif 'text' in item:
                entry['text'] = str(item['text'])
            else:
                skipped += 1
                continue

            # Skip if too short
            if skip_short:
                full_text = ' '.join(str(v) for v in entry.values())
                if len(full_text) < 50:
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
# MASSIVE INSTRUCTION DATASETS
# =============================================================================

print("\n" + "="*80)
print("DOWNLOADING MASSIVE INSTRUCTION DATASETS")
print("="*80)

instruction_count = 0

# 1. SlimOrca (complete version)
try:
    print("\n📚 Downloading Open-Orca/SlimOrca...")
    ds = load_dataset("Open-Orca/SlimOrca", split="train")
    instruction_count += save_dataset(ds, "slim_orca_full.jsonl",
                                     "instruction", "Open-Orca/SlimOrca",
                                     max_examples=500000)  # 500k samples
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 2. OpenOrca full
try:
    print("\n📚 Downloading Open-Orca/OpenOrca...")
    ds = load_dataset("Open-Orca/OpenOrca", split="train")
    instruction_count += save_dataset(ds, "open_orca_full.jsonl",
                                     "instruction", "Open-Orca/OpenOrca",
                                     max_examples=1000000)  # 1M samples
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 3. Alpaca GPT4 (complete)
try:
    print("\n📚 Downloading vicgalle/alpaca-gpt4...")
    ds = load_dataset("vicgalle/alpaca-gpt4", split="train")
    instruction_count += save_dataset(ds, "alpaca_gpt4_full.jsonl",
                                     "instruction", "vicgalle/alpaca-gpt4")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 4. Dolly 15k
try:
    print("\n📚 Downloading databricks/databricks-dolly-15k...")
    # Already have this
    print("  ℹ️  Already have databricks-dolly-15k")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 5. ShareGPT conversations
try:
    print("\n📚 Downloading anon8231489123/ShareGPT_Vicuna_unfiltered...")
    ds = load_dataset("anon8231489123/ShareGPT_Vicuna_unfiltered", split="train")
    instruction_count += save_dataset(ds, "sharegpt_vicuna.jsonl",
                                     "multiturn_dialog", "anon8231489123/ShareGPT_Vicuna_unfiltered",
                                     max_examples=100000)
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 6. WizardLM Evol Instruct
try:
    print("\n📚 Downloading WizardLM/WizardLM_evol_instruct_V2_196k...")
    # Already have this
    print("  ℹ️  Already have WizardLM_evol_instruct_V2_196k")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 7. LIMA quality dataset
try:
    print("\n📚 Downloading GAIR/lima...")
    ds = load_dataset("GAIR/lima", split="train")
    instruction_count += save_dataset(ds, "lima.jsonl",
                                     "instruction", "GAIR/lima")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 8. Tulu V2 Mix
try:
    print("\n📚 Downloading allenai/tulu-v2-sft-mixture...")
    ds = load_dataset("allenai/tulu-v2-sft-mixture", split="train")
    instruction_count += save_dataset(ds, "tulu_v2_mix.jsonl",
                                     "instruction", "allenai/tulu-v2-sft-mixture",
                                     max_examples=300000)
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 9. UltraChat 200k (full)
try:
    print("\n📚 Downloading HuggingFaceH4/ultrachat_200k...")
    # Already have this
    print("  ℹ️  Already have ultrachat_200k")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 10. Flan Collection
try:
    print("\n📚 Downloading Open-Orca/FLAN...")
    ds = load_dataset("Open-Orca/FLAN", split="train")
    instruction_count += save_dataset(ds, "flan_collection.jsonl",
                                     "instruction", "Open-Orca/FLAN",
                                     max_examples=500000)
except Exception as e:
    print(f"  ⚠️  Error: {e}")

print(f"\n✅ Total instruction examples: {instruction_count:,}")

# =============================================================================
# REASONING DATASETS
# =============================================================================

print("\n" + "="*80)
print("DOWNLOADING REASONING DATASETS")
print("="*80)

reasoning_count = 0

# 1. MATH dataset
try:
    print("\n🧮 Downloading hendrycks/math...")
    ds = load_dataset("hendrycks/math", "algebra", split="train")
    reasoning_count += save_dataset(ds, "math_algebra.jsonl",
                                   "reasoning_trace", "hendrycks/math")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 2. GSM8K (already have)
print("\n🧮 Already have GSM8K")

# 3. MetaMathQA (already have)
print("🧮 Already have MetaMathQA")

# 4. MAWPS math word problems
try:
    print("\n🧮 Downloading qwedsacf/grade-school-math-instructions...")
    ds = load_dataset("qwedsacf/grade-school-math-instructions", split="train")
    reasoning_count += save_dataset(ds, "grade_school_math.jsonl",
                                   "reasoning_trace", "qwedsacf/grade-school-math-instructions")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 5. ARC Challenge
try:
    print("\n🧮 Downloading ai2_arc (challenge)...")
    ds = load_dataset("ai2_arc", "ARC-Challenge", split="train")
    reasoning_count += save_dataset(ds, "arc_challenge.jsonl",
                                   "reasoning_trace", "ai2_arc")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 6. PIQA physical reasoning
try:
    print("\n🧮 Downloading piqa...")
    ds = load_dataset("piqa", split="train")
    reasoning_count += save_dataset(ds, "piqa.jsonl",
                                   "reasoning_trace", "piqa")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 7. HellaSwag
try:
    print("\n🧮 Downloading hellaswag...")
    ds = load_dataset("hellaswag", split="train")
    reasoning_count += save_dataset(ds, "hellaswag.jsonl",
                                   "reasoning_trace", "hellaswag")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 8. WinoGrande
try:
    print("\n🧮 Downloading winogrande (xl)...")
    ds = load_dataset("winogrande", "winogrande_xl", split="train")
    reasoning_count += save_dataset(ds, "winogrande.jsonl",
                                   "reasoning_trace", "winogrande")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

print(f"\n✅ Total reasoning examples: {reasoning_count:,}")

# =============================================================================
# CODE DATASETS
# =============================================================================

print("\n" + "="*80)
print("DOWNLOADING CODE DATASETS")
print("="*80)

code_count = 0

# 1. Code Alpaca (complete)
try:
    print("\n💻 Downloading sahil2801/CodeAlpaca-20k...")
    ds = load_dataset("sahil2801/CodeAlpaca-20k", split="train")
    code_count += save_dataset(ds, "code_alpaca_20k_full.jsonl",
                               "code_instruction_multilang", "sahil2801/CodeAlpaca-20k")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 2. Code Feedback filtered
try:
    print("\n💻 Downloading m-a-p/CodeFeedback-Filtered-Instruction...")
    ds = load_dataset("m-a-p/CodeFeedback-Filtered-Instruction", split="train")
    code_count += save_dataset(ds, "code_feedback_filtered.jsonl",
                               "code_instruction_multilang", "m-a-p/CodeFeedback-Filtered-Instruction",
                               max_examples=100000)
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 3. Magicoder Evol (already have)
print("\n💻 Already have Magicoder datasets")

# 4. Glaive code assistant
print("💻 Already have Glaive code assistant")

# 5. Code contests (already have)
print("💻 Already have code_contests")

# 6. Exercism programming exercises
try:
    print("\n💻 Downloading codeparrot/github-code...")
    # This is huge, skip for now
    print("  ℹ️  Skipping github-code (too large)")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 7. Python code instructions
try:
    print("\n💻 Downloading iamtarun/python_code_instructions_18k_alpaca...")
    ds = load_dataset("iamtarun/python_code_instructions_18k_alpaca", split="train")
    code_count += save_dataset(ds, "python_code_instructions_18k.jsonl",
                               "code_instruction_multilang", "iamtarun/python_code_instructions_18k_alpaca")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

print(f"\n✅ Total code examples: {code_count:,}")

# =============================================================================
# DIALOG AND CONVERSATION DATASETS
# =============================================================================

print("\n" + "="*80)
print("DOWNLOADING DIALOG DATASETS")
print("="*80)

dialog_count = 0

# 1. Anthropic HH-RLHF (already have)
print("\n💬 Already have Anthropic/hh-rlhf")

# 2. Empathetic dialogues (already have)
print("💬 Already have empathetic_dialogues")

# 3. Persona chat (already have)
print("💬 Already have persona-chat")

# 4. Daily Dialog
try:
    print("\n💬 Downloading daily_dialog...")
    ds = load_dataset("daily_dialog", split="train")
    dialog_count += save_dataset(ds, "daily_dialog.jsonl",
                                "multiturn_dialog", "daily_dialog")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 5. Multi-turn dialog from Baize
try:
    print("\n💬 Downloading project-baize/baize-chatbot...")
    ds = load_dataset("project-baize/baize-chatbot", "quora_chat_data", split="train")
    dialog_count += save_dataset(ds, "baize_quora.jsonl",
                                "multiturn_dialog", "project-baize/baize-chatbot",
                                max_examples=100000)
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 6. Wizard conversations
try:
    print("\n💬 Downloading WizardLM/WizardLM_evol_instruct_70k...")
    # Already have this
    print("  ℹ️  Already have WizardLM_evol_instruct_70k")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

print(f"\n✅ Total dialog examples: {dialog_count:,}")

# =============================================================================
# FACTUAL / KNOWLEDGE DATASETS
# =============================================================================

print("\n" + "="*80)
print("DOWNLOADING FACTUAL KNOWLEDGE DATASETS")
print("="*80)

factual_count = 0

# 1. Natural Questions
try:
    print("\n📖 Downloading natural_questions...")
    ds = load_dataset("natural_questions", split="train[:100000]")  # Limit to 100k
    factual_count += save_dataset(ds, "natural_questions_100k.jsonl",
                                 "factual_grounding", "natural_questions",
                                 max_examples=100000)
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 2. TriviaQA (already have)
print("\n📖 Already have TriviaQA")

# 3. HotpotQA (already have)
print("📖 Already have HotpotQA")

# 4. SQuAD v2 (already have)
print("📖 Already have SQuAD v2")

# 5. MS MARCO
try:
    print("\n📖 Downloading ms_marco (v2.1)...")
    ds = load_dataset("ms_marco", "v2.1", split="train[:100000]")
    factual_count += save_dataset(ds, "ms_marco_100k.jsonl",
                                 "factual_grounding", "ms_marco",
                                 max_examples=100000)
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 6. ELI5 (Explain Like I'm 5)
try:
    print("\n📖 Downloading eli5...")
    ds = load_dataset("eli5", split="train_eli5")
    factual_count += save_dataset(ds, "eli5.jsonl",
                                 "factual_grounding", "eli5",
                                 max_examples=100000)
except Exception as e:
    print(f"  ⚠️  Error: {e}")

print(f"\n✅ Total factual examples: {factual_count:,}")

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "="*80)
print("MASSIVE CORPUS EXPANSION SUMMARY")
print("="*80)
print(f"📚 Instructions: {instruction_count:,}")
print(f"🧮 Reasoning: {reasoning_count:,}")
print(f"💻 Code: {code_count:,}")
print(f"💬 Dialog: {dialog_count:,}")
print(f"📖 Factual: {factual_count:,}")
print()
total = instruction_count + reasoning_count + code_count + dialog_count + factual_count
print(f"📊 TOTAL NEW EXAMPLES: {total:,}")
print(f"📁 Output: {output_dir}")
print()
print("="*80)
print("ALL FROM LEGITIMATE HUGGINGFACE DATASETS")
print("="*80)
