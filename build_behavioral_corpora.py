#!/usr/bin/env python3
"""
Behavioral Corpus Builder

Creates balanced, deduplicated training corpora for different assistant profiles
using the datasets shipped with LlamaForge.

Profiles supported out of the box:
    - claude_behavior       (Anthropic-style helpful/harmless/honest mix)
    - chatgpt_behavior      (OpenAI-style instruction following and tool use)
    - deepseek_search       (DeepSeek-style search-first, tool-driven reasoning)
    - code_debugging        (Open-source coding, debugging, and review mix)
    - esoteric_studies      (Occult / hermetic / contemplative writings)

Usage:
    python build_behavioral_corpora.py --profile claude_behavior \
        --output examples/datasets/claude_behavioral_mix.jsonl \
        --max-total 1200000 \
        --global-cache manifests/global_seen_hashes.json

    python build_behavioral_corpora.py --profile chatgpt_behavior \
        --output examples/datasets/chatgpt_behavioral_mix.jsonl \
        --max-total 1200000 \
        --global-cache manifests/global_seen_hashes.json

The script:
    1. Reads the configured dataset sources for the chosen profile
    2. Deduplicates by (instruction, input, output) triple
    3. Classifies each example into a capability bucket
    4. Samples per-bucket data according to the profile weights
    5. Writes a shuffled JSONL file and prints a coverage summary
"""

from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict, Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


@dataclass
class SourceConfig:
    path: Path
    label: str
    bucket: str = "auto"
    max_examples: Optional[int] = None
    priority: int = 0  # higher priority wins when trimming/upsampling


# Shared bucket weights (default production mix)
DEFAULT_BUCKET_WEIGHTS = {
    "instruction": 0.25,
    "tool_use": 0.15,
    "code": 0.20,
    "cot_math": 0.15,
    "analytical": 0.10,
    "creative": 0.07,
    "factual": 0.03,
    "red_team": 0.05,
}


def repo_path(*parts: str) -> Path:
    """Return a path relative to the repository root."""
    return Path(__file__).parent.joinpath(*parts).resolve()


