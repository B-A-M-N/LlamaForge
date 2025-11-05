#!/usr/bin/env python3
"""
Analyze persona and personality diversity across all datasets.
Identifies distinct behavioral patterns, tones, and stylistic voices.
"""

import json
import re
from pathlib import Path
from collections import Counter, defaultdict
from tqdm import tqdm


def load_jsonl_sample(file_path, max_samples=1000):
    """Load a sample of examples from JSONL file."""
    examples = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= max_samples:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    examples.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        pass
    return examples


def detect_persona_markers(text):
    """Detect explicit persona/personality markers in text."""
    text_lower = text.lower()
    personas = []

    # Explicit persona tags
    if "<claude" in text_lower or "claude:" in text_lower:
        personas.append("claude_style")
    if "<chatgpt" in text_lower or "chatgpt:" in text_lower or "assistant:" in text_lower:
        personas.append("chatgpt_style")
    if "<shadow" in text_lower:
        personas.append("shadow_mode")
    if "human:" in text_lower and "assistant:" in text_lower:
        personas.append("conversational_agent")

    # Tone markers
    if any(x in text_lower for x in ["i cannot", "i can't", "i'm unable", "i apologize"]):
        personas.append("helpful_harmless")
    if any(x in text_lower for x in ["let's think", "step by step", "reasoning:", "first,"]):
        personas.append("analytical_reasoner")
    if any(x in text_lower for x in ["imagine", "once upon", "story", "narrative"]):
        personas.append("creative_storyteller")
    if any(x in text_lower for x in ["according to", "research shows", "studies indicate", "fact:"]):
        personas.append("factual_informant")
    if any(x in text_lower for x in ["```python", "```java", "def ", "function", "class "]):
        personas.append("code_expert")
    if any(x in text_lower for x in ["empathy", "feelings", "emotions", "support", "understand"]):
        personas.append("empathetic_counselor")
    if any(x in text_lower for x in ["tool:", "function_call", "<tool>", "api"]):
        personas.append("tool_orchestrator")
    if any(x in text_lower for x in ["solve", "problem", "solution", "debug", "fix"]):
        personas.append("problem_solver")
    if any(x in text_lower for x in ["esoteric", "mystical", "spiritual", "occult", "hermetic"]):
        personas.append("esoteric_scholar")
    if any(x in text_lower for x in ["argue", "debate", "perspective", "consider", "on the other hand"]):
        personas.append("critical_debater")

    # Formality detection
    formal_markers = len(re.findall(r'\b(furthermore|moreover|consequently|therefore|thus|hence)\b', text_lower))
    casual_markers = len(re.findall(r'\b(yeah|gonna|wanna|kinda|sorta|hey|cool|awesome)\b', text_lower))

    if formal_markers > casual_markers and formal_markers > 2:
        personas.append("formal_academic")
    elif casual_markers > formal_markers and casual_markers > 2:
        personas.append("casual_friendly")

    # Length-based complexity
    avg_sentence_length = len(text.split()) / max(len(text.split('.')), 1)
    if avg_sentence_length > 25:
        personas.append("verbose_detailed")
    elif avg_sentence_length < 10:
        personas.append("concise_brief")

    return personas


