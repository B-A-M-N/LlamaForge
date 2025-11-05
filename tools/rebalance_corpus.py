#!/usr/bin/env python3
"""
Rebalance the FINAL_CORPUS_7M dataset by removing low-quality slices,
repairing malformed records, and injecting high-quality reasoning plus
dark-protector/philosophy persona data.
"""

import argparse
import hashlib
import json
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, Tuple

CORPUS_ROOT = Path("examples/datasets")
BASE_CORPUS = CORPUS_ROOT / "FINAL_CORPUS_7M.jsonl"
OUTPUT_CORPUS = CORPUS_ROOT / "FINAL_CORPUS_7M_REBALANCED.jsonl"
OUTPUT_MANIFEST = CORPUS_ROOT / "FINAL_MANIFEST_7M_REBALANCED.json"
HASH_DB = Path("output/rebalanced_hashes.sqlite")

EXCLUDE_SOURCES = {
    "esoteric_external",
}

# Persona enrichment targets
PROTECTOR_SOURCES = {
    "chatgpt_external",
    "open_orca",
    "ultimate_3m_mix",
    "wizardlm_evol",
    "wizardlm_70k",
    "alpaca_full",
    "alpaca_gpt4",
    "glaive_function_calling",
    "claude_reasoning_ultimate",
    "claude_external",
    "prosocial_reasoning",
    "life_narratives",
    "personal_narratives",
    "psychology_papers",
    "emotion_analysis",
    "emotional_patterns",
    "therapy_depth",
    "mental_health_counseling",
    "mental_health_chatbot",
    "prosocial_dialog",
    "hh_rlhf",
    "anthropic/hh-rlhf",
    "hh_rlhf_debate",
    "red_team_safe",
    "ultrachat",
    "empathetic_dialogues",
    "daily_dialog",
}

PHILOSOPHY_SOURCES = {
    "chatgpt_external",
    "open_orca",
    "ultimate_3m_mix",
    "claude_reasoning_ultimate",
    "claude_external",
    "wizardlm_evol",
    "wizardlm_70k",
    "alpaca_full",
    "alpaca_gpt4",
    "philosophy_papers",
    "existential_dialog",
    "philosophical_debate",
    "moral_stories_full",
    "ethics_commonsense",
    "ethics_commonsense_v2",
    "ethics_deontology",
    "ethics_justice",
    "ethics_utilitarianism",
    "ethics_virtue",
    "adversarial_moral",
    "psychology_papers",
    "life_narratives",
    "personal_narratives",
    "writing_prompts",
    "kaist-ai/cot-collection",
}

PROTECTOR_SOURCES = {s.lower() for s in PROTECTOR_SOURCES}
PHILOSOPHY_SOURCES = {s.lower() for s in PHILOSOPHY_SOURCES}

PERSONA_LIMITS = {
    "dark_protector_archetype": 85000,
    "dark_philosophy": 80000,
}

PROTECTOR_KEYWORDS = [
    "trauma",
    "abuse",
    "boundaries",
    "boundary",
    "self-defense",
    "protect",
    "protection",
    "safety plan",
    "harm reduction",
    "hypervigilance",
    "resilience",
    "shadow work",
    "shadow",
    "antifragile",
    "self protection",
    "gaslight",
    "gaslighting",
    "emotional abuse",
    "attachment",
    "neglect",
    "survival",
    "healing",
    "cptsd",
    "inner child",
    "safety",
    "boundary-setting",
    "power dynamic",
    "traumatic",
    "violence",
    "safety plan",
]

PHILOSOPHY_KEYWORDS = [
    "nihil",
    "absurd",
    "void",
    "abyss",
    "existential",
    "death",
    "mortality",
    "memento",
    "camus",
    "sartre",
    "nietzsche",
    "schopenhauer",
    "heidegger",
    "will to power",
    "eternal return",
    "meaninglessness",
    "nothingness",
    "dark night",
    "entropy",
    "mortal",
    "doom",
    "apocalypse",
    "suffering",
    "tragedy",
    "anguish",
    "shadow",
    "fate",
    "pessimis",
    "existence",
    "being-toward-death",
]