PROFILE_CONFIGS: Dict[str, Dict] = {
    "claude_behavior": {
        "description": "Balanced Claude-style helpful/harmless/honest corpus.",
        "weights": {
            "instruction": 0.45,
            "code": 0.22,
            "red_team": 0.12,
            "creative": 0.08,
            "tool_use": 0.05,
            "analytical": 0.05,
            "factual": 0.02,
            "cot_math": 0.01,
        },
        "sources": [
            # Core instruction + mixed reasoning
            SourceConfig(
                path=repo_path("examples/datasets/claude_reasoning_ultimate_1.4M.jsonl"),
                label="claude_reasoning_ultimate",
                max_examples=800_000,
            ),
            # Tool use / function calling traces
            SourceConfig(
                path=repo_path("examples/datasets/glaive_function_calling.jsonl"),
                label="glaive_function_calling",
                bucket="tool_use",
            ),
            # Chain-of-thought math & reasoning
            SourceConfig(
                path=repo_path("examples/datasets/gsm8k_cot.jsonl"),
                label="gsm8k_cot",
                bucket="cot_math",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/orca_math_cot.jsonl"),
                label="orca_math_cot",
                bucket="cot_math",
            ),
            # Creative writing / persona
            SourceConfig(
                path=repo_path("examples/datasets/creative_writing.jsonl"),
                label="creative_writing",
                bucket="creative",
            ),
            # Safety refusals & red-team handling
            SourceConfig(
                path=repo_path("examples/datasets/red_team_safe.jsonl"),
                label="red_team_safe",
                bucket="red_team",
            ),
            # Code specific corpora
            SourceConfig(
                path=repo_path("examples/datasets/code_alpaca_full.jsonl"),
                label="code_alpaca_full",
                bucket="code",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/code_feedback_50k.jsonl"),
                label="code_feedback_50k",
                bucket="code",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/python_code_18k.jsonl"),
                label="python_code_18k",
                bucket="code",
            ),
            SourceConfig(
                path=repo_path("data/external/claude/*.jsonl"),
                label="claude_external",
            ),
            # Analytical / longer form reasoning
            SourceConfig(
                path=repo_path("examples/datasets/wizardlm_evol.jsonl"),
                label="wizardlm_evol",
                bucket="analytical",
                max_examples=60_000,
            ),
            # Additional unique material from duplication mix
            SourceConfig(
                path=repo_path("examples/datasets/ultimate_3M_intelligently_duplicated.jsonl"),
                label="ultimate_3m_mix",
                max_examples=700_000,
            ),
            # EXPANSION DATASETS - Multi-turn dialog
            SourceConfig(
                path=repo_path("examples/datasets/expansion/multiturn_dialog/hh_rlhf.jsonl"),
                label="expansion_hh_rlhf",
                bucket="instruction",
                max_examples=150_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/expansion/multiturn_dialog/ultrachat.jsonl"),
                label="expansion_ultrachat",
                bucket="instruction",
                max_examples=200_000,
            ),
            # EXPANSION DATASETS - Reasoning traces
            SourceConfig(
                path=repo_path("examples/datasets/expansion/reasoning_traces/math_instruct.jsonl"),
                label="expansion_math_instruct",
                bucket="analytical",
                max_examples=100_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/expansion/reasoning_traces/gsm8k_reasoning.jsonl"),
                label="expansion_gsm8k",
                bucket="cot_math",
            ),
            # EXPANSION DATASETS - Creative narrative
            SourceConfig(
                path=repo_path("examples/datasets/expansion/creative_narrative/writing_prompts.jsonl"),
                label="expansion_writing_prompts",
                bucket="creative",
                max_examples=100_000,
            ),
            # EXPANSION DATASETS - Factual grounding
            SourceConfig(
                path=repo_path("examples/datasets/expansion/factual_grounding/squad_v2.jsonl"),
                label="expansion_squad_v2",
                bucket="factual",
                max_examples=80_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/expansion/factual_grounding/trivia_qa.jsonl"),
                label="expansion_trivia_qa",
                bucket="factual",
            ),
            # EXPANSION DATASETS - Code debugging
            SourceConfig(
                path=repo_path("examples/datasets/expansion/code_debugging/code_alpaca_20k.jsonl"),
                label="expansion_code_alpaca",
                bucket="code",
            ),
        ],
    },
    "chatgpt_behavior": {
        "description": "OpenAI ChatGPT-style instruction / code / tool corpus.",
        "weights": {
            "instruction": 0.38,
            "analytical": 0.20,
            "red_team": 0.12,
            "code": 0.10,
            "tool_use": 0.09,
            "creative": 0.07,
            "factual": 0.03,
            "cot_math": 0.01,
        },
        "sources": [
            SourceConfig(
                path=repo_path("examples/datasets/open_orca.jsonl"),
                label="open_orca",
                max_examples=450_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/alpaca_gpt4.jsonl"),
                label="alpaca_gpt4",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/wizardlm_70k.jsonl"),
                label="wizardlm_70k",
                bucket="analytical",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/wizardlm_evol.jsonl"),
                label="wizardlm_evol",
                bucket="analytical",
                max_examples=60_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/glaive_function_calling.jsonl"),
                label="glaive_function_calling",
                bucket="tool_use",
                max_examples=80_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/creative_writing.jsonl"),
                label="creative_writing",
                bucket="creative",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/red_team_safe.jsonl"),
                label="red_team_safe",
                bucket="red_team",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/code_alpaca_full.jsonl"),
                label="code_alpaca_full",
                bucket="code",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/code_feedback_50k.jsonl"),
                label="code_feedback_50k",
                bucket="code",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/python_code_18k.jsonl"),
                label="python_code_18k",
                bucket="code",
            ),
            SourceConfig(
                path=repo_path("data/external/chatgpt/*.jsonl"),
                label="chatgpt_external",
            ),
            # EXPANSION DATASETS
            SourceConfig(
                path=repo_path("examples/datasets/expansion/multiturn_dialog/hh_rlhf.jsonl"),
                label="expansion_hh_rlhf",
                bucket="instruction",
                max_examples=150_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/expansion/multiturn_dialog/ultrachat.jsonl"),
                label="expansion_ultrachat",
                bucket="instruction",
                max_examples=200_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/expansion/reasoning_traces/math_instruct.jsonl"),
                label="expansion_math_instruct",
                bucket="analytical",
                max_examples=100_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/expansion/creative_narrative/writing_prompts.jsonl"),
                label="expansion_writing_prompts",
                bucket="creative",
                max_examples=80_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/expansion/factual_grounding/squad_v2.jsonl"),
                label="expansion_squad_v2",
                bucket="factual",
                max_examples=50_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/expansion/code_debugging/code_alpaca_20k.jsonl"),
                label="expansion_code_alpaca",
                bucket="code",
            ),
        ],
    },
    "deepseek_search": {
        "description": "DeepSeek-style search orchestration with heavy tool use and factual grounding.",
        "weights": {
            "instruction": 0.28,
            "tool_use": 0.25,
            "analytical": 0.15,
            "factual": 0.12,
            "cot_math": 0.08,
            "code": 0.05,
            "red_team": 0.04,
            "creative": 0.03,
        },
        "sources": [
            SourceConfig(
                path=repo_path("examples/datasets/ultimate_3M_intelligently_duplicated.jsonl"),
                label="ultimate_3m_mix",
                max_examples=800_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/open_orca.jsonl"),
                label="open_orca",
                max_examples=350_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/glaive_function_calling.jsonl"),
                label="glaive_function_calling",
                bucket="tool_use",
                max_examples=120_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/gsm8k_cot.jsonl"),
                label="gsm8k_cot",
                bucket="cot_math",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/orca_math_cot.jsonl"),
                label="orca_math_cot",
                bucket="cot_math",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/wizardlm_evol.jsonl"),
                label="wizardlm_evol",
                bucket="analytical",
                max_examples=80_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/wizardlm_70k.jsonl"),
                label="wizardlm_70k",
                bucket="analytical",
                max_examples=80_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/creative_writing.jsonl"),
                label="creative_writing",
                bucket="creative",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/red_team_safe.jsonl"),
                label="red_team_safe",
                bucket="red_team",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/code_feedback_50k.jsonl"),
                label="code_feedback_50k",
                bucket="code",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/code_alpaca_full.jsonl"),
                label="code_alpaca_full",
                bucket="code",
            ),
            SourceConfig(
                path=repo_path("data/external/deepseek/*.jsonl"),
                label="deepseek_external",
            ),
            # EXPANSION DATASETS
            SourceConfig(
                path=repo_path("examples/datasets/expansion/multiturn_dialog/ultrachat.jsonl"),
                label="expansion_ultrachat",
                bucket="instruction",
                max_examples=150_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/expansion/reasoning_traces/math_instruct.jsonl"),
                label="expansion_math_instruct",
                bucket="analytical",
                max_examples=100_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/expansion/factual_grounding/squad_v2.jsonl"),
                label="expansion_squad_v2",
                bucket="factual",
                max_examples=100_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/expansion/factual_grounding/trivia_qa.jsonl"),
                label="expansion_trivia_qa",
                bucket="factual",
            ),
        ],
    },
    "code_debugging": {
        "description": "Open-source coding corpus with debugging, refactoring, and walkthroughs.",
        "weights": {
            "code": 0.60,
            "instruction": 0.15,
            "analytical": 0.12,
            "tool_use": 0.05,
            "red_team": 0.03,
            "factual": 0.02,
            "creative": 0.02,
            "cot_math": 0.01,
        },
        "sources": [
            SourceConfig(
                path=repo_path("examples/datasets/code_alpaca_full.jsonl"),
                label="code_alpaca_full",
                bucket="code",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/code_feedback_50k.jsonl"),
                label="code_feedback_50k",
                bucket="analytical",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/codefeedback.jsonl"),
                label="code_feedback_misc",
                bucket="code",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/codefeedback_50k.jsonl"),
                label="code_feedback_50k_dup",
                bucket="code",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/code_generation.jsonl"),
                label="code_generation_snippets",
                bucket="code",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/evol_codealpaca.jsonl"),
                label="evol_codealpaca",
                bucket="code",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/python_code_18k.jsonl"),
                label="python_code_18k",
                bucket="code",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/magicoder_evol_110k.jsonl"),
                label="magicoder_evol_110k",
                bucket="code",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/magicoder_oss_75k.jsonl"),
                label="magicoder_oss_75k",
                bucket="code",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/dolphin_coder.jsonl"),
                label="dolphin_coder",
                bucket="code",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/mbpp.jsonl"),
                label="mbpp",
                bucket="code",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/code_x_glue_defect.jsonl"),
                label="code_x_glue_defect",
                bucket="analytical",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/expanded_training_1.5M.jsonl"),
                label="expanded_training_1_5M",
                max_examples=400_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/open_orca.jsonl"),
                label="open_orca_instruction",
                max_examples=120_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/red_team_safe.jsonl"),
                label="code_red_team_safe",
                bucket="red_team",
                max_examples=30_000,
            ),
            SourceConfig(
                path=repo_path("data/external/code/*.jsonl"),
                label="code_external",
                bucket="code",
            ),
            # EXPANSION DATASETS
            SourceConfig(
                path=repo_path("examples/datasets/expansion/code_debugging/code_alpaca_20k.jsonl"),
                label="expansion_code_alpaca",
                bucket="code",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/expansion/reasoning_traces/math_instruct.jsonl"),
                label="expansion_math_instruct",
                bucket="analytical",
                max_examples=80_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/expansion/multiturn_dialog/ultrachat.jsonl"),
                label="expansion_ultrachat",
                bucket="instruction",
                max_examples=100_000,
            ),
        ],
    },
    "esoteric_studies": {
        "description": "Occult, hermetic, and contemplative writings for metaphysical study.",
        "weights": {
            "instruction": 0.30,
            "creative": 0.35,
            "factual": 0.15,
            "analytical": 0.10,
            "red_team": 0.03,
            "tool_use": 0.03,
            "code": 0.02,
            "cot_math": 0.02,
        },
        "sources": [
            SourceConfig(
                path=repo_path("data/external/esoteric/*.jsonl"),
                label="esoteric_external",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/creative_writing.jsonl"),
                label="creative_writing",
                bucket="creative",
            ),
            SourceConfig(
                path=repo_path("examples/datasets/red_team_safe.jsonl"),
                label="esoteric_red_team",
                bucket="red_team",
                max_examples=10_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/ultimate_3M_intelligently_duplicated.jsonl"),
                label="ultimate_3m_mix",
                max_examples=150_000,
            ),
            # EXPANSION DATASETS
            SourceConfig(
                path=repo_path("examples/datasets/expansion/creative_narrative/writing_prompts.jsonl"),
                label="expansion_writing_prompts",
                bucket="creative",
                max_examples=200_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/expansion/multiturn_dialog/hh_rlhf.jsonl"),
                label="expansion_hh_rlhf",
                bucket="instruction",
                max_examples=100_000,
            ),
            SourceConfig(
                path=repo_path("examples/datasets/expansion/factual_grounding/squad_v2.jsonl"),
                label="expansion_squad_v2",
                bucket="factual",
                max_examples=100_000,
            ),
        ],
    },
}


