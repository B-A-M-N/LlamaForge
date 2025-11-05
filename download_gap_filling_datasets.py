#!/usr/bin/env python3
"""
Download Gap-Filling Datasets

Covers remaining gaps from qwen3vl:8b analysis:
1. Game development (Pygame, game mechanics)
2. Bug fixing / code refactoring
3. Multi-file projects / architecture
4. Web development (Flask, FastAPI, Django)
5. Testing (unittest, pytest)
6. Database / SQL
7. System design
8. More algorithm implementations
"""

import json
from pathlib import Path
from datasets import load_dataset
from tqdm import tqdm

def safe_get(d, *keys, default=""):
    """Safely get nested dict values."""
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key, default)
        else:
            return default
    return d if d is not None else default

def download_gap_filling_datasets():
    """Download datasets to fill remaining gaps."""
    output_dir = Path("examples/datasets/gap_filling")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_config = [
        # ====================================================================
        # GAP 1: REFACTORING & CODE IMPROVEMENT
        # ====================================================================
        {
            "name": "code_refactoring",
            "dataset_id": "BAAI/TACO",
            "config": None,
            "split": "train",
            "max_examples": 20000,
            "description": "Code refactoring and improvement examples",
            "category": "refactoring",
            "priority": 1
        },

        # ====================================================================
        # GAP 2: MORE ALGORITHMS & DATA STRUCTURES
        # ====================================================================
        {
            "name": "algorithm_implementations",
            "dataset_id": "ise-uiuc/Magicoder-OSS-Instruct-75K",
            "config": None,
            "split": "train",
            "max_examples": 30000,
            "description": "Algorithm implementations from open source",
            "category": "algorithms",
            "priority": 1
        },
        {
            "name": "algorithm_evol",
            "dataset_id": "ise-uiuc/Magicoder-Evol-Instruct-110K",
            "config": None,
            "split": "train",
            "max_examples": 30000,
            "description": "Evolution of algorithm implementations",
            "category": "algorithms",
            "priority": 1
        },

        # ====================================================================
        # GAP 3: WEB DEVELOPMENT
        # ====================================================================
        {
            "name": "web_development",
            "dataset_id": "TokenBender/code_instructions_122k_alpaca_style",
            "config": None,
            "split": "train",
            "max_examples": 30000,
            "description": "Web development code instructions",
            "category": "web_dev",
            "priority": 2
        },

        # ====================================================================
        # GAP 4: DATABASE & SQL
        # ====================================================================
        {
            "name": "sql_create_context",
            "dataset_id": "b-mc2/sql-create-context",
            "config": None,
            "split": "train",
            "max_examples": 50000,
            "description": "SQL queries with context",
            "category": "database",
            "priority": 1
        },
        {
            "name": "text_to_sql",
            "dataset_id": "Clinton/Text-to-sql-v1",
            "config": None,
            "split": "train",
            "max_examples": 10000,
            "description": "Text to SQL conversion",
            "category": "database",
            "priority": 2
        },

        # ====================================================================
        # GAP 5: PYTHON EXERCISES (More Complete Examples)
        # ====================================================================
        {
            "name": "python_exercises",
            "dataset_id": "flytech/python-codes-25k",
            "config": None,
            "split": "train",
            "max_examples": 25000,
            "description": "25K Python code exercises",
            "category": "exercises",
            "priority": 1
        },

        # ====================================================================
        # GAP 6: CODE EXPLANATION & DOCUMENTATION
        # ====================================================================
        {
            "name": "code_documentation",
            "dataset_id": "code_x_glue_cc_code_to_code_trans",
            "config": None,
            "split": "train",
            "max_examples": 10000,
            "description": "Code translation and documentation",
            "category": "documentation",
            "priority": 3
        },

        # ====================================================================
        # GAP 7: DIVERSE CODE TASKS
        # ====================================================================
        {
            "name": "diverse_coding",
            "dataset_id": "m-a-p/CodeFeedback-Filtered-Instruction",
            "config": None,
            "split": "train",
            "max_examples": 30000,
            "description": "Diverse coding tasks with feedback",
            "category": "diverse",
            "priority": 1
        },

        # ====================================================================
        # GAP 8: MORE LEETCODE/COMPETITIVE PROGRAMMING
        # ====================================================================
        {
            "name": "competitive_programming",
            "dataset_id": "deepmind/code_contests",
            "config": None,
            "split": "test",
            "max_examples": 5000,
            "description": "More competitive programming problems",
            "category": "competitive",
            "priority": 2
        },

        # ====================================================================
        # GAP 9: PRACTICAL PYTHON
        # ====================================================================
        {
            "name": "practical_python",
            "dataset_id": "Vezora/Tested-22k-Python-Alpaca",
            "config": None,
            "split": "train",
            "max_examples": 22000,
            "description": "Tested Python code examples",
            "category": "practical",
            "priority": 1
        },

        # ====================================================================
        # GAP 10: CODE GENERATION VARIETY
        # ====================================================================
        {
            "name": "code_alpaca_20k",
            "dataset_id": "lucasmccabe-lmi/CodeAlpaca-20k",
            "config": None,
            "split": "train",
            "max_examples": 20000,
            "description": "Code generation variety",
            "category": "generation",
            "priority": 2
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
            category_dir = output_dir / config['category']
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

                    # Universal normalization for code datasets
                    instruction = (safe_get(example, 'instruction') or
                                 safe_get(example, 'prompt') or
                                 safe_get(example, 'question') or
                                 safe_get(example, 'input') or
                                 safe_get(example, 'problem'))

                    output = (safe_get(example, 'output') or
                            safe_get(example, 'response') or
                            safe_get(example, 'code') or
                            safe_get(example, 'solution') or
                            safe_get(example, 'answer'))

                    # Handle solutions that are lists or dicts
                    if isinstance(output, dict):
                        output = safe_get(output, 'code') or safe_get(output, 'text') or str(output)
                    elif isinstance(output, list) and len(output) > 0:
                        output = output[0] if isinstance(output[0], str) else str(output[0])

                    # For SQL datasets
                    if config['category'] == 'database':
                        query = safe_get(example, 'sql') or safe_get(example, 'query')
                        context = safe_get(example, 'context') or safe_get(example, 'question')

                        if query and context:
                            instruction = f"Write SQL for: {context}"
                            output = query

                    # Quality filters
                    if instruction and output:
                        instruction = str(instruction)
                        output = str(output)

                        # Filter: must have substantial code
                        if len(output) > 50 and len(instruction) > 10:
                            # Filter: code should be longer than instruction for most cases
                            if config['category'] in ['algorithms', 'exercises', 'practical']:
                                if len(output) < len(instruction) * 0.3:
                                    continue

                            normalized = {
                                "instruction": instruction[:2000],  # Limit length
                                "input": "",
                                "output": output[:10000],  # Limit code length
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
    print(" DOWNLOADING GAP-FILLING DATASETS")
    print(" Covering remaining code quality gaps")
    print("=" * 80)
    print()
    print("Additional coverage:")
    print("  1. Code refactoring & improvement")
    print("  2. More algorithms & data structures")
    print("  3. Web development (Flask, Django, FastAPI)")
    print("  4. Database & SQL")
    print("  5. More Python exercises")
    print("  6. Code documentation")
    print("  7. Diverse coding tasks")
    print("  8. Competitive programming")
    print("  9. Practical tested Python")
    print("  10. Code generation variety")
    print()
    print("Expected total: ~250K+ additional examples")
    print("=" * 80)

    total = download_gap_filling_datasets()

    print("\n" + "=" * 80)
    print(f"[✓] GAP-FILLING DATASETS COMPLETE: {total:,} examples downloaded")
    print("=" * 80)
    print()
    print("Total corpus now:")
    print("  - Base real: ~2M")
    print("  - Phase 5: ~169K")
    print("  - Real alternatives: ~38K")
    print("  - Code quality: ~63K")
    print("  - Gap filling: ~" + f"{total//1000}K")
    print(f"  - GRAND TOTAL: ~{(2000 + 169 + 38 + 63 + total//1000)}K examples")