def classify_persona(source: str, text: str, persona_counts: Counter):
    """Return optional persona category override based on source and content."""
    s_lower = source.lower()
    if (
        s_lower in PROTECTOR_SOURCES
        and any(kw in text for kw in PROTECTOR_KEYWORDS)
        and persona_counts["dark_protector_archetype"] < PERSONA_LIMITS["dark_protector_archetype"]
    ):
        persona_counts["dark_protector_archetype"] += 1
        return "dark_protector_archetype"
    if (
        s_lower in PHILOSOPHY_SOURCES
        and any(kw in text for kw in PHILOSOPHY_KEYWORDS)
        and persona_counts["dark_philosophy"] < PERSONA_LIMITS["dark_philosophy"]
    ):
        persona_counts["dark_philosophy"] += 1
        return "dark_philosophy"
    return None

# High-signal additions to back-fill reasoning and persona coverage.
ADDITIONAL_JSONL = [
    CORPUS_ROOT / "dark_protector" / "dark_protector_ultra_massive_150k.jsonl",
    CORPUS_ROOT / "dark_protector" / "dark_protector_contextual_expansion.jsonl",
    CORPUS_ROOT / "dark_protector" / "dark_protector_archetype.jsonl",
    CORPUS_ROOT / "dark_protector" / "dark_humor_corpus.jsonl",
    CORPUS_ROOT / "dark_philosophy" / "dark_philosophy_core.jsonl",
]

# Additional reasoning-heavy corpora.
REASONING_JSONL = [
    CORPUS_ROOT / "specialized" / "reasoning_compression" / "cot_collection.jsonl",
    CORPUS_ROOT / "specialized" / "short_context" / "alpaca_gpt4_short.jsonl",
    CORPUS_ROOT / "specialized" / "short_context" / "gpt4_llm_cleaned.jsonl",
    CORPUS_ROOT / "specialized" / "structured_output" / "code_instructions_structured.jsonl",
    CORPUS_ROOT / "specialized" / "structured_output" / "sql_create_context.jsonl",
    CORPUS_ROOT / "specialized" / "structured_output" / "wikisql.jsonl",
    CORPUS_ROOT / "specialized" / "tool_api" / "glaive_function_calling_v2.jsonl",
    CORPUS_ROOT / "advanced_science" / "bayesian_inference.jsonl",
    CORPUS_ROOT / "advanced_science" / "chaos_theory.jsonl",
    CORPUS_ROOT / "advanced_science" / "machine_learning.jsonl",
    CORPUS_ROOT / "advanced_science" / "statistical_mechanics.jsonl",
    CORPUS_ROOT / "gap_spanning" / "reasoning" / "metamath_qa.jsonl",
    CORPUS_ROOT / "gap_spanning" / "code" / "code_contests.jsonl",
    CORPUS_ROOT / "gap_spanning" / "code" / "code_completion_python.jsonl",
    CORPUS_ROOT / "gap_spanning" / "factual" / "hotpot_qa.jsonl",
    CORPUS_ROOT / "gap_spanning" / "dpo" / "hh_rlhf_dpo.jsonl",
    CORPUS_ROOT / "UNMERGED_DATASETS_COMBINED.jsonl",
    CORPUS_ROOT / "FINAL_MERGED_CORPUS_10M.jsonl",
]