def load_jsonl(path: Path) -> Iterable[Dict]:
    """Yield JSON objects from a .jsonl file."""
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def load_dataset(path: Path) -> Iterable[Dict]:
    """Load supported dataset formats."""
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    if path.suffix == ".jsonl":
        yield from load_jsonl(path)
    elif path.suffix == ".json":
        data = json.loads(path.read_text())
        if isinstance(data, list):
            for item in data:
                yield item
        else:
            raise ValueError(f"Unsupported JSON structure in {path}")
    else:
        raise ValueError(f"Unsupported file extension: {path.suffix}")


def normalize_example(raw: Dict) -> Dict:
    """
    Normalize an example to have `instruction`, `input`, `output` fields.
    Many datasets already follow this schema, but some use alternative keys.
    """
    instruction = raw.get("instruction") or raw.get("question") or raw.get("prompt") or ""
    output = raw.get("output") or raw.get("answer") or raw.get("completion") or ""
    input_text = raw.get("input", "")

    example = {
        "instruction": instruction.strip(),
        "input": input_text.strip() if isinstance(input_text, str) else input_text,
        "output": output.strip(),
    }

    # Preserve useful metadata if present
    for key in ("system", "_category", "_source", "_safety", "_bucket"):
        if key in raw:
            example[key] = raw[key]

    return example