def analyze_source_personas(source_name):
    """Map dataset sources to their inherent personas."""
    source_personas = {
        # Claude-style datasets
        "claude_reasoning_ultimate": ["claude_style", "analytical_reasoner", "helpful_harmless"],
        "claude_behavioral_mix": ["claude_style", "balanced_assistant"],
        "claude_mega": ["claude_style", "comprehensive_assistant"],
        "claude_ultimate": ["claude_style", "advanced_reasoner"],

        # ChatGPT-style datasets
        "open_orca": ["chatgpt_style", "conversational_agent", "helpful_assistant"],
        "alpaca": ["chatgpt_style", "instruction_follower"],
        "chatgpt_behavioral": ["chatgpt_style", "balanced_assistant"],

        # Code-focused
        "code_alpaca": ["code_expert", "problem_solver", "technical_instructor"],
        "code_feedback": ["code_expert", "code_reviewer", "debugging_assistant"],
        "magicoder": ["code_expert", "code_generator", "technical_expert"],
        "python_code": ["code_expert", "python_specialist"],
        "dolphin_coder": ["code_expert", "uncensored_coder"],
        "evol_codealpaca": ["code_expert", "evolved_reasoner"],

        # Reasoning & Math
        "gsm8k": ["analytical_reasoner", "math_tutor", "step_by_step_explainer"],
        "orca_math": ["analytical_reasoner", "math_expert"],
        "metamath": ["analytical_reasoner", "mathematical_thinker"],
        "math_instruct": ["analytical_reasoner", "math_instructor"],

        # Creative
        "creative_writing": ["creative_storyteller", "narrative_writer", "imaginative_author"],
        "writing_prompts": ["creative_storyteller", "fiction_writer"],

        # Dialog & Conversation
        "hh_rlhf": ["conversational_agent", "helpful_harmless", "safe_assistant"],
        "ultrachat": ["conversational_agent", "multi_turn_specialist", "contextual_responder"],
        "oasst": ["conversational_agent", "community_assistant"],

        # Factual & QA
        "squad": ["factual_informant", "qa_specialist", "reading_comprehender"],
        "trivia": ["factual_informant", "trivia_expert", "knowledge_base"],

        # Tool use
        "glaive_function": ["tool_orchestrator", "api_specialist", "function_caller"],

        # Analytical
        "wizardlm": ["analytical_reasoner", "evolved_thinker", "complex_problem_solver"],

        # Safety
        "red_team": ["safety_conscious", "refusal_expert", "boundary_enforcer"],

        # Esoteric
        "esoteric": ["esoteric_scholar", "mystical_guide", "occult_expert"],

        # DeepSeek
        "deepseek": ["search_orchestrator", "tool_user", "research_assistant"],
    }

    # Find matching personas
    for key, personas in source_personas.items():
        if key in source_name.lower():
            return personas

    return ["general_assistant"]


def analyze_persona_diversity():
    """Analyze persona diversity across all datasets."""

    print("=" * 80)
    print(" PERSONA & PERSONALITY DIVERSITY ANALYSIS")
    print("=" * 80)

    # Collect all dataset files
    dataset_dirs = [
        Path("examples/datasets"),
        Path("examples/datasets/expansion"),
    ]

    all_files = []
    for base_dir in dataset_dirs:
        if base_dir.exists():
            all_files.extend(base_dir.rglob("*.jsonl"))

    # Track personas
    all_personas = Counter()
    persona_by_source = defaultdict(Counter)
    explicit_personas = Counter()
    implicit_personas = Counter()

    print(f"\n[i] Analyzing {len(all_files)} dataset files...\n")

    for file_path in tqdm(sorted(all_files), desc="Analyzing"):
        source_name = file_path.stem

        # Get inherent source personas
        source_personas = analyze_source_personas(source_name)
        for p in source_personas:
            all_personas[p] += 1
            persona_by_source[source_name][p] += 1

        # Sample and analyze content
        examples = load_jsonl_sample(file_path, max_samples=500)

        for example in examples:
            text = f"{example.get('instruction', '')} {example.get('output', '')}"

            # Detect personas in content
            detected = detect_persona_markers(text)
            for persona in detected:
                all_personas[persona] += 1
                persona_by_source[source_name][persona] += 1
                implicit_personas[persona] += 1

            # Check for explicit tags
            if "_persona" in example:
                explicit_personas[example["_persona"]] += 1
            if "_style" in example:
                explicit_personas[example["_style"]] += 1

    return all_personas, persona_by_source, explicit_personas, implicit_personas


