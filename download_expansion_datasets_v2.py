#!/usr/bin/env python3
"""
Download expansion datasets - simplified and robust version.
Focuses on well-tested, high-quality datasets with reliable formats.
"""

import json
import os
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


def download_multiturn_dialog():
    """Download multi-turn conversation datasets."""
    output_dir = Path("examples/datasets/expansion/multiturn_dialog")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Anthropic HH-RLHF
    print("\n[→] Downloading Anthropic HH-RLHF...")
    try:
        ds = load_dataset("Anthropic/hh-rlhf", split="train", streaming=True)
        output_file = output_dir / "hh_rlhf.jsonl"
        count = 0

        with output_file.open("w", encoding="utf-8") as f:
            for example in tqdm(ds, total=150_000, desc="hh_rlhf"):
                chosen = safe_get(example, "chosen")
                if not chosen or "Human:" not in chosen or "Assistant:" not in chosen:
                    continue

                # Parse Human/Assistant dialog
                parts = chosen.split("\n\nAssistant:")
                if len(parts) >= 2:
                    instruction = parts[0].replace("\n\nHuman:", "").strip()
                    output = parts[1].split("\n\nHuman:")[0].strip()

                    if instruction and output:
                        normalized = {
                            "instruction": instruction,
                            "input": "",
                            "output": output,
                            "_source": "hh_rlhf",
                            "_category": "multiturn_dialog"
                        }
                        f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                        count += 1

                if count >= 150_000:
                    break

        print(f"[✓] Saved {count:,} examples to {output_file}")
    except Exception as e:
        print(f"[!] Failed: {e}")

    # 2. UltraChat
    print("\n[→] Downloading UltraChat...")
    try:
        ds = load_dataset("stingning/ultrachat", split="train", streaming=True)
        output_file = output_dir / "ultrachat.jsonl"
        count = 0

        with output_file.open("w", encoding="utf-8") as f:
            for example in tqdm(ds, total=200_000, desc="ultrachat"):
                data = safe_get(example, "data")
                if isinstance(data, list) and len(data) >= 2:
                    instruction = data[0] if isinstance(data[0], str) else ""
                    output = data[1] if isinstance(data[1], str) else ""

                    if instruction and output:
                        normalized = {
                            "instruction": instruction,
                            "input": "",
                            "output": output,
                            "_source": "ultrachat",
                            "_category": "multiturn_dialog"
                        }
                        f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                        count += 1

                if count >= 200_000:
                    break

        print(f"[✓] Saved {count:,} examples to {output_file}")
    except Exception as e:
        print(f"[!] Failed: {e}")


def download_reasoning_traces():
    """Download reasoning trace datasets."""
    output_dir = Path("examples/datasets/expansion/reasoning_traces")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. MathInstruct
    print("\n[→] Downloading MathInstruct...")
    try:
        ds = load_dataset("TIGER-Lab/MathInstruct", split="train", streaming=True)
        output_file = output_dir / "math_instruct.jsonl"
        count = 0

        with output_file.open("w", encoding="utf-8") as f:
            for example in tqdm(ds, total=100_000, desc="math_instruct"):
                instruction = safe_get(example, "instruction")
                output = safe_get(example, "output")

                if instruction and output:
                    normalized = {
                        "instruction": instruction,
                        "input": safe_get(example, "input", default=""),
                        "output": output,
                        "_source": "math_instruct",
                        "_category": "reasoning_trace"
                    }
                    f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                    count += 1

                if count >= 100_000:
                    break

        print(f"[✓] Saved {count:,} examples to {output_file}")
    except Exception as e:
        print(f"[!] Failed: {e}")

    # 2. GSM8K with reasoning
    print("\n[→] Downloading GSM8K...")
    try:
        ds = load_dataset("gsm8k", "main", split="train")
        output_file = output_dir / "gsm8k_reasoning.jsonl"
        count = 0

        with output_file.open("w", encoding="utf-8") as f:
            for example in tqdm(ds, desc="gsm8k"):
                question = safe_get(example, "question")
                answer = safe_get(example, "answer")

                if question and answer:
                    normalized = {
                        "instruction": question,
                        "input": "",
                        "output": answer,
                        "_source": "gsm8k",
                        "_category": "reasoning_trace"
                    }
                    f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                    count += 1

        print(f"[✓] Saved {count:,} examples to {output_file}")
    except Exception as e:
        print(f"[!] Failed: {e}")


def download_code_debugging():
    """Download code debugging datasets."""
    output_dir = Path("examples/datasets/expansion/code_debugging")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Code Alpaca 20k
    print("\n[→] Downloading Code Alpaca 20k...")
    try:
        ds = load_dataset("sahil2801/CodeAlpaca-20k", split="train")
        output_file = output_dir / "code_alpaca_20k.jsonl"
        count = 0

        with output_file.open("w", encoding="utf-8") as f:
            for example in tqdm(ds, desc="code_alpaca"):
                instruction = safe_get(example, "instruction")
                output = safe_get(example, "output")

                if instruction and output:
                    normalized = {
                        "instruction": instruction,
                        "input": safe_get(example, "input", default=""),
                        "output": output,
                        "_source": "code_alpaca_20k",
                        "_category": "code_debugging"
                    }
                    f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                    count += 1

        print(f"[✓] Saved {count:,} examples to {output_file}")
    except Exception as e:
        print(f"[!] Failed: {e}")

    # 2. APPS coding problems
    print("\n[→] Downloading APPS...")
    try:
        ds = load_dataset("codeparrot/apps", split="train", streaming=True)
        output_file = output_dir / "apps.jsonl"
        count = 0

        with output_file.open("w", encoding="utf-8") as f:
            for example in tqdm(ds, total=50_000, desc="apps"):
                problem = safe_get(example, "question")
                solutions = safe_get(example, "solutions")

                if problem and solutions:
                    # Parse JSON solutions if needed
                    if isinstance(solutions, str):
                        try:
                            solutions = json.loads(solutions)
                            if isinstance(solutions, list) and solutions:
                                solution = solutions[0]
                            else:
                                solution = solutions
                        except:
                            solution = solutions
                    else:
                        solution = str(solutions)

                    normalized = {
                        "instruction": f"Solve this coding problem:\n\n{problem}",
                        "input": "",
                        "output": solution,
                        "_source": "apps",
                        "_category": "code_debugging"
                    }
                    f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                    count += 1

                if count >= 50_000:
                    break

        print(f"[✓] Saved {count:,} examples to {output_file}")
    except Exception as e:
        print(f"[!] Failed: {e}")


