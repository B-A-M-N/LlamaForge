#!/usr/bin/env python3
"""
Download CodeGeeX-related datasets (HumanEval-X).

HumanEval-X is a benchmark for evaluating multilingual code generation ability
with 820 high-quality human-crafted code samples across 5 programming languages.

This complements our existing code corpus with multi-language code generation examples.
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


def download_humaneval_x():
    """Download HumanEval-X multi-language code generation dataset."""
    output_dir = Path("examples/datasets/codegeex_corpus")
    output_dir.mkdir(parents=True, exist_ok=True)

    # HumanEval-X has 5 language subsets
    languages = ["python", "cpp", "go", "java", "js"]

    total_examples = 0

    for lang in languages:
        try:
            print(f"\n[→] Downloading HumanEval-X ({lang})...")

            ds = load_dataset(
                "THUDM/humaneval-x",
                lang,
                split="test",  # HumanEval-X only has test split
                streaming=False,  # Small dataset, no need for streaming
                trust_remote_code=True  # Required for HumanEval-X
            )

            output_file = output_dir / f"humaneval_x_{lang}.jsonl"
            count = 0

            with output_file.open("w", encoding="utf-8") as f:
                for example in tqdm(ds, desc=f"humaneval-x-{lang}"):
                    # HumanEval-X format:
                    # - task_id: Unique task identifier
                    # - prompt: Code prompt/stub
                    # - declaration: Function declaration
                    # - canonical_solution: Reference solution
                    # - test: Test cases
                    # - entry_point: Function entry point

                    prompt = safe_get(example, "prompt", default="")
                    declaration = safe_get(example, "declaration", default="")
                    canonical_solution = safe_get(example, "canonical_solution", default="")
                    task_id = safe_get(example, "task_id", default="")

                    if prompt and canonical_solution:
                        # Create instruction: implement the function
                        instruction = f"Complete this {lang.upper()} function:\n\n{prompt}"

                        # Include declaration if available
                        if declaration and declaration != prompt:
                            instruction = f"Implement this {lang.upper()} function:\n\n{declaration}"

                        # Output is the full solution
                        output = canonical_solution

                        normalized = {
                            "instruction": instruction,
                            "input": "",
                            "output": output,
                            "_source": f"humaneval_x_{lang}",
                            "_category": "code_generation_multilang",
                            "_task_id": task_id,
                            "_language": lang
                        }
                        f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                        count += 1

            print(f"[✓] Saved {count:,} {lang.upper()} examples to {output_file}")
            total_examples += count

        except Exception as e:
            print(f"[!] Failed to download HumanEval-X ({lang}): {e}")

    print(f"\n[✓] Total HumanEval-X examples: {total_examples:,}")
    return total_examples


def download_additional_code_datasets():
    """Download additional large-scale code datasets similar to CodeGeeX training data."""
    output_dir = Path("examples/datasets/codegeex_corpus")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Additional code instruction datasets to complement HumanEval-X
    datasets_to_download = [
        # Code Alpaca (already may have this, but ensure we get it)
        ("sahil2801/CodeAlpaca-20k", "code_alpaca_20k", None, 20_000),

        # Evol-CodeAlpaca (evolved code instructions)
        ("theblackcat102/evol-codealpaca-v1", "evol_codealpaca", None, 110_000),

        # Code Feedback (multi-language code with feedback)
        ("m-a-p/Code-Feedback", "code_feedback_corpus", None, 100_000),

        # OpenCodeInterpreter (code execution and interpretation)
        ("m-a-p/CodeFeedback-Filtered-Instruction", "code_feedback_filtered", None, 50_000),
    ]

    total_downloaded = 0

    for dataset_info in datasets_to_download:
        dataset_id, name, config, max_examples = dataset_info

        try:
            print(f"\n[→] Downloading {name} from {dataset_id}...")

            ds = load_dataset(
                dataset_id,
                config,
                split="train",
                streaming=True,
                trust_remote_code=False
            )

            output_file = output_dir / f"{name}.jsonl"
            count = 0

            with output_file.open("w", encoding="utf-8") as f:
                for example in tqdm(ds, total=max_examples, desc=name):
                    # Try to extract instruction/output from various formats
                    instruction = safe_get(example, "instruction",
                                          default=safe_get(example, "prompt",
                                          default=safe_get(example, "question")))

                    output = safe_get(example, "output",
                                     default=safe_get(example, "response",
                                     default=safe_get(example, "answer",
                                     default=safe_get(example, "code"))))

                    input_text = safe_get(example, "input", default="")

                    if instruction and output:
                        normalized = {
                            "instruction": instruction,
                            "input": input_text,
                            "output": output,
                            "_source": name,
                            "_category": "code_instruction_multilang"
                        }
                        f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                        count += 1

                    if count >= max_examples:
                        break

            print(f"[✓] Saved {count:,} examples to {output_file}")
            total_downloaded += count

        except Exception as e:
            print(f"[!] Failed to download {name}: {e}")

    return total_downloaded


if __name__ == "__main__":
    print("=" * 80)
    print(" CODEGEEX CORPUS DOWNLOAD")
    print(" Adding multi-language code generation datasets")
    print("=" * 80)

    # Download HumanEval-X (820 examples across 5 languages)
    print("\n[1/2] Downloading HumanEval-X (multi-language code evaluation)...")
    humaneval_count = download_humaneval_x()

    # Download additional large-scale code datasets
    print("\n[2/2] Downloading additional code instruction datasets...")
    additional_count = download_additional_code_datasets()

    print("\n" + "=" * 80)
    print("[✓] CODEGEEX CORPUS DOWNLOAD COMPLETE")
    print(f"    HumanEval-X: {humaneval_count:,} examples")
    print(f"    Additional:  {additional_count:,} examples")
    print(f"    Total:       {humaneval_count + additional_count:,} examples")
    print("=" * 80)