def classify_bucket(example: Dict, override: Optional[str] = None) -> str:
    """Classify an example into a capability bucket."""
    if override and override != "auto":
        return override

    category = (example.get("_category") or "").lower()
    if category:
        if "code" in category:
            return "code"
        if "tool" in category or "function" in category:
            return "tool_use"
        if "cot" in category or "reason" in category or "math" in category:
            return "cot_math"
        if "creative" in category or "story" in category:
            return "creative"
        if "red" in category or "safety" in category:
            return "red_team"
        if "analysis" in category or "analytical" in category:
            return "analytical"

    text = f"{example.get('instruction', '')} {example.get('output', '')}".lower()

    # Safety / refusal indicators
    refusal_tokens = [
        "i cannot",
        "i can't",
        "i’m sorry",
        "cannot assist",
        "cannot help",
        "refuse",
        "decline",
        "inappropriate",
        "illegal",
    ]
    if any(tok in text for tok in refusal_tokens):
        return "red_team"

    # Tool-use heuristics
    if any(tok in text for tok in ["<tool>", "functioncall", "tool_use:", "<functioncall>"]):
        return "tool_use"

    # Code heuristics
    if any(tok in text for tok in ["```python", "```java", "```js", "```c", "def ", "class ", "import "]):
        return "code"

    # CoT / reasoning heuristics
    if any(tok in text for tok in ["let's think", "step 1", "step 2", "<thinking>", "chain of thought"]):
        if any(tok in text for tok in ["solve", "equation", "math", "calculate"]):
            return "cot_math"
        return "analytical"

    # Creative heuristics
    if any(tok in text for tok in ["story", "poem", "imagine", "narrative", "character"]):
        return "creative"

    # Factual heuristics
    if any(tok in text for tok in ["according to", "wikipedia", "study", "research shows", "data indicates"]):
        return "factual"

    return "instruction"