def iter_jsonl(path: Path) -> Iterable[Tuple[int, dict]]:
    """Yield line number and parsed JSON objects from JSONL, skipping bad lines."""
    with path.open("r", encoding="utf-8") as handle:
        for idx, raw in enumerate(handle, start=1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                yield idx, json.loads(raw)
            except json.JSONDecodeError:
                continue


def normalize_fields(example: dict) -> Tuple[str, str, str]:
    """Extract instruction/input/output, trying multiple field variations."""
    instruction = (
        example.get("instruction")
        or example.get("prompt")
        or example.get("question")
        or example.get("text")
        or ""
    )
    input_text = example.get("input") or example.get("context") or ""
    output = (
        example.get("output")
        or example.get("response")
        or example.get("answer")
        or example.get("completion")
        or example.get("text")
        or ""
    )

    if not isinstance(instruction, str):
        instruction = json.dumps(instruction, ensure_ascii=False)
    if not isinstance(input_text, str):
        input_text = json.dumps(input_text, ensure_ascii=False)
    if not isinstance(output, str):
        output = json.dumps(output, ensure_ascii=False)

    # Handle conversation-style formats.
    if not instruction and isinstance(example.get("conversations"), list):
        convs = example["conversations"]
        if len(convs) >= 2:
            instruction = convs[0].get("value", "")
            output = convs[-1].get("value", "")

    if not instruction and isinstance(example.get("messages"), list):
        msgs = example["messages"]
        if len(msgs) >= 2:
            instruction = msgs[0].get("content", "")
            output = msgs[-1].get("content", "")

    return instruction.strip(), input_text.strip(), output.strip()


def hash_example(ins: str, inp: str, out: str) -> str:
    payload = "\u241f".join((ins, inp, out))
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()


def collect_additional_files() -> Iterable[Path]:
    """Gather additional reasoning JSONL files."""
    files = []
    for candidate in ADDITIONAL_JSONL + REASONING_JSONL:
        if candidate.exists() and candidate.stat().st_size > 0:
            files.append(candidate)
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base",
        type=Path,
        default=BASE_CORPUS,
        help="Path to the baseline corpus JSONL.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_CORPUS,
        help="Path for the cleaned corpus JSONL.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=OUTPUT_MANIFEST,
        help="Path for the output manifest JSON.",
    )
    args = parser.parse_args()

    if not args.base.exists():
        raise SystemExit(f"Base corpus not found: {args.base}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    HASH_DB.parent.mkdir(parents=True, exist_ok=True)
    if HASH_DB.exists():
        HASH_DB.unlink()

    conn = sqlite3.connect(str(HASH_DB))
    conn.execute("PRAGMA journal_mode=MEMORY")
    conn.execute("PRAGMA synchronous=OFF")
    conn.execute("CREATE TABLE IF NOT EXISTS seen(hash TEXT PRIMARY KEY)")
    insert_cursor = conn.cursor()
    batch = 0

    stats = Counter()
    drop_reasons = Counter()
    category_counts = Counter()
    source_counts = Counter()
    persona_counts = Counter()

    def try_write(ins: str, inp: str, out: str, example: dict, origin: Path):
        nonlocal batch
        if not ins or not out:
            drop_reasons["missing_instruction_or_output"] += 1
            return False

        source = example.get("_source")
        if not source:
            source = origin.stem
            example["_source"] = source

        if source in EXCLUDE_SOURCES:
            drop_reasons["excluded_source"] += 1
            return False

        digest = hash_example(ins, inp, out)
        insert_cursor.execute("INSERT OR IGNORE INTO seen VALUES (?)", (digest,))
        if insert_cursor.rowcount == 0:
            drop_reasons["duplicate"] += 1
            return False

        batch += 1
        if batch >= 5000:
            conn.commit()
            batch = 0

        persona_override = classify_persona(source, f"{ins} {inp} {out}".lower(), persona_counts)
        if persona_override:
            category = persona_override
        else:
            category = example.get("_category", "unknown")
        example["_category"] = category
        example["_source"] = source
        category_counts[category] += 1
        source_counts[source] += 1

        payload = {
            "instruction": ins,
            "input": inp,
            "output": out,
            "_category": category,
            "_source": source,
        }
        args.output_handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
        stats["written"] += 1
        return True

    with args.output.open("w", encoding="utf-8") as out_handle:
        args.output_handle = out_handle

        # Pass 1: filter the baseline corpus.
        for line_no, example in iter_jsonl(args.base):
            ins, inp, out = normalize_fields(example)
            if try_write(ins, inp, out, example, args.base):
                stats["base_kept"] += 1
            else:
                stats["base_dropped"] += 1

        # Pass 2: add curated persona + reasoning datasets.
        for extra_path in collect_additional_files():
            if not extra_path.exists():
                continue
            for line_no, example in iter_jsonl(extra_path):
                ins, inp, out = normalize_fields(example)
                if try_write(ins, inp, out, example, extra_path):
                    stats["extra_added"] += 1
                else:
                    stats["extra_dropped"] += 1

    if batch:
        conn.commit()
    conn.close()
    if HASH_DB.exists():
        HASH_DB.unlink()

    manifest = {
        "source_corpus": str(args.base),
        "output_corpus": str(args.output),
        "total_written": stats["written"],
        "base_retained": stats["base_kept"],
        "base_dropped": stats["base_dropped"],
        "extras_added": stats["extra_added"],
        "extras_dropped": stats["extra_dropped"],
        "drop_reasons": dict(drop_reasons),
        "category_counts": dict(category_counts),
        "source_counts": dict(source_counts),
        "persona_overrides": dict(persona_counts),
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    with args.manifest.open("w", encoding="utf-8") as man_handle:
        json.dump(manifest, man_handle, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
