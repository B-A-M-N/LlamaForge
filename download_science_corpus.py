#!/usr/bin/env python3
"""Download a focused science corpus covering chaos theory, Bayesian inference,
statistical mechanics, and machine learning topics.

The script streams relevant abstracts/problems from public Hugging Face datasets
and normalizes them into instruction-tuning friendly JSONL files.
"""

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List

from datasets import load_dataset
from tqdm import tqdm


@dataclass
class TopicConfig:
    name: str
    keywords: List[str]
    instruction: str
    category: str
    limit: int
    collected: int = 0
    hashes: set = field(default_factory=set)


OUTPUT_DIR = Path("examples/datasets/advanced_science")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Topic definitions for filtering arXiv abstracts.
TOPICS: List[TopicConfig] = [
    TopicConfig(
        name="chaos_theory",
        keywords=[
            "chaos",
            "chaotic",
            "strange attractor",
            "nonlinear dynamics",
            "lyapunov",
            "bifurcation",
            "dynamic instability",
        ],
        instruction="Explain the following research abstract on chaos theory and nonlinear dynamics.",
        category="chaos_theory",
        limit=20000,
    ),
    TopicConfig(
        name="bayesian_inference",
        keywords=[
            "bayesian",
            "posterior",
            "prior",
            "bayes",
            "mcmc",
            "markov chain monte carlo",
            "variational inference",
            "probabilistic inference",
        ],
        instruction="Summarize the following abstract with emphasis on Bayesian inference methods.",
        category="bayesian_inference",
        limit=20000,
    ),
    TopicConfig(
        name="statistical_mechanics",
        keywords=[
            "statistical mechanics",
            "partition function",
            "ising model",
            "boltzmann",
            "thermodynamic limit",
            "spin glass",
            "entropy production",
            "renormalization group",
        ],
        instruction="Describe the key ideas from this statistical mechanics abstract in clear terms.",
        category="statistical_mechanics",
        limit=20000,
    ),
    TopicConfig(
        name="machine_learning",
        keywords=[
            "machine learning",
            "neural network",
            "deep learning",
            "representation learning",
            "reinforcement learning",
            "self-supervised",
            "transformer",
            "gradient descent",
            "classifi",
            "regression model",
        ],
        instruction="Summarize the following machine learning research abstract, highlighting the main contribution.",
        category="machine_learning",
        limit=30000,
    ),
]


def sha256_digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalized_example(instruction: str, body: str, source: str, category: str) -> dict:
    return {
        "instruction": instruction,
        "input": "",
        "output": body,
        "_source": source,
        "_category": category,
    }


def stream_arxiv_topics() -> None:
    """Stream the arXiv portion of scientific_papers and collect topic-specific abstracts."""

    for topic in TOPICS:
        existing_path = OUTPUT_DIR / f"{topic.name}.jsonl"
        if existing_path.exists():
            with existing_path.open("r", encoding="utf-8") as existing_file:
                for line in existing_file:
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    digest = sha256_digest(obj.get("output", ""))
                    topic.hashes.add(digest)
                    topic.collected += 1

    dataset = load_dataset(
        "scientific_papers",
        "arxiv",
        split="train",
        streaming=True,
        trust_remote_code=True,
    )

    writers = {
        topic.name: (OUTPUT_DIR / f"{topic.name}.jsonl").open("a", encoding="utf-8")
        for topic in TOPICS
    }

    try:
        for idx, example in enumerate(dataset):
            abstract = example.get("abstract") or ""
            if not abstract:
                continue

            title = example.get("article", "").split("\n")[0][:256]
            text_blob = f"Title: {title}\n\nAbstract: {abstract.strip()}"
            lower_blob = text_blob.lower()

            for topic in TOPICS:
                if topic.collected >= topic.limit:
                    continue

                if any(keyword in lower_blob for keyword in topic.keywords):
                    payload_hash = sha256_digest(text_blob)
                    if payload_hash in topic.hashes:
                        continue

                    topic.hashes.add(payload_hash)
                    record = normalized_example(
                        instruction=topic.instruction,
                        body=text_blob,
                        source="scientific_papers_arxiv",
                        category=topic.category,
                    )
                    writers[topic.name].write(json.dumps(record, ensure_ascii=False) + "\n")
                    topic.collected += 1

            if idx % 1000 == 0 and idx > 0:
                collected_summary = ", ".join(
                    f"{topic.name}: {topic.collected}" for topic in TOPICS
                )
                print(f"[arxiv] processed {idx:,} records | {collected_summary}")

            if all(topic.collected >= topic.limit for topic in TOPICS):
                print("[arxiv] reached targets for all topics")
                break

        else:
            print("[arxiv] stream ended before hitting all targets")

    finally:
        for handle in writers.values():
            handle.close()


def ingest_bayesian_problem_sets(limit: int = 8000) -> int:
    """Augment bayesian corpus with problem-solution pairs."""

    output_file = OUTPUT_DIR / "bayesian_inference.jsonl"
    seen_hashes = set()
    collected = 0

    if output_file.exists():
        with output_file.open("r", encoding="utf-8") as existing:
            for line in existing:
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                digest = sha256_digest(obj.get("instruction", "") + obj.get("output", ""))
                seen_hashes.add(digest)
                collected += 1

    if collected >= limit:
        print(f"[bayesian-problems] existing corpus already has {collected} examples")
        return collected

    dataset = load_dataset(
        "quyanh/MAS3301-Bayesian-Statistic",
        split="train",
        streaming=True,
    )

    with output_file.open("a", encoding="utf-8") as writer:
        for example in dataset:
            problem = example.get("problem", "").strip()
            solution = example.get("solution", "").strip()
            if not problem or not solution:
                continue

            digest = sha256_digest(problem + solution)
            if digest in seen_hashes:
                continue

            record = {
                "instruction": "Solve the following Bayesian statistics problem.",
                "input": problem,
                "output": solution,
                "_source": "MAS3301_bayesian_statistic",
                "_category": "bayesian_inference",
            }
            writer.write(json.dumps(record, ensure_ascii=False) + "\n")

            seen_hashes.add(digest)
            collected += 1

            if collected % 500 == 0:
                print(f"[bayesian-problems] collected {collected} problems")

            if collected >= limit:
                break

    return collected


def main() -> None:
    print("=" * 80)
    print(" ADVANCED SCIENCE CORPUS DOWNLOAD")
    print("=" * 80)

    stream_arxiv_topics()

    bayesian_total = ingest_bayesian_problem_sets()
    print(f"[bayesian-problems] final count: {bayesian_total}")

    print("=" * 80)
    print(" DOWNLOAD COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
