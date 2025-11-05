#!/usr/bin/env python3
"""
Download Code Quality Datasets from HuggingFace

Targets gaps demonstrated in qwen3vl:8b output:
1. Code correctness (logic bugs, syntax errors)
2. Complete working applications (not just snippets)
3. Test-driven development
4. Application architecture
5. Concise code-focused examples

Focus: Real, working, verified code for building applications
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

def download_code_quality_datasets():
    """Download datasets to improve code generation quality."""
    output_dir = Path("examples/datasets/code_quality")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_config = [
        # ====================================================================
        # CATEGORY 1: COMPLETE WORKING APPLICATIONS
        # ====================================================================
        {
            "name": "python_code_instructions_18k",
            "dataset_id": "iamtarun/python_code_instructions_18k_alpaca",
            "config": None,
            "split": "train",
            "max_examples": 18000,
            "description": "Complete Python code with clear instructions",
            "category": "applications",
            "priority": 1
        },

        # ====================================================================
        # CATEGORY 2: CODE WITH TESTS (Verified Correctness)
        # ====================================================================
        {
            "name": "code_contests",
            "dataset_id": "deepmind/code_contests",
            "config": None,
            "split": "train",
            "max_examples": 10000,
            "description": "Programming contest problems with test cases",
            "category": "verified_code",
            "priority": 1
        },
        {
            "name": "apps",
            "dataset_id": "codeparrot/apps",
            "config": None,
            "split": "train",
            "max_examples": 5000,
            "description": "Programming problems with solutions and tests",
            "category": "verified_code",
            "priority": 2
        },

        # ====================================================================
        # CATEGORY 3: CODE DEBUGGING & CORRECTION
        # ====================================================================
        {
            "name": "code_search_net_go",
            "dataset_id": "code_search_net",
            "config": "go",
            "split": "train",
            "max_examples": 20000,
            "description": "Go code with documentation (clean examples)",
            "category": "clean_code",
            "priority": 3
        },
        {
            "name": "code_search_net_java",
            "dataset_id": "code_search_net",
            "config": "java",
            "split": "train",
            "max_examples": 20000,
            "description": "Java code with documentation",
            "category": "clean_code",
            "priority": 3
        },

        # ====================================================================
        # CATEGORY 4: CONCISE CODE EXAMPLES (Less Verbose)
        # ====================================================================
        {
            "name": "code_instructions_120k",
            "dataset_id": "sahil2801/code_instructions_120k",
            "config": None,
            "split": "train",
            "max_examples": 50000,
            "description": "Large-scale code instruction dataset",
            "category": "concise_code",
            "priority": 1
        },

        # ====================================================================
        # CATEGORY 5: REAL GITHUB CODE (Not Synthetic)
        # ====================================================================
        {
            "name": "github_code_python",
            "dataset_id": "codeparrot/github-code",
            "config": "Python",
            "split": "train",
            "max_examples": 30000,
            "description": "Real Python code from GitHub",
            "category": "real_code",
            "priority": 1
        },

        # ====================================================================
        # CATEGORY 6: ALGORITHM IMPLEMENTATIONS
        # ====================================================================
        {
            "name": "leetcode_solutions",
            "dataset_id": "greengerong/leetcode",
            "config": None,
            "split": "train",
            "max_examples": 2000,
            "description": "LeetCode problems with solutions",
            "category": "algorithms",
            "priority": 2
        },

        # ====================================================================
        # CATEGORY 7: CODE EXPLANATION (But Concise)
        # ====================================================================
        {
            "name": "code_explain",
            "dataset_id": "teknium/GPTeacher-General-Instruct",
            "config": None,
            "split": "train",
            "max_examples": 10000,
            "description": "Code with concise explanations",
            "category": "explained_code",
            "priority": 3
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

                    # ========================================================
                    # APPLICATIONS & CONCISE CODE
                    # ========================================================
                    if config['category'] in ['applications', 'concise_code']:
                        instruction = safe_get(example, 'instruction')
                        if not instruction:
                            instruction = safe_get(example, 'prompt')
                        if not instruction:
                            instruction = safe_get(example, 'question')

                        output = safe_get(example, 'output')
                        if not output:
                            output = safe_get(example, 'response')
                        if not output:
                            output = safe_get(example, 'code')

                        if instruction and output and len(output) > 50:
                            # Filter: code should be longer than explanation
                            if len(output) > len(instruction) * 0.5:
                                normalized = {
                                    "instruction": instruction,
                                    "input": "",
                                    "output": output,
                                    "_source": config['name'],
                                    "_category": config['category']
                                }

                    # ========================================================
                    # VERIFIED CODE (With Tests)
                    # ========================================================
                    elif config['category'] == 'verified_code':
                        # Code contests format
                        problem = safe_get(example, 'description')
                        if not problem:
                            problem = safe_get(example, 'question')

                        solution = safe_get(example, 'solutions')
                        if not solution:
                            solution = safe_get(example, 'code')

                        # Get first solution if multiple
                        if isinstance(solution, list) and len(solution) > 0:
                            solution = solution[0]

                        # Get test cases
                        tests = safe_get(example, 'public_tests')
                        if not tests:
                            tests = safe_get(example, 'test_cases')

                        if problem and solution:
                            # Include tests in output if available
                            full_output = solution
                            if tests:
                                full_output += f"\n\n# Test cases:\n{tests}"

                            normalized = {
                                "instruction": problem,
                                "input": "",
                                "output": full_output,
                                "_source": config['name'],
                                "_category": config['category'],
                                "_verified": True
                            }

                    # ========================================================
                    # CLEAN CODE (CodeSearchNet)
                    # ========================================================
                    elif config['category'] == 'clean_code':
                        code = safe_get(example, 'whole_func_string')
                        if not code:
                            code = safe_get(example, 'code')

                        docstring = safe_get(example, 'func_documentation_string')
                        if not docstring:
                            docstring = safe_get(example, 'docstring')

                        if code and docstring and len(code) > 100:
                            normalized = {
                                "instruction": f"Write a function that {docstring}",
                                "input": "",
                                "output": code,
                                "_source": config['name'],
                                "_category": config['category']
                            }

                    # ========================================================
                    # REAL CODE (GitHub)
                    # ========================================================
                    elif config['category'] == 'real_code':
                        code = safe_get(example, 'code')

                        # Try to extract intent from filename or docstring
                        path = safe_get(example, 'path')

                        if code and len(code) > 200 and len(code) < 5000:
                            # Create instruction from filename
                            if path:
                                filename = path.split('/')[-1]
                                instruction = f"Implement the functionality from {filename}"
                            else:
                                instruction = "Implement this Python module"

                            normalized = {
                                "instruction": instruction,
                                "input": "",
                                "output": code,
                                "_source": config['name'],
                                "_category": config['category'],
                                "_real": True
                            }

                    # ========================================================
                    # ALGORITHMS
                    # ========================================================
                    elif config['category'] == 'algorithms':
                        problem = safe_get(example, 'title')
                        if not problem:
                            problem = safe_get(example, 'question')

                        solution = safe_get(example, 'solution')
                        if not solution:
                            solution = safe_get(example, 'code')

                        if problem and solution and len(solution) > 50:
                            normalized = {
                                "instruction": f"Solve: {problem}",
                                "input": "",
                                "output": solution,
                                "_source": config['name'],
                                "_category": config['category']
                            }

                    # ========================================================
                    # EXPLAINED CODE
                    # ========================================================
                    elif config['category'] == 'explained_code':
                        instruction = safe_get(example, 'instruction')
                        response = safe_get(example, 'response')

                        # Only take if response contains code
                        if instruction and response and '```' in response:
                            # Filter: must have code blocks
                            normalized = {
                                "instruction": instruction,
                                "input": "",
                                "output": response,
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
    print(" DOWNLOADING CODE QUALITY DATASETS")
    print(" Addressing gaps in qwen3vl:8b output")
    print("=" * 80)
    print()
    print("Target improvements:")
    print("  1. Code correctness (verified with tests)")
    print("  2. Complete applications (not snippets)")
    print("  3. Real GitHub code (not synthetic)")
    print("  4. Concise examples (code > explanation)")
    print("  5. Algorithm implementations")
    print()
    print("Expected total: ~165K high-quality code examples")
    print("=" * 80)

    total = download_code_quality_datasets()

    print("\n" + "=" * 80)
    print(f"[✓] CODE QUALITY DATASETS COMPLETE: {total:,} examples downloaded")
    print("=" * 80)
    print()
    print("Next steps:")
    print("  1. Merge with existing real datasets")
    print("  2. Weight code datasets higher in training")
    print("  3. Train with focus on correctness and completeness")
