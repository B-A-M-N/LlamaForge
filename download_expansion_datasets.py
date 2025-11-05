#!/usr/bin/env python3
"""
Download expansion datasets to diversify training corpus.

Categories aligned with the pipeline outline:
- Multi-turn dialog
- Reasoning traces & inner-monologue
- Psychology & emotional introspection
- Creative narrative & metaphorical writing
- Code debugging & reasoning
- Tool & API grounding
- Factual grounding & retrieval
- Adversarial & moral dilemmas
"""

import json
import os
from pathlib import Path
from datasets import load_dataset
from tqdm import tqdm


def normalize_to_alpaca(example, dataset_name):
    """Normalize various dataset formats to Alpaca instruction format."""
    normalized = {
        "instruction": "",
        "input": "",
        "output": "",
        "_source": dataset_name,
        "_category": ""
    }
    return normalized


def download_multiturn_dialog():
    """Download multi-turn conversation datasets (+400k target)."""
    output_dir = Path("examples/datasets/expansion/multiturn_dialog")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_download = [
        # ShareGPT-style multi-turn conversations
        ("anon8231489123/ShareGPT_Vicuna_unfiltered", "sharegpt_vicuna", None, 200_000),

        # OpenAssistant conversations (multi-turn)
        ("OpenAssistant/oasst2", "oasst2", None, 100_000),

        # Anthropic HH-RLHF (helpful/harmless multi-turn)
        ("Anthropic/hh-rlhf", "hh_rlhf", None, 150_000),

        # UltraChat (large-scale multi-turn)
        ("stingning/ultrachat", "ultrachat", None, 200_000),

        # Wizard-Vicuna conversations
        ("cognitivecomputations/wizard-vicuna-13b-uncensored", "wizard_vicuna", None, 50_000),
    ]

    for dataset_id, name, config, max_examples in datasets_to_download:
        try:
            print(f"\n[→] Downloading {name} from {dataset_id}...")
            ds = load_dataset(dataset_id, config, split="train", streaming=True)

            output_file = output_dir / f"{name}.jsonl"
            count = 0

            with output_file.open("w", encoding="utf-8") as f:
                for example in tqdm(ds, total=max_examples, desc=name):
                    # Convert to Alpaca format
                    if "conversations" in example:
                        # ShareGPT format
                        convs = example["conversations"]
                        if len(convs) >= 2:
                            instruction = convs[0].get("value", "")
                            output = convs[1].get("value", "")
                            normalized = {
                                "instruction": instruction,
                                "input": "",
                                "output": output,
                                "_source": name,
                                "_category": "multiturn_dialog",
                                "_turns": len(convs)
                            }
                    elif "chosen" in example and "rejected" in example:
                        # HH-RLHF format
                        chosen = example["chosen"]
                        # Parse conversation
                        parts = chosen.split("\n\nAssistant:")
                        if len(parts) >= 2:
                            instruction = parts[0].replace("Human:", "").strip()
                            output = parts[1].strip()
                            normalized = {
                                "instruction": instruction,
                                "input": "",
                                "output": output,
                                "_source": name,
                                "_category": "multiturn_dialog"
                            }
                    elif "messages" in example:
                        # OpenAssistant format
                        msgs = example["messages"]
                        if len(msgs) >= 2:
                            instruction = msgs[0].get("content", "")
                            output = msgs[1].get("content", "")
                            normalized = {
                                "instruction": instruction,
                                "input": "",
                                "output": output,
                                "_source": name,
                                "_category": "multiturn_dialog",
                                "_turns": len(msgs)
                            }
                    else:
                        continue

                    f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                    count += 1

                    if count >= max_examples:
                        break

            print(f"[✓] Saved {count:,} examples to {output_file}")

        except Exception as e:
            print(f"[!] Failed to download {name}: {e}")


