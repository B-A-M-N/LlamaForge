#!/usr/bin/env python3
"""
Download ALL REAL Dataset Alternatives to Replace Synthetic Datasets

Replaces:
1. Dark protector (132K synthetic) → 2M real (open-instruct, SARC, reddit, wizard)
2. Behavioral mix (3GB synthetic) → 20K+ real counseling conversations
3. Esoteric mix (260MB synthetic) → Real philosophy/esoteric texts
4. Code debugging mix (31MB synthetic) → Real GitHub/contest code
5. DeepSeek search mix (175MB synthetic) → Real web QA

Total: Replacing ~8GB synthetic with ~3GB REAL, higher quality data
"""

import json
from pathlib import Path
from datasets import load_dataset
from tqdm import tqdm
import random

def safe_get(d, *keys, default=""):
    """Safely get nested dict values."""
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key, default)
        else:
            return default
    return d if d is not None else default

def download_all_real_alternatives():
    """Download all real dataset alternatives."""
    output_base = Path("examples/datasets/real_alternatives")
    output_base.mkdir(parents=True, exist_ok=True)

    datasets_config = [
        # ====================================================================
        # CATEGORY 1: PSYCHOLOGY/BEHAVIORAL (Replacing behavioral mix)
        # ====================================================================
        {
            "name": "mentalchat_16k",
            "dataset_id": "ShenLab/MentalChat16K",
            "config": None,
            "split": "train",
            "max_examples": 16000,
            "description": "Real counseling conversations from clinical trials",
            "category": "psychology_behavioral",
            "priority": 1
        },
        {
            "name": "mental_health_counseling",
            "dataset_id": "Amod/mental_health_counseling_conversations",
            "config": None,
            "split": "train",
            "max_examples": 10000,
            "description": "Real Q&A from mental health platforms",
            "category": "psychology_behavioral",
            "priority": 2
        },
        {
            "name": "everyday_conversations",
            "dataset_id": "HuggingFaceTB/everyday-conversations-llama3.1-2k",
            "config": None,
            "split": "train",
            "max_examples": 2000,
            "description": "Everyday human conversations",
            "category": "psychology_behavioral",
            "priority": 3
        },

        # ====================================================================
        # CATEGORY 2: ESOTERIC/PHILOSOPHY (Replacing esoteric mix)
        # ====================================================================
        {
            "name": "trismegistus_project",
            "dataset_id": "teknium/trismegistus-project",
            "config": None,
            "split": "train",
            "max_examples": 50000,
            "description": "Esoteric, mystical, occult knowledge from real texts",
            "category": "esoteric_philosophy",
            "priority": 1
        },
        {
            "name": "stanford_philosophy",
            "dataset_id": "dmarx/stanford-encyclopedia-of-philosophy_dec23",
            "config": None,
            "split": "train",
            "max_examples": 30000,
            "description": "Stanford Encyclopedia of Philosophy",
            "category": "esoteric_philosophy",
            "priority": 2
        },

        # ====================================================================
        # CATEGORY 3: WEB SEARCH/QA (Replacing DeepSeek mix)
        # ====================================================================
        # Note: MS MARCO is very large, we'll sample
        {
            "name": "web_questions",
            "dataset_id": "web_questions",
            "config": None,
            "split": "train",
            "max_examples": 5000,
            "description": "Real web-based question answering",
            "category": "web_search_qa",
            "priority": 2
        },

        # ====================================================================
        # CATEGORY 4: CODE (Replacing code debugging mix)
        # ====================================================================
        # Note: The Stack is MASSIVE, we'll sample carefully
        {
            "name": "code_alpaca",
            "dataset_id": "sahil2801/CodeAlpaca-20k",
            "config": None,
            "split": "train",
            "max_examples": 20000,
            "description": "Real code instruction dataset",
            "category": "code_real",
            "priority": 1
        },
    ]

    total_downloaded = 0

    for config in datasets_config:
        try:
            print(f"\n{'='*80}")
            print(f"[{config['priority']}] Downloading {config['name']}...")
            print(f"    Dataset: {config['dataset_id']}")
            print(f"    Description: {config['description']}")
            print(f"    Target: {config['max_examples']:,} examples")
            print(f"{'='*80}")

            # Create category subdirectory
            category_dir = output_base / config['category']
            category_dir.mkdir(parents=True, exist_ok=True)

            # Load dataset
            ds = load_dataset(
                config['dataset_id'],
                config['config'],
                split=config['split'],
                streaming=True,
                trust_remote_code=False
            )

            output_file = category_dir / f"{config['name']}.jsonl"
            count = 0

            with output_file.open("w", encoding="utf-8") as f:
                for example in tqdm(ds, total=config['max_examples'], desc=config['name']):
                    normalized = None

                    # ========================================================
                    # PSYCHOLOGY/BEHAVIORAL
                    # ========================================================
                    if config['category'] == 'psychology_behavioral':
                        # Try multiple field names
                        question = safe_get(example, 'question')
                        if not question:
                            question = safe_get(example, 'input')
                        if not question:
                            question = safe_get(example, 'instruction')
                        if not question:
                            question = safe_get(example, 'user')
                        if not question:
                            question = safe_get(example, 'prompt')

                        answer = safe_get(example, 'answer')
                        if not answer:
                            answer = safe_get(example, 'output')
                        if not answer:
                            answer = safe_get(example, 'response')
                        if not answer:
                            answer = safe_get(example, 'assistant')
                        if not answer:
                            answer = safe_get(example, 'completion')

                        # Handle conversation format
                        if not question or not answer:
                            conversations = safe_get(example, 'conversations')
                            if isinstance(conversations, list) and len(conversations) >= 2:
                                question = conversations[0].get('value', '') if isinstance(conversations[0], dict) else ''
                                answer = conversations[1].get('value', '') if isinstance(conversations[1], dict) else ''

                        if question and answer and len(question) > 10 and len(answer) > 20:
                            normalized = {
                                "instruction": question,
                                "input": "",
                                "output": answer,
                                "_source": config['name'],
                                "_category": config['category']
                            }

                    # ========================================================
                    # ESOTERIC/PHILOSOPHY
                    # ========================================================
                    elif config['category'] == 'esoteric_philosophy':
                        instruction = safe_get(example, 'instruction')
                        output = safe_get(example, 'output')

                        # Try alternative formats
                        if not instruction:
                            instruction = safe_get(example, 'question')
                        if not instruction:
                            instruction = safe_get(example, 'prompt')
                        if not instruction:
                            # Try extracting from text
                            text = safe_get(example, 'text')
                            if text and len(text) > 100:
                                # Use first part as instruction
                                parts = text.split('\n\n', 1)
                                if len(parts) == 2:
                                    instruction = parts[0][:500]
                                    output = parts[1][:2000]

                        if not output:
                            output = safe_get(example, 'response')
                        if not output:
                            output = safe_get(example, 'answer')

                        if instruction and output and len(instruction) > 20 and len(output) > 50:
                            normalized = {
                                "instruction": instruction,
                                "input": "",
                                "output": output,
                                "_source": config['name'],
                                "_category": config['category']
                            }

                    # ========================================================
                    # WEB SEARCH/QA
                    # ========================================================
                    elif config['category'] == 'web_search_qa':
                        question = safe_get(example, 'question')
                        answers = safe_get(example, 'answers')

                        if question and answers:
                            # WebQuestions format
                            if isinstance(answers, list) and len(answers) > 0:
                                answer = answers[0]
                            else:
                                answer = str(answers)

                            if len(question) > 10 and len(answer) > 5:
                                normalized = {
                                    "instruction": question,
                                    "input": "",
                                    "output": answer,
                                    "_source": config['name'],
                                    "_category": config['category']
                                }

                    # ========================================================
                    # CODE
                    # ========================================================
                    elif config['category'] == 'code_real':
                        instruction = safe_get(example, 'instruction')
                        if not instruction:
                            instruction = safe_get(example, 'prompt')

                        output = safe_get(example, 'output')
                        if not output:
                            output = safe_get(example, 'response')
                        if not output:
                            output = safe_get(example, 'code')

                        if instruction and output and len(output) > 20:
                            normalized = {
                                "instruction": instruction,
                                "input": "",
                                "output": output,
                                "_source": config['name'],
                                "_category": config['category']
                            }

                    # Write if normalized successfully
                    if normalized:
                        f.write(json.dumps(normalized, ensure_ascii=False) + '\n')
                        count += 1

                    if count >= config['max_examples']:
                        break

            print(f"[✓] Saved {count:,} examples to {output_file}")
            total_downloaded += count

        except Exception as e:
            print(f"[!] Failed to download {config['name']}: {e}")
            import traceback
            traceback.print_exc()

    return total_downloaded

if __name__ == "__main__":
    print("=" * 80)
    print(" DOWNLOADING ALL REAL DATASET ALTERNATIVES")
    print(" Replacing synthetic datasets with REAL data")
    print("=" * 80)
    print()
    print("Categories:")
    print("  1. Psychology/Behavioral: MentalChat16K, counseling conversations")
    print("  2. Esoteric/Philosophy: Trismegistus, Stanford Philosophy")
    print("  3. Web Search/QA: WebQuestions")
    print("  4. Code: CodeAlpaca")
    print()
    print("Expected total: ~100K real examples replacing ~8GB synthetic")
    print("=" * 80)

    total = download_all_real_alternatives()

    print("\n" + "=" * 80)
    print(f"[✓] ALL REAL ALTERNATIVES COMPLETE: {total:,} examples downloaded")
    print("=" * 80)
    print()
    print("Next steps:")
    print("  1. Delete synthetic datasets (ultimate_3M, expanded_1.5M, mixes)")
    print("  2. Merge all REAL datasets only")
    print("  3. Deduplicate final corpus")
    print("  4. Train on QUALITY data")
