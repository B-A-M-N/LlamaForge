#!/usr/bin/env python3
"""
Add explicit persona control tokens to all training data.

Converts implicit persona diversity into explicit conditioning tokens
that can be used at inference time for behavioral control.
"""

import json
import re
from pathlib import Path
from collections import Counter
from tqdm import tqdm


def detect_primary_persona(example):
    """Detect the primary persona/style for an example."""
    text = f"{example.get('instruction', '')} {example.get('output', '')}".lower()

    # Priority order - most specific first
    persona_rules = [
        # Specialized
        (["esoteric", "mystical", "occult", "hermetic", "archetype"], "esoteric_scholar"),
        (["therapy", "counseling", "empathy", "feelings", "emotional support"], "empathetic_counselor"),

        # Technical
        (["```python", "```java", "def ", "class ", "function("], "code_expert"),
        (["debug", "error", "traceback", "exception"], "debugging_assistant"),
        (["solve", "algorithm", "optimize"], "problem_solver"),

        # Reasoning
        (["step by step", "let's think", "reasoning:", "first,", "second,"], "analytical_reasoner"),
        (["math", "equation", "calculate", "solve for"], "math_tutor"),

        # Creative
        (["story", "once upon", "imagine", "narrative", "character"], "creative_storyteller"),
        (["poem", "verse", "metaphor", "imagery"], "creative_writer"),

        # Conversational
        (["human:", "assistant:", "conversation"], "conversational_agent"),
        (["empathize", "understand how you feel", "i hear you"], "empathetic_counselor"),

        # Tool/API
        (["<tool>", "function_call", "<functioncall>", "api"], "tool_orchestrator"),

        # Factual
        (["according to", "research shows", "fact:", "wikipedia"], "factual_informant"),

        # Safety
        (["i cannot", "i can't", "i'm unable", "inappropriate"], "safety_guardian"),

        # Debate
        (["argue", "debate", "consider", "perspective", "on the other hand"], "critical_debater"),
    ]

    # Check explicit category tags first
    if "_category" in example:
        category = example["_category"]
        category_to_persona = {
            "psychology_emotional": "empathetic_counselor",
            "code_debugging": "code_expert",
            "tool_api": "tool_orchestrator",
            "creative_narrative": "creative_storyteller",
            "reasoning_trace": "analytical_reasoner",
            "factual_grounding": "factual_informant",
            "multiturn_dialog": "conversational_agent",
            "red_team": "safety_guardian",
            "adversarial_moral": "critical_debater",
        }
        if category in category_to_persona:
            return category_to_persona[category]

    # Check existing _persona tag
    if "_persona" in example:
        return example["_persona"]

    # Pattern matching
    for patterns, persona in persona_rules:
        if any(pattern in text for pattern in patterns):
            return persona

    # Default based on length/style
    avg_sentence_length = len(text.split()) / max(len(text.split('.')), 1)
    if avg_sentence_length > 25:
        return "verbose_explainer"
    elif avg_sentence_length < 10:
        return "concise_responder"

    return "general_assistant"


def detect_secondary_traits(example):
    """Detect secondary behavioral traits."""
    text = f"{example.get('instruction', '')} {example.get('output', '')}".lower()
    traits = []

    # Formality
    formal_markers = len(re.findall(r'\b(furthermore|moreover|consequently|therefore|thus)\b', text))
    casual_markers = len(re.findall(r'\b(yeah|gonna|wanna|hey|cool)\b', text))

    if formal_markers > casual_markers and formal_markers > 2:
        traits.append("formal")
    elif casual_markers > formal_markers and casual_markers > 1:
        traits.append("casual")

    # Detail level
    if len(text.split()) > 500:
        traits.append("detailed")
    elif len(text.split()) < 100:
        traits.append("brief")

    # Emotional tone
    positive_markers = len(re.findall(r'\b(great|excellent|wonderful|amazing|happy)\b', text))
    if positive_markers > 3:
        traits.append("positive")

    supportive_markers = len(re.findall(r'\b(support|help|assist|understand|empathize)\b', text))
    if supportive_markers > 2:
        traits.append("supportive")

    # Reasoning style
    if "step 1" in text or "step 2" in text:
        traits.append("methodical")

    if "however" in text or "although" in text or "but" in text:
        traits.append("nuanced")

    return traits[:3]  # Max 3 secondary traits


def add_persona_tokens(input_dir, output_dir):
    """Add persona tokens to all datasets."""

    print("=" * 80)
    print(" ADDING PERSONA CONTROL TOKENS")
    print("=" * 80)

    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Find all JSONL files
    all_files = list(input_path.rglob("*.jsonl"))

    print(f"\n[i] Found {len(all_files)} dataset files\n")

    persona_counts = Counter()
    trait_counts = Counter()
    total_processed = 0

    for file_path in tqdm(all_files, desc="Processing files"):
        # Create output path maintaining directory structure
        rel_path = file_path.relative_to(input_path)
        out_file = output_path / rel_path
        out_file.parent.mkdir(parents=True, exist_ok=True)

        count = 0

        with file_path.open('r', encoding='utf-8') as f_in, \
             out_file.open('w', encoding='utf-8') as f_out:

            for line in f_in:
                line = line.strip()
                if not line:
                    continue

                try:
                    example = json.loads(line)

                    # Detect primary persona
                    primary_persona = detect_primary_persona(example)
                    persona_counts[primary_persona] += 1

                    # Detect secondary traits
                    traits = detect_secondary_traits(example)
                    for trait in traits:
                        trait_counts[trait] += 1

                    # Add persona metadata
                    example["_persona"] = primary_persona
                    if traits:
                        example["_traits"] = traits

                    # Add persona control token to instruction
                    instruction = example.get("instruction", "")
                    persona_token = f"<persona:{primary_persona}>"

                    # Only add if not already present
                    if not instruction.startswith("<persona:"):
                        example["instruction"] = f"{persona_token}\n{instruction}"

                    # Write enhanced example
                    f_out.write(json.dumps(example, ensure_ascii=False) + "\n")
                    count += 1
                    total_processed += 1

                except json.JSONDecodeError:
                    continue

        if count > 0:
            print(f"  {rel_path}: {count:,} examples tagged")

    # Summary
    print("\n" + "=" * 80)
    print(" PERSONA TAGGING SUMMARY")
    print("=" * 80)

    print(f"\nTotal examples processed: {total_processed:,}")
    print(f"\nPersona distribution:")
    for persona, count in persona_counts.most_common(20):
        pct = (count / total_processed * 100) if total_processed > 0 else 0
        print(f"  {persona:30s} {count:>10,} ({pct:>5.1f}%)")

    print(f"\nTop secondary traits:")
    for trait, count in trait_counts.most_common(10):
        pct = (count / total_processed * 100) if total_processed > 0 else 0
        print(f"  {trait:20s} {count:>10,} ({pct:>5.1f}%)")

    print(f"\n[✓] Tagged datasets saved to: {output_path}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        input_dir = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else "examples/datasets_persona_tagged"
    else:
        input_dir = "examples/datasets"
        output_dir = "examples/datasets_persona_tagged"

    add_persona_tokens(input_dir, output_dir)