def print_results(all_personas, persona_by_source, explicit_personas, implicit_personas):
    """Print detailed persona analysis."""

    print("\n" + "=" * 80)
    print(" PERSONA CATEGORIES DETECTED")
    print("=" * 80)

    # Group personas by category
    categories = {
        "Assistant Styles": ["claude_style", "chatgpt_style", "general_assistant", "balanced_assistant",
                            "helpful_harmless", "helpful_assistant", "safe_assistant", "uncensored_coder"],

        "Behavioral Modes": ["conversational_agent", "multi_turn_specialist", "contextual_responder",
                            "instruction_follower", "problem_solver", "analytical_reasoner"],

        "Domain Experts": ["code_expert", "math_expert", "math_tutor", "python_specialist",
                          "code_reviewer", "debugging_assistant", "technical_expert", "technical_instructor"],

        "Reasoning Types": ["step_by_step_explainer", "evolved_reasoner", "complex_problem_solver",
                           "analytical_reasoner", "evolved_thinker", "mathematical_thinker"],

        "Creative Personas": ["creative_storyteller", "narrative_writer", "imaginative_author",
                             "fiction_writer"],

        "Knowledge Specialists": ["factual_informant", "qa_specialist", "reading_comprehender",
                                 "trivia_expert", "knowledge_base", "research_assistant"],

        "Tool & API": ["tool_orchestrator", "api_specialist", "function_caller",
                      "search_orchestrator", "tool_user"],

        "Emotional & Social": ["empathetic_counselor", "critical_debater", "community_assistant"],

        "Specialized": ["esoteric_scholar", "mystical_guide", "occult_expert",
                       "safety_conscious", "refusal_expert", "boundary_enforcer"],

        "Communication Styles": ["formal_academic", "casual_friendly", "verbose_detailed",
                                "concise_brief"],
    }

    total_unique_personas = len(set(all_personas.keys()))

    print(f"\n📊 TOTAL UNIQUE PERSONAS DETECTED: {total_unique_personas}\n")

    for category, persona_list in categories.items():
        found = [p for p in persona_list if p in all_personas]
        if found:
            print(f"\n{category}:")
            print("-" * 80)
            for persona in found:
                count = all_personas[persona]
                print(f"  {persona:30s} {count:>10,} occurrences")

    # Other personas not categorized
    categorized = set()
    for persona_list in categories.values():
        categorized.update(persona_list)

    other = [p for p in all_personas if p not in categorized]
    if other:
        print(f"\nOther Personas:")
        print("-" * 80)
        for persona in sorted(other, key=lambda x: all_personas[x], reverse=True)[:20]:
            count = all_personas[persona]
            print(f"  {persona:30s} {count:>10,} occurrences")

    # Top datasets by persona diversity
    print("\n" + "=" * 80)
    print(" TOP DATASETS BY PERSONA DIVERSITY")
    print("=" * 80)

    diversity_scores = {
        source: len(personas)
        for source, personas in persona_by_source.items()
    }

    for source, score in sorted(diversity_scores.items(), key=lambda x: x[1], reverse=True)[:15]:
        personas = persona_by_source[source]
        top_personas = [p for p, _ in personas.most_common(3)]
        print(f"  {source:40s} {score:>3} personas ({', '.join(top_personas)})")

    # Summary statistics
    print("\n" + "=" * 80)
    print(" SUMMARY STATISTICS")
    print("=" * 80)

    print(f"\nTotal unique personas/styles:     {total_unique_personas:>6}")
    print(f"Explicit persona tags:             {len(explicit_personas):>6}")
    print(f"Implicit behavioral patterns:      {len(implicit_personas):>6}")
    print(f"Datasets analyzed:                 {len(persona_by_source):>6}")

    print(f"\nMost common personas:")
    for persona, count in all_personas.most_common(10):
        print(f"  {persona:30s} {count:>10,}")


if __name__ == "__main__":
    all_personas, persona_by_source, explicit_personas, implicit_personas = analyze_persona_diversity()
    print_results(all_personas, persona_by_source, explicit_personas, implicit_personas)