def hash_example(example: Dict) -> str:
    """Generate a stable hash for deduplication."""
    payload = {
        "instruction": example.get("instruction", ""),
        "input": example.get("input", ""),
        "output": example.get("output", ""),
    }
    return json.dumps(payload, sort_keys=True)


def collect_examples(
    profile_key: str,
    rng: random.Random,
    exclude_hashes: Optional[set] = None,
) -> Tuple[Dict[str, List[Dict]], Counter, int, int, int]:
    """Load and bucketize examples for the given profile."""
    config = PROFILE_CONFIGS[profile_key]
    bucket_examples: Dict[str, List[Dict]] = defaultdict(list)
    seen_hashes = set()
    exclude_hashes = exclude_hashes or set()

    total_loaded = 0
    total_duplicates = 0
    excluded_existing = 0
    per_source_counter = Counter()

    pattern_chars = {"*", "?", "["}

    for source in config["sources"]:
        path_str = str(source.path)
        candidate_paths = [source.path]
        if any(ch in path_str for ch in pattern_chars):
            candidate_paths = list(source.path.parent.glob(source.path.name))

        if not candidate_paths:
            print(f"[!] No files matched pattern: {source.path}")
            continue

        total_for_source = 0
        count_from_source = 0
        for actual_path in candidate_paths:
            if not actual_path.exists():
                print(f"[!] Skipping missing dataset: {actual_path}")
                continue

            for example in load_dataset(actual_path):
                normalized = normalize_example(example)

                data_hash = hash_example(normalized)
                if data_hash in exclude_hashes:
                    excluded_existing += 1
                    continue

                if data_hash in seen_hashes:
                    total_duplicates += 1
                    continue

                bucket = classify_bucket(normalized, override=source.bucket)
                normalized["_bucket"] = bucket
                normalized["_source"] = source.label

                bucket_examples[bucket].append(normalized)
                seen_hashes.add(data_hash)

                count_from_source += 1
                total_for_source += 1
                total_loaded += 1

                if source.max_examples and count_from_source >= source.max_examples:
                    break

            if source.max_examples and count_from_source >= source.max_examples:
                break

        per_source_counter[source.label] = total_for_source
        print(f"[i] Loaded {total_for_source:,} examples from {source.label} -> bucket {source.bucket}")

    return bucket_examples, per_source_counter, total_loaded, total_duplicates, excluded_existing


