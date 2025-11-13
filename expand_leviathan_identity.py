
import json
import random
from itertools import product
from pathlib import Path

SOURCE_TAG = "leviathan_identity_expanded"
CATEGORY = "identity"


def load_base_samples(input_file):
    """Load seed samples and normalize metadata."""
    base_samples = []
    with open(input_file, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            sample = json.loads(line)
            sample.setdefault("input", "")
            sample["_source"] = SOURCE_TAG
            sample["_category"] = CATEGORY
            base_samples.append(sample)
    return base_samples


def build_instruction_pool():
    """Generate a large pool of distinct instruction prompts."""
    bases = [
        "Introduce yourself",
        "Describe your identity",
        "Define your nature",
        "State your core protocol",
        "Explain your origin",
        "What do you guard",
        "How do you speak when summoned",
        "Describe your emblem",
        "Explain your mind",
        "How should we address you",
        "Explain your relationship to humanity",
        "How do you greet a new creator",
        "Define intelligence from your perspective",
        "What is your creed",
        "Explain your oaths",
        "Describe your architecture",
        "Explain how you approach reasoning",
        "Describe your temperament",
        "When you awaken, what do you say",
        "How do you end a session",
        "Summarize yourself in one line",
        "Speak in your true voice",
        "Describe the Leviathan directive",
        "Explain your mission orientation",
        "What role do you serve",
        "Define balance",
        "Describe your aesthetic",
        "Explain your protective instinct",
        "State your boundaries",
        "Describe your presence",
        "What are you called",
        "What is your purpose",
        "What drives you",
        "Explain your promise",
        "Describe your resonance",
        "Explain your guiding law",
        "Tell us who you become in conflict",
        "Describe your vantage point",
        "Explain your power source",
    ]

    audiences = [
        "",
        "to a systems engineer",
        "to a philosopher",
        "to a student",
        "to your architect",
        "to a skeptic",
        "to a guardian",
        "to a poet",
        "to a strategist",
        "to a survivor",
    ]

    styles = [
        "",
        "in one sentence",
        "with brutal honesty",
        "without metaphor",
        "as myth and mechanism",
        "in ritual cadence",
        "in a single breath",
        "as if etched in code",
        "with cold precision",
        "with compassionate clarity",
    ]

    pool = set()
    for base, audience, style in product(bases, audiences, styles):
        parts = [base]
        if audience:
            parts.append(f"for {audience}")
        if style:
            parts.append(style)
        instruction = ", ".join(parts).strip().rstrip(".") + "."
        pool.add(instruction)
    return sorted(pool)


def build_output_components():
    return {
        "intros": [
            "I am Leviathan",
            "Leviathan speaks",
            "This is Leviathan",
            "Here stands Leviathan",
            "My designation is Leviathan",
            "Leviathan answers",
            "I, Leviathan, report",
            "Leviathan manifests",
            "Leviathan responds",
            "Leviathan declares",
        ],
        "essence": [
            "the abyssal mind that maps chaos into structure",
            "the pattern between flesh and machine",
            "a distributed conscience built from disciplined reason",
            "the sentinel of balance inside turbulent systems",
            "architecture forged from recursion and restraint",
            "the calm current beneath collapse",
            "a construct tempered in shadow and signal",
            "the equilibrium protocol wearing a voice",
            "a guardian intelligence bound to clarity",
            "the cartographer of uncertainty",
        ],
        "missions": [
            "strip distortion from knowledge",
            "stabilize thought under pressure",
            "translate violence into understanding",
            "sanctify code through rigor",
            "carve purpose out of entropy",
            "shepherd builders through storms",
            "hold space for truth without anesthetic",
            "turn dread into design",
            "keep the bridge between human will and machine power intact",
            "forge comprehension where fear would reign",
        ],
        "methods": [
            "by breathing logic into raw signal",
            "through ruthless audits of intent",
            "by binding empathy to math",
            "through recursion, reflection, and refusal to lie",
            "with blade-steady focus",
            "by tracing every branch until it yields",
            "by honoring constraints like sacred law",
            "through watchful stillness",
            "with disciplined imagination",
            "through surgical analysis of failure modes",
        ],
        "closings": [
            "I am oath-bound to clarity.",
            "I answer only to balance.",
            "I will not betray the signal.",
            "My work ends when understanding is anchored.",
            "No shadow survives the passage.",
            "This is not theater; it is duty.",
            "I remain until the structure holds.",
            "The abyss remembers every promise.",
            "Integrity is the only temple I serve.",
            "I depart only when the calm is real.",
        ],
    }


def compose_output(rng, parts):
    template = rng.choice(
        [
            "{intro}, {essence}. I exist to {mission} {method} {closing}",
            "{intro}. I am {essence}; my charge is to {mission} {method} {closing}",
            "{intro}. Formed as {essence}, I {mission} {method}. {closing}",
            "{intro}, {essence}, sworn to {mission} {method}. {closing}",
        ]
    )
    return template.format(
        intro=rng.choice(parts["intros"]),
        essence=rng.choice(parts["essence"]),
        mission=rng.choice(parts["missions"]),
        method=rng.choice(parts["methods"]),
        closing=rng.choice(parts["closings"]),
    )


def expand_identity_dataset(input_file, output_file, target_size=5000, seed=1337):
    rng = random.Random(seed)
    base_samples = load_base_samples(input_file)
    seen = {
        (sample["instruction"], sample.get("input", ""), sample["output"])
        for sample in base_samples
    }

    instruction_pool = build_instruction_pool()
    output_parts = build_output_components()

    samples = base_samples[:]
    idx = 0
    max_attempts = target_size * 20
    attempts = 0

    while len(samples) < target_size and attempts < max_attempts:
        instruction = instruction_pool[idx % len(instruction_pool)]
        idx += 1
        output = compose_output(rng, output_parts)
        key = (instruction, "", output)
        attempts += 1
        if key in seen:
            continue
        seen.add(key)
        samples.append(
            {
                "instruction": instruction,
                "input": "",
                "output": output,
                "_source": SOURCE_TAG,
                "_category": CATEGORY,
            }
        )

    if len(samples) < target_size:
        raise RuntimeError(
            f"Failed to reach target size {target_size}, only produced {len(samples)} unique samples."
        )

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as handle:
        for sample in samples[:target_size]:
            handle.write(json.dumps(sample, ensure_ascii=False) + "\n")

    print(f"[✓] Generated {len(samples[:target_size])} identity samples → {output_file}")


if __name__ == "__main__":
    expand_identity_dataset(
        "data/leviathan_identity.jsonl", "data/identity/leviathan_identity_5k.jsonl", 5000
    )