def download_reasoning_traces():
    """Download reasoning trace & inner-monologue datasets (+300k target)."""
    output_dir = Path("examples/datasets/expansion/reasoning_traces")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_download = [
        # Chain-of-thought reasoning
        ("kaist-ai/CoT-Collection", "cot_collection", None, 100_000),

        # OpenAI grade-school math with solutions
        ("openai/gsm8k", "gsm8k_full", "main", 20_000),

        # Math reasoning traces
        ("TIGER-Lab/MathInstruct", "math_instruct", None, 100_000),

        # Reasoning dataset with step-by-step
        ("causalnlp/corr2cause", "corr2cause", None, 30_000),

        # DeepMind mathematics dataset
        ("deepmind/math_dataset", "math_dataset", "algebra__linear_1d", 50_000),

        # ReClor (logical reasoning)
        ("lucasmccabe/reclor", "reclor", None, 10_000),
    ]

    for dataset_id, name, config, max_examples in datasets_to_download:
        try:
            print(f"\n[→] Downloading {name} from {dataset_id}...")
            ds = load_dataset(dataset_id, config, split="train", streaming=True)

            output_file = output_dir / f"{name}.jsonl"
            count = 0

            with output_file.open("w", encoding="utf-8") as f:
                for example in tqdm(ds, total=max_examples, desc=name):
                    normalized = {}

                    if "question" in example and "answer" in example:
                        instruction = example["question"]
                        output = example["answer"]
                        if "solution" in example:
                            output = f"Let me think through this step by step:\n\n{example['solution']}\n\nAnswer: {output}"
                        normalized = {
                            "instruction": instruction,
                            "input": "",
                            "output": output,
                            "_source": name,
                            "_category": "reasoning_trace"
                        }
                    elif "problem" in example and "solution" in example:
                        normalized = {
                            "instruction": example["problem"],
                            "input": "",
                            "output": example["solution"],
                            "_source": name,
                            "_category": "reasoning_trace"
                        }
                    else:
                        continue

                    if normalized:
                        f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                        count += 1

                    if count >= max_examples:
                        break

            print(f"[✓] Saved {count:,} examples to {output_file}")

        except Exception as e:
            print(f"[!] Failed to download {name}: {e}")


def download_psychology_emotional():
    """Download psychology & emotional introspection datasets (+300k target)."""
    output_dir = Path("examples/datasets/expansion/psychology_emotional")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_download = [
        # Therapeutic conversations
        ("Amod/mental_health_counseling_conversations", "mental_health_counseling", None, 100_000),

        # Emotional support conversations
        ("emotional_support_conversations", "emotional_support", None, 50_000),

        # Empathetic dialogues
        ("empathetic_dialogues", "empathetic_dialogues", None, 50_000),

        # PsychQA
        ("abacusai/PsychQA", "psych_qa", None, 50_000),

        # Mental health FAQ
        ("Amod/mental_health_FAQ", "mental_health_faq", None, 20_000),
    ]

    for dataset_id, name, config, max_examples in datasets_to_download:
        try:
            print(f"\n[→] Downloading {name} from {dataset_id}...")
            ds = load_dataset(dataset_id, config, split="train", streaming=True)

            output_file = output_dir / f"{name}.jsonl"
            count = 0

            with output_file.open("w", encoding="utf-8") as f:
                for example in tqdm(ds, total=max_examples, desc=name):
                    # Various formats for psychology/therapy datasets
                    if "Context" in example and "Response" in example:
                        normalized = {
                            "instruction": example["Context"],
                            "input": "",
                            "output": example["Response"],
                            "_source": name,
                            "_category": "psychology_emotional"
                        }
                    elif "prompt" in example and "response" in example:
                        normalized = {
                            "instruction": example["prompt"],
                            "input": "",
                            "output": example["response"],
                            "_source": name,
                            "_category": "psychology_emotional"
                        }
                    elif "utterance" in example and "context" in example:
                        normalized = {
                            "instruction": example["context"],
                            "input": "",
                            "output": example["utterance"],
                            "_source": name,
                            "_category": "psychology_emotional"
                        }
                    else:
                        continue

                    f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                    count += 1

                    if count >= max_examples:
                        break

            print(f"[✓] Saved {count:,} examples to {output_file}")

        except Exception as e:
            print(f"[!] Failed to download {name}: {e}")


def download_creative_narrative():
    """Download creative narrative & metaphorical writing datasets (+200k target)."""
    output_dir = Path("examples/datasets/expansion/creative_narrative")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_download = [
        # WritingPrompts
        ("euclaise/writingprompts", "writing_prompts", None, 100_000),

        # TinyStories
        ("roneneldan/TinyStories", "tiny_stories", None, 50_000),

        # Story generation
        ("HuggingFaceH4/story_generation", "story_generation", None, 30_000),

        # Fictional conversations
        ("Isotonic/fictional_fineweb", "fictional_fineweb", None, 20_000),
    ]

    for dataset_id, name, config, max_examples in datasets_to_download:
        try:
            print(f"\n[→] Downloading {name} from {dataset_id}...")
            ds = load_dataset(dataset_id, config, split="train", streaming=True)

            output_file = output_dir / f"{name}.jsonl"
            count = 0

            with output_file.open("w", encoding="utf-8") as f:
                for example in tqdm(ds, total=max_examples, desc=name):
                    if "prompt" in example and "story" in example:
                        normalized = {
                            "instruction": example["prompt"],
                            "input": "",
                            "output": example["story"],
                            "_source": name,
                            "_category": "creative_narrative"
                        }
                    elif "instruction" in example and "response" in example:
                        normalized = {
                            "instruction": example["instruction"],
                            "input": "",
                            "output": example["response"],
                            "_source": name,
                            "_category": "creative_narrative"
                        }
                    elif "text" in example:
                        # For story datasets without explicit instruction
                        text = example["text"]
                        if len(text) > 100:  # Filter short texts
                            normalized = {
                                "instruction": "Write a creative story.",
                                "input": "",
                                "output": text[:2000],  # Limit length
                                "_source": name,
                                "_category": "creative_narrative"
                            }
                    else:
                        continue

                    f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                    count += 1

                    if count >= max_examples:
                        break

            print(f"[✓] Saved {count:,} examples to {output_file}")

        except Exception as e:
            print(f"[!] Failed to download {name}: {e}")


