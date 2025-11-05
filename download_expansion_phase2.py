#!/usr/bin/env python3
"""
Phase 2 Expansion: Fill persona gaps and reach 6-7M total examples.

Focus areas:
- Psychology & Emotional (empathetic counselor, therapeutic)
- Tool/API grounding (function calling, API orchestration)
- Multi-turn dialog (conversational depth)
- Adversarial & Moral (debate, ethical reasoning)
- Advanced reasoning (chain-of-thought, inner monologue)
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
        # 1. Mental Health Counseling
        ("Amod/mental_health_counseling_conversations", "mental_health_counseling", None, 50_000),

        # 2. Empathetic Dialogues
        ("empathetic_dialogues", "empathetic_dialogues", None, 25_000),

        # 3. Emotional Support
        ("emotional_support_conversations", "emotional_support", None, 10_000),

        # 4. Therapy conversations
        ("heliosbrahma/mental_health_chatbot_dataset", "mental_health_chatbot", None, 30_000),

        # 5. Counseling Q&A
        ("Amod/mental_health_FAQ", "mental_health_faq", None, 5_000),

        # 6. Depression & anxiety support
        ("sentiment140", "sentiment140", None, 50_000),

        # 7. Social skills & relationships
        ("AlekseyKorshuk/persona-chat", "persona_chat", None, 50_000),

        # 8. Emotional intelligence
        ("daily_dialog", "daily_dialog", None, 13_000),
    ]

    for dataset_id, name, config, max_examples in datasets_to_download:
        try:
            print(f"\n[→] Downloading {name} from {dataset_id}...")

            if name == "sentiment140":
                # Sentiment140 special handling
                ds = load_dataset(dataset_id, split="train", streaming=True)
                output_file = output_dir / f"{name}.jsonl"
                count = 0

                with output_file.open("w", encoding="utf-8") as f:
                    for example in tqdm(ds, total=max_examples, desc=name):
                        sentiment = safe_get(example, "sentiment")
                        text = safe_get(example, "text")

                        if text:
                            # Create empathetic response based on sentiment
                            if sentiment == 4:  # Positive
                                response_prefix = "I'm so glad to hear that! "
                            elif sentiment == 0:  # Negative
                                response_prefix = "I understand you're going through a difficult time. "
                            else:
                                response_prefix = ""

                            normalized = {
                                "instruction": f"Respond empathetically to: {text}",
                                "input": "",
                                "output": f"{response_prefix}It sounds like you're feeling {text}",
                                "_source": name,
                                "_category": "psychology_emotional",
                                "_persona": "empathetic_counselor"
                            }
                            f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                            count += 1

                        if count >= max_examples:
                            break

                print(f"[✓] Saved {count:,} examples to {output_file}")
                continue

            ds = load_dataset(dataset_id, config, split="train", streaming=True)
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
                                "_category": "psychology_emotional",
                                "_persona": "empathetic_counselor"
                            }

                    elif "Context" in example and "Response" in example:
                        # Mental health format
                        normalized = {
                            "instruction": example["Context"],
                            "input": "",
                            "output": example["Response"],
                            "_source": name,
                            "_category": "psychology_emotional",
                            "_persona": "empathetic_counselor"
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
                                "_category": "psychology_emotional",
                                "_persona": "conversational_agent"
                            }

                    elif "history" in example and "candidates" in example:
                        # Persona-chat format
                        history = example["history"]
                        candidates = example["candidates"]
                        if history and candidates:
                            normalized = {
                                "instruction": " ".join(history[-2:]) if len(history) >= 2 else history[-1],
                                "input": "",
                                "output": candidates[0] if isinstance(candidates, list) else str(candidates),
                                "_source": name,
                                "_category": "psychology_emotional",
                                "_persona": "conversational_agent"
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
        # 1. Berkeley function calling
        ("gorilla-llm/Berkeley-Function-Calling-Leaderboard", "berkeley_function", None, 50_000),

        # 2. ToolBench
        ("ToolBench/ToolBench", "toolbench", None, 50_000),

        # 3. Glaive code assistant (includes tools)
        ("glaiveai/glaive-code-assistant", "glaive_code_assistant", None, 50_000),

        # 4. API calls dataset
        ("NousResearch/hermes-function-calling-v1", "hermes_function", None, 50_000),
    ]

    for dataset_id, name, config, max_examples in datasets_to_download:
        try:
            print(f"\n[→] Downloading {name} from {dataset_id}...")
            ds = load_dataset(dataset_id, config, split="train", streaming=True, trust_remote_code=True)
            output_file = output_dir / f"{name}.jsonl"
            count = 0

            with output_file.open("w", encoding="utf-8") as f:
                for example in tqdm(ds, total=max_examples, desc=name):
                    instruction = safe_get(example, "instruction", default=safe_get(example, "question", default=safe_get(example, "prompt")))
                    output = safe_get(example, "output", default=safe_get(example, "answer", default=safe_get(example, "response")))

                    if instruction and output:
                        normalized = {
                            "instruction": instruction,
                            "input": safe_get(example, "input", default=""),
                            "output": output,
                            "_source": name,
                            "_category": "tool_api",
                            "_persona": "tool_orchestrator"
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
        # 1. WizardLM conversations
        ("WizardLM/WizardLM_evol_instruct_V2_196k", "wizardlm_conversations", None, 100_000),

        # 2. ShareGPT cleaned
        ("anon8231489123/ShareGPT_Vicuna_unfiltered", "sharegpt_cleaned", None, 50_000),

        # 3. OpenOrca-like multi-turn
        ("Open-Orca/OpenOrca", "open_orca_multiturn", None, 50_000),
    ]

    for dataset_id, name, config, max_examples in datasets_to_download:
        try:
            print(f"\n[→] Downloading {name} from {dataset_id}...")
            ds = load_dataset(dataset_id, config, split="train", streaming=True)
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
                                    "_persona": "conversational_agent",
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
                            "_category": "multiturn_dialog",
                            "_persona": "conversational_agent"
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
        # 1. ETHICS dataset
        ("hendrycks/ethics", "ethics_commonsense", "commonsense", 30_000),
        ("hendrycks/ethics", "ethics_virtue", "virtue", 30_000),
        ("hendrycks/ethics", "ethics_justice", "justice", 30_000),

        # 2. Moral stories
        ("demelin/moral_stories", "moral_stories", None, 30_000),

        # 3. Debate datasets
        ("Anthropic/persuasion", "persuasion", None, 30_000),
    ]

    for dataset_id, name, config, max_examples in datasets_to_download:
        try:
            print(f"\n[→] Downloading {name} from {dataset_id}...")
            ds = load_dataset(dataset_id, config, split="train", streaming=True)
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
                            "_category": "adversarial_moral",
                            "_persona": "critical_debater"
                        }
                        f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                        count += 1

                    elif "moral_action" in example and "immoral_action" in example:
                        # Moral stories format
                        norm = safe_get(example, "norm")
                        moral = safe_get(example, "moral_action")
                        immoral = safe_get(example, "immoral_action")

                        if norm and moral:
                            normalized = {
                                "instruction": f"Explain why this is ethical: {moral}",
                                "input": f"Context: {norm}",
                                "output": f"This action aligns with the principle that {norm}. By {moral}, we uphold this ethical standard.",
                                "_source": name,
                                "_category": "adversarial_moral",
                                "_persona": "critical_debater"
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
        # 1. Complex CoT
        ("kaist-ai/CoT-Collection", "cot_complex", None, 100_000),

        # 2. Causal reasoning
        ("causalnlp/corr2cause", "causal_reasoning", None, 30_000),

        # 3. MMLU with reasoning
        ("cais/mmlu", "mmlu_all", "all", 50_000),

        # 4. ARC challenge
        ("ai2_arc", "arc_challenge", "ARC-Challenge", 20_000),
    ]

    for dataset_id, name, config, max_examples in datasets_to_download:
        try:
            print(f"\n[→] Downloading {name} from {dataset_id}...")
            ds = load_dataset(dataset_id, config, split="train", streaming=True)
            output_file = output_dir / f"{name}.jsonl"
            count = 0

            with output_file.open("w", encoding="utf-8") as f:
                for example in tqdm(ds, total=max_examples, desc=name):
                    if "question" in example:
                        question = safe_get(example, "question")
                        answer = safe_get(example, "answer", default=safe_get(example, "choices"))

                        if question and answer:
                            # Add reasoning prefix
                            output = f"Let me think through this step by step:\n\n{answer}"

                            normalized = {
                                "instruction": question,
                                "input": "",
                                "output": output,
                                "_source": name,
                                "_category": "reasoning_trace",
                                "_persona": "analytical_reasoner"
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
    print(" PHASE 2 EXPANSION: FILLING PERSONA GAPS")
    print(" Target: +1-1.5M additional examples")
    print("=" * 80)

    print("\n[1/5] Psychology & Emotional Datasets (+300k target)")
    download_psychology_emotional()

    print("\n[2/5] Advanced Tool/API Datasets (+200k target)")
    download_tool_api_advanced()

    print("\n[3/5] Advanced Multi-turn Dialog (+200k target)")
    download_multiturn_advanced()

    print("\n[4/5] Adversarial & Moral Dilemmas (+150k target)")
    download_adversarial_moral()

    print("\n[5/5] Advanced Reasoning Traces (+200k target)")
    download_advanced_reasoning()

    print("\n" + "=" * 80)
    print("[✓] PHASE 2 DOWNLOADS COMPLETE")
    print("=" * 80)
