#!/usr/bin/env python3
"""
Phase 2 Expansion (Fixed): Fill diversity gaps and reach 6-7M total examples.

Focus areas:
- Psychology & Emotional (empathetic, therapeutic)
- Tool/API grounding (function calling, API orchestration)
- Multi-turn dialog (conversational depth)
- Adversarial & Moral (debate, ethical reasoning)
- Advanced reasoning (chain-of-thought, inner monologue)

NOTE: No explicit persona control tokens - emergent personality only.
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


def download_psychology_emotional():
    """Download psychology & emotional introspection datasets (+300k)."""
    output_dir = Path("examples/datasets/expansion_phase2/psychology_emotional")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_download = [
        # 1. Empathetic Dialogues (FIXED: added trust_remote_code)
        ("empathetic_dialogues", "empathetic_dialogues", None, 25_000, True),

        # 2. Daily Dialog (FIXED: added trust_remote_code)
        ("daily_dialog", "daily_dialog", None, 13_000, True),

        # 3. Counseling conversations
        ("Amod/mental_health_counseling_conversations", "mental_health_counseling", None, 50_000, False),

        # 4. ProsocialDialog (alternative to emotional_support)
        ("allenai/prosocial-dialog", "prosocial_dialog", None, 50_000, False),

        # 5. Empathy mental health (alternative)
        ("mrm8488/mental-health-conversational-data", "mental_health_conv", None, 10_000, False),

        # 6. Therapeutic conversations
        ("Amod/mental_health_counseling_conversations", "therapy_conv", None, 30_000, False),
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
                    normalized = None

                    # Handle different formats
                    if "context" in example or "utterance" in example:
                        # Empathetic dialogues format
                        context = safe_get(example, "context", default=safe_get(example, "prompt"))
                        utterance = safe_get(example, "utterance", default=safe_get(example, "response"))

                        if context and utterance:
                            normalized = {
                                "instruction": context,
                                "input": "",
                                "output": utterance,
                                "_source": name,
                                "_category": "psychology_emotional"
                            }

                    elif "Context" in example and "Response" in example:
                        # Mental health format
                        normalized = {
                            "instruction": example["Context"],
                            "input": "",
                            "output": example["Response"],
                            "_source": name,
                            "_category": "psychology_emotional"
                        }

                    elif "dialog" in example:
                        # Daily dialog format
                        dialog = example["dialog"]
                        if len(dialog) >= 2:
                            normalized = {
                                "instruction": dialog[0],
                                "input": "",
                                "output": dialog[1],
                                "_source": name,
                                "_category": "psychology_emotional"
                            }

                    elif "prompt" in example and "response" in example:
                        # Prosocial dialog format
                        normalized = {
                            "instruction": safe_get(example, "prompt"),
                            "input": safe_get(example, "context", default=""),
                            "output": safe_get(example, "response"),
                            "_source": name,
                            "_category": "psychology_emotional"
                        }

                    if normalized:
                        f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                        count += 1

                    if count >= max_examples:
                        break

            print(f"[✓] Saved {count:,} examples to {output_file}")

        except Exception as e:
            print(f"[!] Failed to download {name}: {e}")


def download_tool_api_advanced():
    """Download advanced tool & API datasets (+200k)."""
    output_dir = Path("examples/datasets/expansion_phase2/tool_api_advanced")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_download = [
        # 1. Glaive code assistant (already worked)
        ("glaiveai/glaive-code-assistant", "glaive_code_assistant_v2", None, 50_000, True),

        # 2. xlam function calling (alternative to Berkeley)
        ("Salesforce/xlam-function-calling-60k", "xlam_function", None, 60_000, False),

        # 3. Gorilla API Bench
        ("gorilla-llm/APIBench", "gorilla_api", None, 50_000, True),

        # 4. Glaive function calling v2
        ("glaiveai/glaive-function-calling-v2", "glaive_function_v2", None, 40_000, False),
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
                                          default=safe_get(example, "question",
                                          default=safe_get(example, "prompt")))
                    output = safe_get(example, "output",
                                     default=safe_get(example, "answer",
                                     default=safe_get(example, "response")))

                    if instruction and output:
                        normalized = {
                            "instruction": instruction,
                            "input": safe_get(example, "input", default=""),
                            "output": output,
                            "_source": name,
                            "_category": "tool_api"
                        }
                        f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                        count += 1

                    if count >= max_examples:
                        break

            print(f"[✓] Saved {count:,} examples to {output_file}")

        except Exception as e:
            print(f"[!] Failed to download {name}: {e}")


def download_multiturn_advanced():
    """Download more multi-turn dialog datasets (+200k)."""
    output_dir = Path("examples/datasets/expansion_phase2/multiturn_advanced")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_download = [
        # Already successful
        ("WizardLM/WizardLM_evol_instruct_V2_196k", "wizardlm_v2", None, 100_000, False),
        ("Open-Orca/OpenOrca", "open_orca_v2", None, 100_000, False),

        # New additions
        ("lmsys/lmsys-chat-1m", "lmsys_chat", None, 100_000, False),
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
                    # Try different conversation formats
                    if "conversations" in example:
                        convs = example["conversations"]
                        if isinstance(convs, list) and len(convs) >= 2:
                            instruction = convs[0].get("value", "") if isinstance(convs[0], dict) else str(convs[0])
                            output = convs[1].get("value", "") if isinstance(convs[1], dict) else str(convs[1])

                            if instruction and output:
                                normalized = {
                                    "instruction": instruction,
                                    "input": "",
                                    "output": output,
                                    "_source": name,
                                    "_category": "multiturn_dialog",
                                    "_turns": len(convs)
                                }
                                f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                                count += 1

                    elif "question" in example and "response" in example:
                        normalized = {
                            "instruction": safe_get(example, "question"),
                            "input": safe_get(example, "system_prompt", default=""),
                            "output": safe_get(example, "response"),
                            "_source": name,
                            "_category": "multiturn_dialog"
                        }
                        f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                        count += 1

                    if count >= max_examples:
                        break

            print(f"[✓] Saved {count:,} examples to {output_file}")

        except Exception as e:
            print(f"[!] Failed to download {name}: {e}")


def download_adversarial_moral():
    """Download adversarial & moral dilemma datasets (+150k)."""
    output_dir = Path("examples/datasets/expansion_phase2/adversarial_moral")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_download = [
        # ETHICS (FIXED: use specific configs that worked)
        ("hendrycks/ethics", "ethics_commonsense_v2", "commonsense", 30_000, False),
        ("hendrycks/ethics", "ethics_utilitarianism", "utilitarianism", 30_000, False),
        ("hendrycks/ethics", "ethics_deontology", "deontology", 30_000, False),

        # Moral stories (FIXED: use specific config)
        ("demelin/moral_stories", "moral_stories_full", "full", 30_000, False),

        # Debate datasets
        ("Anthropic/hh-rlhf", "hh_rlhf_debate", None, 30_000, False),
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
                    if "input" in example and "label" in example:
                        # ETHICS format
                        normalized = {
                            "instruction": f"Evaluate the ethical implications: {example['input']}",
                            "input": "",
                            "output": f"Analysis: {example['label']}",
                            "_source": name,
                            "_category": "adversarial_moral"
                        }
                        f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                        count += 1

                    elif "moral_action" in example and "norm" in example:
                        # Moral stories format
                        norm = safe_get(example, "norm")
                        moral = safe_get(example, "moral_action")

                        if norm and moral:
                            normalized = {
                                "instruction": f"Explain why this is ethical: {moral}",
                                "input": f"Context: {norm}",
                                "output": f"This action aligns with the principle that {norm}. By {moral}, we uphold this ethical standard.",
                                "_source": name,
                                "_category": "adversarial_moral"
                            }
                            f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                            count += 1

                    elif "chosen" in example and "rejected" in example:
                        # HH-RLHF debate format
                        normalized = {
                            "instruction": safe_get(example, "prompt", default=example.get("chosen", "")[:200]),
                            "input": "",
                            "output": safe_get(example, "chosen"),
                            "_source": name,
                            "_category": "adversarial_moral"
                        }
                        f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                        count += 1

                    if count >= max_examples:
                        break

            print(f"[✓] Saved {count:,} examples to {output_file}")

        except Exception as e:
            print(f"[!] Failed to download {name}: {e}")


def download_advanced_reasoning():
    """Download advanced reasoning trace datasets (+200k)."""
    output_dir = Path("examples/datasets/expansion_phase2/advanced_reasoning")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_download = [
        # CoT Collection (FIXED: added trust_remote_code)
        ("kaist-ai/CoT-Collection", "cot_collection", None, 100_000, True),

        # MMLU (FIXED: use correct split)
        ("cais/mmlu", "mmlu_reasoning", "all", 50_000, False, "test"),

        # ARC Challenge
        ("ai2_arc", "arc_challenge_v2", "ARC-Challenge", 20_000, False),

        # Chain-of-thought hub
        ("QingyiSi/Alpaca-CoT", "alpaca_cot", None, 30_000, False),
    ]

    for dataset_info in datasets_to_download:
        trust_code = False
        custom_split = "train"

        if len(dataset_info) == 6:
            dataset_id, name, config, max_examples, trust_code, custom_split = dataset_info
        elif len(dataset_info) == 5:
            dataset_id, name, config, max_examples, trust_code = dataset_info
        else:
            dataset_id, name, config, max_examples = dataset_info

        try:
            print(f"\n[→] Downloading {name} from {dataset_id}...")
            ds = load_dataset(
                dataset_id,
                config,
                split=custom_split,
                streaming=True,
                trust_remote_code=trust_code
            )
            output_file = output_dir / f"{name}.jsonl"
            count = 0

            with output_file.open("w", encoding="utf-8") as f:
                for example in tqdm(ds, total=max_examples, desc=name):
                    if "question" in example:
                        question = safe_get(example, "question")
                        answer = safe_get(example, "answer",
                                         default=safe_get(example, "choices",
                                         default=safe_get(example, "output")))

                        if question and answer:
                            # Add reasoning prefix for CoT
                            if "cot" in name.lower() or "reasoning" in name.lower():
                                output = f"Let me think through this step by step:\n\n{answer}"
                            else:
                                output = str(answer)

                            normalized = {
                                "instruction": question,
                                "input": "",
                                "output": output,
                                "_source": name,
                                "_category": "reasoning_trace"
                            }
                            f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                            count += 1

                    elif "instruction" in example and "output" in example:
                        normalized = {
                            "instruction": safe_get(example, "instruction"),
                            "input": safe_get(example, "input", default=""),
                            "output": safe_get(example, "output"),
                            "_source": name,
                            "_category": "reasoning_trace"
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
    print(" PHASE 2 EXPANSION (FIXED): FILLING DIVERSITY GAPS")
    print(" Target: +1-1.5M additional examples")
    print(" NOTE: No persona control tokens - emergent personality only")
    print("=" * 80)

    print("\n[1/5] Psychology & Emotional Datasets (+178k target)")
    download_psychology_emotional()

    print("\n[2/5] Advanced Tool/API Datasets (+200k target)")
    download_tool_api_advanced()

    print("\n[3/5] Advanced Multi-turn Dialog (+300k target)")
    download_multiturn_advanced()

    print("\n[4/5] Adversarial & Moral Dilemmas (+150k target)")
    download_adversarial_moral()

    print("\n[5/5] Advanced Reasoning Traces (+200k target)")
    download_advanced_reasoning()

    print("\n" + "=" * 80)
    print("[✓] PHASE 2 DOWNLOADS COMPLETE (FIXED)")
    print("=" * 80)