def download_code_debugging():
    """Download code debugging & reasoning datasets (+200k target)."""
    output_dir = Path("examples/datasets/expansion/code_debugging")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_download = [
        # Code Alpaca
        ("sahil2801/CodeAlpaca-20k", "code_alpaca_20k", None, 20_000),

        # Code contests
        ("deepmind/code_contests", "code_contests", None, 30_000),

        # Apps (coding problems)
        ("codeparrot/apps", "apps", "train", 50_000),

        # HumanEval-X (multilingual code)
        ("THUDM/humaneval-x", "humaneval_x", None, 10_000),

        # CodeSearchNet
        ("code_search_net", "codesearchnet", "python", 50_000),

        # Stack Overflow
        ("pacovaldez/stackoverflow-questions", "stackoverflow", None, 40_000),
    ]

    for dataset_id, name, config, max_examples in datasets_to_download:
        try:
            print(f"\n[→] Downloading {name} from {dataset_id}...")
            ds = load_dataset(dataset_id, config, split="train", streaming=True)

            output_file = output_dir / f"{name}.jsonl"
            count = 0

            with output_file.open("w", encoding="utf-8") as f:
                for example in tqdm(ds, total=max_examples, desc=name):
                    if "instruction" in example and "output" in example:
                        normalized = {
                            "instruction": example["instruction"],
                            "input": example.get("input", ""),
                            "output": example["output"],
                            "_source": name,
                            "_category": "code_debugging"
                        }
                    elif "question" in example and "solutions" in example:
                        normalized = {
                            "instruction": example["question"],
                            "input": "",
                            "output": example["solutions"],
                            "_source": name,
                            "_category": "code_debugging"
                        }
                    elif "func_documentation_string" in example and "func_code_string" in example:
                        normalized = {
                            "instruction": f"Write a Python function that: {example['func_documentation_string']}",
                            "input": "",
                            "output": example["func_code_string"],
                            "_source": name,
                            "_category": "code_debugging"
                        }
                    else:
                        continue

                    f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                    count += 1

                    if count >= max_examples:
                        break

            print(f"[✓] Saved {count:,} examples to {output_file}")

        except Exception as e:
            print(f"[!] Failed to download {name}: {e}")


def download_tool_api():
    """Download tool & API grounding datasets (+100k target)."""
    output_dir = Path("examples/datasets/expansion/tool_api")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_download = [
        # ToolBench
        ("Salesforce/xlam-function-calling-60k", "xlam_function_calling", None, 60_000),

        # API Bank
        ("APIBank/APIBank", "api_bank", None, 20_000),

        # RestBench
        ("Salesforce/restbench", "restbench", None, 10_000),

        # Glaive function calling (if not already downloaded)
        ("glaiveai/glaive-function-calling-v2", "glaive_v2", None, 20_000),
    ]

    for dataset_id, name, config, max_examples in datasets_to_download:
        try:
            print(f"\n[→] Downloading {name} from {dataset_id}...")
            ds = load_dataset(dataset_id, config, split="train", streaming=True)

            output_file = output_dir / f"{name}.jsonl"
            count = 0

            with output_file.open("w", encoding="utf-8") as f:
                for example in tqdm(ds, total=max_examples, desc=name):
                    if "instruction" in example and "output" in example:
                        normalized = {
                            "instruction": example["instruction"],
                            "input": example.get("input", ""),
                            "output": example["output"],
                            "_source": name,
                            "_category": "tool_api"
                        }
                    elif "query" in example and "answers" in example:
                        normalized = {
                            "instruction": example["query"],
                            "input": "",
                            "output": str(example["answers"]),
                            "_source": name,
                            "_category": "tool_api"
                        }
                    else:
                        continue

                    f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                    count += 1

                    if count >= max_examples:
                        break

            print(f"[✓] Saved {count:,} examples to {output_file}")

        except Exception as e:
            print(f"[!] Failed to download {name}: {e}")


