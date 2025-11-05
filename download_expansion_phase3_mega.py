#!/usr/bin/env python3
"""
Phase 3 MEGA Expansion: Scale to 10M total examples.

Target: +5.5M examples across all categories
Strategy: Use the largest available high-quality datasets
Focus: Emergent personality through massive diverse exposure

Current: ~4.6M
Target: ~10M
Gap: ~5.4M examples
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


def download_mega_code_datasets():
    """Download massive code & technical datasets (+1.5M)."""
    output_dir = Path("examples/datasets/expansion_phase3/mega_code")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_download = [
        # StarCoder data
        ("bigcode/starcoderdata", "starcoderdata", "python", 300_000, True),

        # Code contests
        ("deepmind/code_contests", "code_contests", None, 100_000, False),

        # The Stack - dedup
        ("bigcode/the-stack-dedup", "the_stack_python", "data/python", 300_000, True),

        # CodeSearchNet
        ("code_search_net", "code_search_net", "python", 200_000, True),

        # Apps programming problems
        ("codeparrot/apps", "apps_programming", None, 100_000, True),

        # Code instructions
        ("iamtarun/python_code_instructions_18k_alpaca", "python_instructions", None, 50_000, False),

        # Stack Exchange code QA
        ("pacovaldez/stackoverflow-questions", "stackoverflow", None, 400_000, False),

        # Additional magicoder
        ("ise-uiuc/Magicoder-Evol-Instruct-110K", "magicoder_extra", None, 50_000, False),
    ]

    for dataset_info in datasets_to_download:
        if len(dataset_info) == 5:
            dataset_id, name, config, max_examples, trust_code = dataset_info
        else:
            dataset_id, name, config, max_examples = dataset_info
            trust_code = False

        try:
            print(f"\n[→] Downloading {name} from {dataset_id}...")
            ds = load_dataset(
                dataset_id,
                config,
                split="train",
                streaming=True,
                trust_remote_code=trust_code
            )
            output_file = output_dir / f"{name}.jsonl"
            count = 0

            with output_file.open("w", encoding="utf-8") as f:
                for example in tqdm(ds, total=max_examples, desc=name):
                    # Handle different code formats
                    code = safe_get(example, "content",
                                   default=safe_get(example, "code",
                                   default=safe_get(example, "text")))

                    instruction = safe_get(example, "instruction",
                                          default=safe_get(example, "question",
                                          default=f"Analyze this code"))

                    output = safe_get(example, "output",
                                     default=safe_get(example, "answer",
                                     default=code))

                    if (code or instruction) and output:
                        normalized = {
                            "instruction": instruction,
                            "input": code if code != output else "",
                            "output": output,
                            "_source": name,
                            "_category": "technical_code"
                        }
                        f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                        count += 1

                    if count >= max_examples:
                        break

            print(f"[✓] Saved {count:,} examples to {output_file}")

        except Exception as e:
            print(f"[!] Failed to download {name}: {e}")


def download_mega_instruction_datasets():
    """Download massive general instruction datasets (+1.5M)."""
    output_dir = Path("examples/datasets/expansion_phase3/mega_instruction")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_download = [
        # Databricks Dolly
        ("databricks/databricks-dolly-15k", "dolly_15k", None, 15_000, False),

        # ShareGPT90K
        ("RyokoAI/ShareGPT52K", "sharegpt_52k", None, 52_000, False),

        # OpenHermes 2.5
        ("teknium/OpenHermes-2.5", "openhermes", None, 500_000, False),

        # Ultrafeedback
        ("HuggingFaceH4/ultrafeedback_binarized", "ultrafeedback", None, 200_000, False),

        # SlimOrca
        ("Open-Orca/SlimOrca", "slimorca", None, 300_000, False),

        # Flan v2
        ("SirNeural/flan_v2", "flan_v2", None, 500_000, False),
    ]

    for dataset_info in datasets_to_download:
        if len(dataset_info) == 5:
            dataset_id, name, config, max_examples, trust_code = dataset_info
        else:
            dataset_id, name, config, max_examples = dataset_info
            trust_code = False

        try:
            print(f"\n[→] Downloading {name} from {dataset_id}...")
            ds = load_dataset(
                dataset_id,
                config,
                split="train",
                streaming=True,
                trust_remote_code=trust_code
            )
            output_file = output_dir / f"{name}.jsonl"
            count = 0

            with output_file.open("w", encoding="utf-8") as f:
                for example in tqdm(ds, total=max_examples, desc=name):
                    instruction = safe_get(example, "instruction",
                                          default=safe_get(example, "prompt",
                                          default=safe_get(example, "question")))
                    output = safe_get(example, "output",
                                     default=safe_get(example, "response",
                                     default=safe_get(example, "chosen")))

                    if instruction and output:
                        normalized = {
                            "instruction": instruction,
                            "input": safe_get(example, "input", default=""),
                            "output": output,
                            "_source": name,
                            "_category": "general_instruction"
                        }
                        f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                        count += 1

                    if count >= max_examples:
                        break

            print(f"[✓] Saved {count:,} examples to {output_file}")

        except Exception as e:
            print(f"[!] Failed to download {name}: {e}")


def download_mega_math_reasoning():
    """Download massive math & reasoning datasets (+1M)."""
    output_dir = Path("examples/datasets/expansion_phase3/mega_math_reasoning")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_download = [
        # MATH dataset
        ("hendrycks/competition_math", "competition_math", None, 100_000, False),

        # MathQA
        ("math_qa", "mathqa", None, 200_000, False),

        # GSM8K full
        ("gsm8k", "gsm8k_full", "main", 100_000, False),

        # OpenMathInstruct
        ("nvidia/OpenMathInstruct-1", "openmathinstruct", None, 300_000, False),

        # PRM800K (reasoning)
        ("openai/prm800k", "prm800k", None, 200_000, False),

        # TheoremQA
        ("TIGER-Lab/TheoremQA", "theoremqa", None, 100_000, False),
    ]

    for dataset_info in datasets_to_download:
        if len(dataset_info) == 5:
            dataset_id, name, config, max_examples, trust_code = dataset_info
        else:
            dataset_id, name, config, max_examples = dataset_info
            trust_code = False

        try:
            print(f"\n[→] Downloading {name} from {dataset_id}...")
            ds = load_dataset(
                dataset_id,
                config,
                split="train",
                streaming=True,
                trust_remote_code=trust_code
            )
            output_file = output_dir / f"{name}.jsonl"
            count = 0

            with output_file.open("w", encoding="utf-8") as f:
                for example in tqdm(ds, total=max_examples, desc=name):
                    question = safe_get(example, "question",
                                       default=safe_get(example, "problem"))
                    answer = safe_get(example, "answer",
                                     default=safe_get(example, "solution"))

                    if question and answer:
                        # Add step-by-step prefix for math
                        if "step" not in str(answer).lower():
                            output = f"Let me solve this step by step:\n\n{answer}"
                        else:
                            output = str(answer)

                        normalized = {
                            "instruction": question,
                            "input": "",
                            "output": output,
                            "_source": name,
                            "_category": "math_reasoning"
                        }
                        f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                        count += 1

                    if count >= max_examples:
                        break

            print(f"[✓] Saved {count:,} examples to {output_file}")

        except Exception as e:
            print(f"[!] Failed to download {name}: {e}")


def download_mega_qa_knowledge():
    """Download massive QA & knowledge datasets (+1M)."""
    output_dir = Path("examples/datasets/expansion_phase3/mega_qa_knowledge")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_download = [
        # Natural Questions
        ("natural_questions", "natural_questions", "default", 300_000, False),

        # MS MARCO
        ("ms_marco", "ms_marco", "v2.1", 200_000, False),

        # HotpotQA
        ("hotpot_qa", "hotpotqa", "fullwiki", 200_000, False),

        # ELI5
        ("eli5", "eli5", None, 150_000, False),

        # Wiki QA
        ("wiki_qa", "wikiqa", None, 50_000, False),

        # SQuAD v2 (more)
        ("squad_v2", "squad_v2_extra", None, 100_000, False),
    ]

    for dataset_info in datasets_to_download:
        if len(dataset_info) == 5:
            dataset_id, name, config, max_examples, trust_code = dataset_info
        else:
            dataset_id, name, config, max_examples = dataset_info
            trust_code = False

        try:
            print(f"\n[→] Downloading {name} from {dataset_id}...")
            ds = load_dataset(
                dataset_id,
                config,
                split="train",
                streaming=True,
                trust_remote_code=trust_code
            )
            output_file = output_dir / f"{name}.jsonl"
            count = 0

            with output_file.open("w", encoding="utf-8") as f:
                for example in tqdm(ds, total=max_examples, desc=name):
                    question = safe_get(example, "question")
                    answer = safe_get(example, "answer",
                                     default=safe_get(example, "answers"))

                    if question and answer:
                        # Handle different answer formats
                        if isinstance(answer, dict):
                            answer = safe_get(answer, "text", default=str(answer))
                        elif isinstance(answer, list) and len(answer) > 0:
                            answer = answer[0] if isinstance(answer[0], str) else safe_get(answer[0], "text")

                        normalized = {
                            "instruction": question,
                            "input": safe_get(example, "context", default=""),
                            "output": str(answer),
                            "_source": name,
                            "_category": "qa_knowledge"
                        }
                        f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                        count += 1

                    if count >= max_examples:
                        break

            print(f"[✓] Saved {count:,} examples to {output_file}")

        except Exception as e:
            print(f"[!] Failed to download {name}: {e}")


def download_mega_conversation():
    """Download massive conversation datasets (+500k)."""
    output_dir = Path("examples/datasets/expansion_phase3/mega_conversation")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_download = [
        # Anthropic HH-RLHF (more)
        ("Anthropic/hh-rlhf", "hh_rlhf_extra", None, 200_000, False),

        # OpenAssistant conversations v2
        ("OpenAssistant/oasst2", "oasst2_extra", None, 100_000, False),

        # UltraChat 200k
        ("HuggingFaceH4/ultrachat_200k", "ultrachat_200k", None, 200_000, False),
    ]

    for dataset_info in datasets_to_download:
        if len(dataset_info) == 5:
            dataset_id, name, config, max_examples, trust_code = dataset_info
        else:
            dataset_id, name, config, max_examples = dataset_info
            trust_code = False

        try:
            print(f"\n[→] Downloading {name} from {dataset_id}...")
            ds = load_dataset(
                dataset_id,
                config,
                split="train",
                streaming=True,
                trust_remote_code=trust_code
            )
            output_file = output_dir / f"{name}.jsonl"
            count = 0

            with output_file.open("w", encoding="utf-8") as f:
                for example in tqdm(ds, total=max_examples, desc=name):
                    # Handle conversation formats
                    if "chosen" in example and "rejected" in example:
                        # HH-RLHF format
                        instruction = example.get("chosen", "")[:200]
                        output = example.get("chosen", "")
                    elif "messages" in example:
                        # UltraChat format
                        messages = example["messages"]
                        if len(messages) >= 2:
                            instruction = messages[0].get("content", "")
                            output = messages[1].get("content", "")
                        else:
                            continue
                    else:
                        continue

                    if instruction and output:
                        normalized = {
                            "instruction": instruction,
                            "input": "",
                            "output": output,
                            "_source": name,
                            "_category": "conversation"
                        }
                        f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                        count += 1

                    if count >= max_examples:
                        break

            print(f"[✓] Saved {count:,} examples to {output_file}")

        except Exception as e:
            print(f"[!] Failed to download {name}: {e}")


if __name__ == "__main__":
    print("=" * 80)
    print(" PHASE 3 MEGA EXPANSION: SCALING TO 10M EXAMPLES")
    print(" Target: +5.5M examples across all categories")
    print(" Current: ~4.6M → Target: ~10M")
    print("=" * 80)

    print("\n[1/5] Mega Code & Technical Datasets (+1.5M target)")
    download_mega_code_datasets()

    print("\n[2/5] Mega General Instruction Datasets (+1.5M target)")
    download_mega_instruction_datasets()

    print("\n[3/5] Mega Math & Reasoning Datasets (+1M target)")
    download_mega_math_reasoning()

    print("\n[4/5] Mega QA & Knowledge Datasets (+1M target)")
    download_mega_qa_knowledge()

    print("\n[5/5] Mega Conversation Datasets (+500k target)")
    download_mega_conversation()

    print("\n" + "=" * 80)
    print("[✓] PHASE 3 MEGA EXPANSION COMPLETE")
    print("=" * 80)