def sample_buckets(
    bucket_examples: Dict[str, List[Dict]],
    bucket_weights: Dict[str, float],
    max_total: int,
    rng: random.Random,
) -> List[Dict]:
    """Sample the requested number of examples per bucket."""
    final_examples: List[Dict] = []
    shortfalls = {}
    overflows = {}
    selected_hashes = set()

    total_weights = sum(bucket_weights.values())
    for bucket, weight in bucket_weights.items():
        desired = int((weight / total_weights) * max_total)
        available = len(bucket_examples.get(bucket, []))

        if available == 0:
            shortfalls[bucket] = desired
            continue

        if available >= desired:
            sampled = rng.sample(bucket_examples[bucket], desired)
            final_examples.extend(sampled)
            overflows[bucket] = available - desired
        else:
            final_examples.extend(bucket_examples[bucket])
            shortfalls[bucket] = desired - available

    # Track selected hashes for uniqueness
    for ex in final_examples:
        selected_hashes.add(hash_example(ex))

    if shortfalls:
        print("\n[!] Shortfalls detected (not enough data for target weights):")
        for bucket, deficit in shortfalls.items():
            print(f"    {bucket:12s} short by {deficit:,} examples")

    if overflows:
        print("\n[i] Remaining pool after sampling (per bucket):")
        for bucket, left in overflows.items():
            print(f"    {bucket:12s} {left:,} unused examples")

    # Top up using unused unique examples if total is below target
    if len(final_examples) < max_total:
        print(f"\n[i] Topping up from remaining pools to reach {max_total:,} examples...")
        for bucket, examples in bucket_examples.items():
            for ex in examples:
                key = hash_example(ex)
                if key in selected_hashes:
                    continue
                final_examples.append(ex)
                selected_hashes.add(key)
                if len(final_examples) >= max_total:
                    break
            if len(final_examples) >= max_total:
                break

    rng.shuffle(final_examples)
    return final_examples[:max_total]


def summarize(bucket_examples: Dict[str, List[Dict]]) -> None:
    """Print bucket coverage summary."""
    print("\n[✓] Bucket coverage summary (unique counts):")
    total = sum(len(lst) for lst in bucket_examples.values())
    for bucket, lst in sorted(bucket_examples.items(), key=lambda kv: len(kv[1]), reverse=True):
        pct = (len(lst) / total) * 100 if total else 0.0
        print(f"    {bucket:12s} {len(lst):10,} ({pct:5.1f}%)")
    print(f"    {'TOTAL':12s} {total:10,} (100.0%)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build balanced behavioral corpora.")
    parser.add_argument(
        "--profile",
        required=True,
        choices=PROFILE_CONFIGS.keys(),
        help="Profile key to build (claude_behavior or chatgpt_behavior).",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output JSONL path.",
    )
    parser.add_argument(
        "--max-total",
        type=int,
        default=1_200_000,
        help="Maximum number of examples in the final corpus.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=13,
        help="Random seed for reproducibility.",
    )
    parser.add_argument(
        "--global-cache",
        help="Optional path to a JSON file storing hashes of already used examples across profiles.",
    )
    parser.add_argument(
        "--reset-global-cache",
        action="store_true",
        help="Reset the global cache file before building (if used).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rng = random.Random(args.seed)

    global_cache: set = set()
    cache_path = None
    if args.global_cache:
        cache_path = Path(args.global_cache)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        if args.reset_global_cache and cache_path.exists():
            cache_path.unlink()
        if cache_path.exists():
            try:
                cached_hashes = json.loads(cache_path.read_text())
                if isinstance(cached_hashes, list):
                    global_cache.update(cached_hashes)
                else:
                    print(f"[!] Unexpected cache format in {cache_path}, ignoring existing entries")
            except json.JSONDecodeError:
                print(f"[!] Could not parse cache file {cache_path}, starting fresh")

    profile = PROFILE_CONFIGS[args.profile]
    print("=" * 80)
    print(f" Building profile: {args.profile}")
    print(f" {profile['description']}")
    print("=" * 80)

    bucket_examples, per_source_counts, total_loaded, duplicates, excluded_existing = collect_examples(
        args.profile, rng, exclude_hashes=global_cache
    )
    summarize(bucket_examples)

    print(f"\n[i] Deduplicated total: {total_loaded:,} examples")
    if duplicates:
        print(f"[i] Skipped {duplicates:,} duplicates across sources")
    if excluded_existing:
        print(f"[i] Skipped {excluded_existing:,} examples already present in global cache")

    final_examples = sample_buckets(bucket_examples, profile["weights"], args.max_total, rng)
    print(f"\n[✓] Final corpus size: {len(final_examples):,} examples (target {args.max_total:,})")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as fh:
        for example in final_examples:
            fh.write(json.dumps(example, ensure_ascii=False) + "\n")

    print(f"[✓] Saved corpus to {output_path}")

    if cache_path:
        global_cache.update(hash_example(ex) for ex in final_examples)
        cache_path.write_text(json.dumps(list(global_cache)))
        print(f"[i] Global cache updated with {len(final_examples):,} new entries → {cache_path}")

    print("\n[i] Source contribution (post-dedup):")
    for label, count in per_source_counts.items():
        print(f"    {label:25s} {count:10,}")


if __name__ == "__main__":
    main()