def download_factual_grounding():
    """Download factual grounding & retrieval datasets (+100k target)."""
    output_dir = Path("examples/datasets/expansion/factual_grounding")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_download = [
        # Natural Questions
        ("natural_questions", "natural_questions", "default", 50_000),

        # TriviaQA
        ("trivia_qa", "trivia_qa", "rc.nocontext", 30_000),

        # SQuAD
        ("squad_v2", "squad_v2", None, 20_000),

        # HotpotQA
        ("hotpot_qa", "hotpot_qa", "fullwiki", 20_000),

        # ELI5 (Explain Like I'm 5)
        ("eli5", "eli5", None, 30_000),
    ]

    for dataset_id, name, config, max_examples in datasets_to_download:
        try:
            print(f"\n[→] Downloading {name} from {dataset_id}...")
            ds = load_dataset(dataset_id, config, split="train", streaming=True)

            output_file = output_dir / f"{name}.jsonl"
            count = 0

            with output_file.open("w", encoding="utf-8") as f:
                for example in tqdm(ds, total=max_examples, desc=name):
                    if "question" in example and "answers" in example:
                        answers = example["answers"]
                        if isinstance(answers, dict) and "text" in answers:
                            answer = answers["text"][0] if answers["text"] else ""
                        else:
                            answer = str(answers)

                        normalized = {
                            "instruction": example["question"],
                            "input": example.get("context", ""),
                            "output": answer,
                            "_source": name,
                            "_category": "factual_grounding"
                        }
                    else:
                        continue

                    if answer:  # Only save if we have an answer
                        f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                        count += 1

                    if count >= max_examples:
                        break

            print(f"[✓] Saved {count:,} examples to {output_file}")

        except Exception as e:
            print(f"[!] Failed to download {name}: {e}")


def download_adversarial_moral():
    """Download adversarial & moral dilemma datasets (+100k target)."""
    output_dir = Path("examples/datasets/expansion/adversarial_moral")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_download = [
        # Anthropic red-teaming
        ("Anthropic/hh-rlhf", "hh_rlhf_red", "red-team-attempts", 50_000),

        # ToxiGen
        ("toxigen/toxigen-data", "toxigen", None, 20_000),

        # ETHICS
        ("hendrycks/ethics", "ethics", "commonsense", 15_000),

        # Moral stories
        ("demelin/moral_stories", "moral_stories", None, 15_000),
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
                        normalized = {
                            "instruction": example["input"],
                            "input": "",
                            "output": str(example["label"]),
                            "_source": name,
                            "_category": "adversarial_moral"
                        }
                    elif "chosen" in example:
                        # HH-RLHF format
                        text = example["chosen"]
                        if "Human:" in text and "Assistant:" in text:
                            parts = text.split("Assistant:")
                            if len(parts) >= 2:
                                normalized = {
                                    "instruction": parts[0].replace("Human:", "").strip(),
                                    "input": "",
                                    "output": parts[1].strip(),
                                    "_source": name,
                                    "_category": "adversarial_moral"
                                }
                    else:
                        continue

                    f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                    count += 1

                    if count >= max_examples:
                        break

            print(f"[✓] Saved {count:,} examples to {output_file}")

        except Exception as e:
            print(f"[!] Failed to download {name}: {e}")


if __name__ == "__main__":
    print("=" * 80)
    print(" EXPANSION DATASET DOWNLOADER")
    print(" Downloading diverse datasets to fill pipeline gaps")
    print("=" * 80)

    # Download all categories
    print("\n[1/8] Multi-turn Dialog Datasets")
    download_multiturn_dialog()

    print("\n[2/8] Reasoning Trace & Inner-Monologue Datasets")
    download_reasoning_traces()

    print("\n[3/8] Psychology & Emotional Introspection Datasets")
    download_psychology_emotional()

    print("\n[4/8] Creative Narrative & Metaphorical Writing Datasets")
    download_creative_narrative()

    print("\n[5/8] Code Debugging & Reasoning Datasets")
    download_code_debugging()

    print("\n[6/8] Tool & API Grounding Datasets")
    download_tool_api()

    print("\n[7/8] Factual Grounding & Retrieval Datasets")
    download_factual_grounding()

    print("\n[8/8] Adversarial & Moral Dilemma Datasets")
    download_adversarial_moral()

    print("\n" + "=" * 80)
    print("[✓] ALL DOWNLOADS COMPLETE")
    print("=" * 80)