def download_tool_api():
    """Download tool & API datasets."""
    output_dir = Path("examples/datasets/expansion/tool_api")
    output_dir.mkdir(parents=True, exist_ok=True)

    # XLAM Function Calling 60k
    print("\n[→] Downloading XLAM Function Calling...")
    try:
        ds = load_dataset("Salesforce/xlam-function-calling-60k", split="train")
        output_file = output_dir / "xlam_function_calling.jsonl"
        count = 0

        with output_file.open("w", encoding="utf-8") as f:
            for example in tqdm(ds, desc="xlam"):
                query = safe_get(example, "query")
                answers = safe_get(example, "answers")

                if query and answers:
                    normalized = {
                        "instruction": query,
                        "input": "",
                        "output": str(answers),
                        "_source": "xlam_function_calling",
                        "_category": "tool_api"
                    }
                    f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                    count += 1

        print(f"[✓] Saved {count:,} examples to {output_file}")
    except Exception as e:
        print(f"[!] Failed: {e}")


def download_factual_grounding():
    """Download factual grounding datasets."""
    output_dir = Path("examples/datasets/expansion/factual_grounding")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. SQuAD v2
    print("\n[→] Downloading SQuAD v2...")
    try:
        ds = load_dataset("squad_v2", split="train")
        output_file = output_dir / "squad_v2.jsonl"
        count = 0

        with output_file.open("w", encoding="utf-8") as f:
            for example in tqdm(ds, desc="squad_v2"):
                question = safe_get(example, "question")
                answers = safe_get(example, "answers")
                context = safe_get(example, "context")

                if question and answers:
                    answer_text = ""
                    if isinstance(answers, dict) and "text" in answers:
                        texts = answers["text"]
                        if isinstance(texts, list) and texts:
                            answer_text = texts[0]

                    if answer_text:
                        normalized = {
                            "instruction": question,
                            "input": context,
                            "output": answer_text,
                            "_source": "squad_v2",
                            "_category": "factual_grounding"
                        }
                        f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                        count += 1

        print(f"[✓] Saved {count:,} examples to {output_file}")
    except Exception as e:
        print(f"[!] Failed: {e}")

    # 2. TriviaQA
    print("\n[→] Downloading TriviaQA...")
    try:
        ds = load_dataset("trivia_qa", "rc.nocontext", split="train", streaming=True)
        output_file = output_dir / "trivia_qa.jsonl"
        count = 0

        with output_file.open("w", encoding="utf-8") as f:
            for example in tqdm(ds, total=30_000, desc="trivia_qa"):
                question = safe_get(example, "question")
                answer = safe_get(example, "answer")

                if question:
                    # Extract answer value
                    if isinstance(answer, dict):
                        answer_text = safe_get(answer, "value", default="")
                        if not answer_text:
                            answer_text = safe_get(answer, "normalized_value", default="")
                    else:
                        answer_text = str(answer)

                    if answer_text:
                        normalized = {
                            "instruction": question,
                            "input": "",
                            "output": answer_text,
                            "_source": "trivia_qa",
                            "_category": "factual_grounding"
                        }
                        f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                        count += 1

                if count >= 30_000:
                    break

        print(f"[✓] Saved {count:,} examples to {output_file}")
    except Exception as e:
        print(f"[!] Failed: {e}")


def download_creative_narrative():
    """Download creative writing datasets."""
    output_dir = Path("examples/datasets/expansion/creative_narrative")
    output_dir.mkdir(parents=True, exist_ok=True)

    # WritingPrompts
    print("\n[→] Downloading WritingPrompts...")
    try:
        ds = load_dataset("euclaise/writingprompts", split="train", streaming=True)
        output_file = output_dir / "writing_prompts.jsonl"
        count = 0

        with output_file.open("w", encoding="utf-8") as f:
            for example in tqdm(ds, total=100_000, desc="writing_prompts"):
                prompt = safe_get(example, "prompt")
                story = safe_get(example, "story")

                if prompt and story and len(story) > 100:
                    normalized = {
                        "instruction": prompt,
                        "input": "",
                        "output": story[:2000],  # Limit length
                        "_source": "writing_prompts",
                        "_category": "creative_narrative"
                    }
                    f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                    count += 1

                if count >= 100_000:
                    break

        print(f"[✓] Saved {count:,} examples to {output_file}")
    except Exception as e:
        print(f"[!] Failed: {e}")


if __name__ == "__main__":
    print("=" * 80)
    print(" EXPANSION DATASET DOWNLOADER V2")
    print(" Robust, tested datasets with reliable formats")
    print("=" * 80)

    download_multiturn_dialog()
    download_reasoning_traces()
    download_code_debugging()
    download_tool_api()
    download_factual_grounding()
    download_creative_narrative()

    print("\n" + "=" * 80)
    print("[✓] DOWNLOADS COMPLETE")
    print("=" * 80)
