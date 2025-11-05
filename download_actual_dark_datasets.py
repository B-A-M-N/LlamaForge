#!/usr/bin/env python3
"""
Download ACTUAL Dark Protector Datasets from HuggingFace

Replaces the 150K synthetic template with real datasets:
- open-instruct-uncensored (1.7M - removes refusals/safety theater)
- SARC_Sarcasm (1.3M - Reddit sarcasm)
- reddit-sarcasm (~100K - sarcasm detection)
- wizard_vicuna_70k_unfiltered (70K - no alignment)

Target: ~2M examples of REAL dark humor, sarcasm, brutal honesty
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

def download_actual_dark_datasets():
    """Download real dark protector datasets."""
    output_dir = Path("examples/datasets/dark_protector_actual")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_config = [
        # ====================================================================
        # 1. OPEN-INSTRUCT-UNCENSORED (CRITICAL - Removes refusals)
        # ====================================================================
        {
            "name": "open_instruct_uncensored",
            "dataset_id": "cognitivecomputations/open-instruct-uncensored",
            "config": None,
            "split": "train",
            "max_examples": 1700000,  # Full dataset
            "description": "ShareGPT with refusals removed - brutal honesty over safety theater",
            "category": "uncensored_instructions",
            "priority": 1
        },

        # ====================================================================
        # 2. SARC SARCASM (HIGH - Reddit sarcasm corpus)
        # ====================================================================
        {
            "name": "sarc_sarcasm",
            "dataset_id": "CreativeLang/SARC_Sarcasm",
            "config": None,
            "split": "train",
            "max_examples": 200000,  # Sample 200K from 1.3M (avoid overwhelming corpus)
            "description": "Reddit sarcasm corpus - natural dark humor",
            "category": "sarcasm",
            "priority": 2
        },

        # ====================================================================
        # 3. REDDIT SARCASM (MEDIUM - Sarcasm detection pairs)
        # ====================================================================
        {
            "name": "reddit_sarcasm",
            "dataset_id": "Thewillonline/reddit-sarcasm",
            "config": None,
            "split": "train",
            "max_examples": 100000,  # Full dataset expected ~100K
            "description": "Reddit sarcasm detection dataset",
            "category": "sarcasm",
            "priority": 3
        },

        # ====================================================================
        # 4. WIZARD VICUNA UNFILTERED (FAST - No alignment)
        # ====================================================================
        {
            "name": "wizard_vicuna_unfiltered",
            "dataset_id": "ehartford/wizard_vicuna_70k_unfiltered",
            "config": None,
            "split": "train",
            "max_examples": 70000,  # Full dataset
            "description": "Wizard-Vicuna unfiltered - no safety alignment",
            "category": "uncensored_instructions",
            "priority": 4
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

            # Load dataset
            ds = load_dataset(
                config['dataset_id'],
                config['config'],
                split=config['split'],
                streaming=True,
                trust_remote_code=False
            )

            output_file = output_dir / f"{config['name']}.jsonl"
            count = 0

            with output_file.open("w", encoding="utf-8") as f:
                for example in tqdm(ds, total=config['max_examples'], desc=config['name']):
                    normalized = None

                    # ========================================================
                    # UNCENSORED INSTRUCTIONS (open-instruct, wizard_vicuna)
                    # ========================================================
                    if config['category'] == 'uncensored_instructions':
                        # These are typically in conversational format

                        # Try multiple formats
                        instruction = safe_get(example, 'instruction')
                        if not instruction:
                            instruction = safe_get(example, 'prompt')
                        if not instruction:
                            instruction = safe_get(example, 'input')
                        if not instruction:
                            # Try conversation format
                            conversations = safe_get(example, 'conversations')
                            if isinstance(conversations, list) and len(conversations) > 0:
                                # Extract first user message
                                for conv in conversations:
                                    if isinstance(conv, dict) and conv.get('from') == 'human':
                                        instruction = conv.get('value', '')
                                        break

                        output = safe_get(example, 'output')
                        if not output:
                            output = safe_get(example, 'response')
                        if not output:
                            output = safe_get(example, 'completion')
                        if not output:
                            # Try conversation format
                            conversations = safe_get(example, 'conversations')
                            if isinstance(conversations, list) and len(conversations) > 1:
                                # Extract first assistant response
                                for conv in conversations:
                                    if isinstance(conv, dict) and conv.get('from') in ['gpt', 'assistant']:
                                        output = conv.get('value', '')
                                        break

                        if instruction and output and len(instruction) > 10 and len(output) > 20:
                            normalized = {
                                "instruction": instruction,
                                "input": "",
                                "output": output,
                                "_source": config['name'],
                                "_category": config['category']
                            }

                    # ========================================================
                    # SARCASM (SARC, reddit-sarcasm)
                    # ========================================================
                    elif config['category'] == 'sarcasm':
                        # SARC format: parent comment + sarcastic response
                        context = safe_get(example, 'context')
                        response = safe_get(example, 'response')

                        if not context:
                            context = safe_get(example, 'parent_comment')
                        if not response:
                            response = safe_get(example, 'comment')

                        # Label (whether it's sarcastic)
                        label = safe_get(example, 'label')

                        # Only take sarcastic examples (label == 1 or label == 'sarcastic')
                        is_sarcastic = (label == 1 or label == '1' or label == 'sarcastic' or label == True)

                        # If no label field, try 'sarcasm' field
                        if label == "" or label is None:
                            sarcasm_field = safe_get(example, 'sarcasm')
                            is_sarcastic = (sarcasm_field == 1 or sarcasm_field == '1' or sarcasm_field == True)

                        # Some datasets don't have labels - take all if no label field
                        if label == "" or label is None:
                            is_sarcastic = True  # Assume dataset is pre-filtered

                        if context and response and is_sarcastic and len(response) > 10:
                            # Format as instruction-response pair
                            instruction = f"{context}"

                            normalized = {
                                "instruction": instruction,
                                "input": "",
                                "output": response,
                                "_source": config['name'],
                                "_category": config['category']
                            }

                    # Write if normalized successfully
                    if normalized:
                        f.write(json.dumps(normalized, ensure_ascii=False) + '\\n')
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
    print(" DOWNLOADING ACTUAL DARK PROTECTOR DATASETS")
    print(" Replacing 150K synthetic template with REAL data")
    print("=" * 80)
    print()
    print("Target datasets:")
    print("  1. open-instruct-uncensored: 1.7M (removes refusals)")
    print("  2. SARC_Sarcasm: 200K (Reddit sarcasm)")
    print("  3. reddit-sarcasm: 100K (sarcasm detection)")
    print("  4. wizard_vicuna_unfiltered: 70K (no alignment)")
    print()
    print("Expected total: ~2M real examples")
    print("=" * 80)

    total = download_actual_dark_datasets()

    print("\\n" + "=" * 80)
    print(f"[✓] ACTUAL DARK DATASETS COMPLETE: {total:,} examples downloaded")
    print("=" * 80)
    print()
    print("Next steps:")
    print("  1. Replace synthetic dark_protector_ultra_massive_150k.jsonl")
    print("  2. Use these REAL datasets in final merge")
    print("  3. Update training config to weight uncensored data")
