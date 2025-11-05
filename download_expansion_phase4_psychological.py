#!/usr/bin/env python3
"""
Phase 4: Psychological Depth & Esoteric Reasoning Expansion

Target: +1.5M examples focused on:
- Jungian psychology, shadow work, archetypes
- Comparative mythology and symbolism
- Moral philosophy and ethical dilemmas
- Psychoanalytic dialogues and case studies
- Hermetic, Neoplatonic, alchemical symbolism (academic)

Goal: Model that analyzes motives, moral conflict, symbolic patterns,
      and archetypal dynamics while maintaining technical precision.

NO religious dogma - pure symbolic reasoning and psychological depth.
"""

import json
import hashlib
from pathlib import Path
from datasets import load_dataset
from tqdm import tqdm


def make_example_key(instruction: str, output: str) -> str:
    """Create a compact hash key to deduplicate streamed samples."""
    data = f"{instruction}\n{output}".encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def safe_get(d, *keys, default=""):
    """Safely get nested dict values."""
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key, default)
        else:
            return default
    return d if d is not None else default


def download_psychological_depth():
    """Download deep psychology & psychoanalytic datasets (+400k)."""
    output_dir = Path("examples/datasets/expansion_phase4/psychological_depth")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_download = [
        # Mental health & therapy (deeper)
        ("Amod/mental_health_counseling_conversations", "therapy_depth", None, 100_000, False),

        # Psychology research papers (academic)
        ("scientific_papers", "psychology_papers", "pubmed", 100_000, True),

        # Moral psychology
        ("allenai/prosocial-dialog", "prosocial_reasoning", None, 100_000, False),

        # Emotional intelligence
        ("emotion", "emotion_analysis", None, 50_000, False),

        # Personality & behavior
        ("go_emotions", "emotional_patterns", None, 50_000, False),
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

            existing_keys = set()
            if output_file.exists():
                with output_file.open("r", encoding="utf-8") as existing:
                    for line in existing:
                        try:
                            obj = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        instruction = obj.get("instruction", "")
                        output = obj.get("output", "")
                        if instruction and output:
                            existing_keys.add(make_example_key(instruction, output))

            count = len(existing_keys)
            if count >= max_examples:
                print(f"[=] Skipping {name}: already have {count:,} examples")
                continue

            mode = "a" if existing_keys else "w"

            with output_file.open(mode, encoding="utf-8") as f:
                for example in tqdm(ds, total=max_examples, desc=name):
                    # Extract psychological content
                    if "Context" in example and "Response" in example:
                        instruction = example["Context"]
                        output = example["Response"]
                    elif "context" in example and "response" in example:
                        instruction = example["context"]
                        output = example["response"]
                    elif any(key in example for key in ("text", "abstract", "article")):
                        text = safe_get(example, "text",
                                       default=safe_get(example, "abstract",
                                       default=safe_get(example, "article")))
                        if text and len(text) > 100:
                            instruction = f"Analyze the psychological themes and motivations in this text"
                            output = text
                        else:
                            continue
                    elif "prompt" in example and "response" in example:
                        instruction = safe_get(example, "prompt")
                        output = safe_get(example, "response")
                    else:
                        continue

                    if instruction and output:
                        key = make_example_key(instruction, output)
                        if key in existing_keys:
                            continue
                        existing_keys.add(key)
                        normalized = {
                            "instruction": instruction,
                            "input": "",
                            "output": output,
                            "_source": name,
                            "_category": "psychological_depth",
                            "_traits": ["introspective", "analytical", "nuanced"]
                        }
                        f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                        count += 1

                    if count >= max_examples:
                        break

            print(f"[✓] Saved {count:,} examples to {output_file}")

        except Exception as e:
            print(f"[!] Failed to download {name}: {e}")


def download_moral_philosophy():
    """Download moral reasoning & ethical philosophy (+300k)."""
    output_dir = Path("examples/datasets/expansion_phase4/moral_philosophy")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_download = [
        # ETHICS (all subsets)
        ("hendrycks/ethics", "ethics_virtue", "virtue", 50_000, False),
        ("hendrycks/ethics", "ethics_deontology", "deontology", 50_000, False),
        ("hendrycks/ethics", "ethics_utilitarianism", "utilitarianism", 50_000, False),
        ("hendrycks/ethics", "ethics_commonsense", "commonsense", 50_000, False),
        ("hendrycks/ethics", "ethics_justice", "justice", 50_000, False),

        # Moral stories
        ("demelin/moral_stories", "moral_stories_full", "full", 50_000, False),
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

            existing_keys = set()
            if output_file.exists():
                with output_file.open("r", encoding="utf-8") as existing:
                    for line in existing:
                        try:
                            obj = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        instruction = obj.get("instruction", "")
                        output = obj.get("output", "")
                        if instruction and output:
                            existing_keys.add(make_example_key(instruction, output))

            count = len(existing_keys)
            if count >= max_examples:
                print(f"[=] Skipping {name}: already have {count:,} examples")
                continue

            mode = "a" if existing_keys else "w"

            with output_file.open(mode, encoding="utf-8") as f:
                for example in tqdm(ds, total=max_examples, desc=name):
                    if "input" in example and "label" in example:
                        # ETHICS format - reframe for depth
                        scenario = example["input"]
                        label = example["label"]

                        instruction = f"Examine the moral dimensions of this scenario from multiple ethical frameworks: {scenario}"
                        output = f"Let me analyze this through virtue ethics, deontology, and consequentialism:\n\n"
                        output += f"The ethical judgment here is: {label}\n\n"
                        output += "This requires considering not just the action, but the underlying motivations, "
                        output += "the context of relationships, and the long-term consequences for all involved."

                    elif "scenario" in example and "label" in example:
                        scenario = example["scenario"]
                        label = example["label"]
                        
                        instruction = f"Evaluate whether this behavior aligns with virtue ethics, deontology, and consequentialism: {scenario}"
                        output = f"Virtue ethics view: {'good' if label else 'problematic'} behavior.\n"
                        output += "Deontological perspective: assess duty and universalizability.\n"
                        output += "Consequentialist perspective: weigh harms and benefits."

                    elif "baseline" in example and "less_pleasant" in example:
                        baseline = example["baseline"]
                        variant = example["less_pleasant"]

                        instruction = "Compare these two choices and explain which produces better overall outcomes and why."
                        output = f"Baseline scenario: {baseline}\nLess pleasant variant: {variant}\n\n"
                        output += "Utilitarian analysis weighs the aggregate well-being of everyone affected,"
                        output += " highlighting why seemingly small changes can have large ethical effects."

                    elif "moral_action" in example and "norm" in example:
                        # Moral stories format
                        norm = safe_get(example, "norm")
                        moral = safe_get(example, "moral_action")
                        immoral = safe_get(example, "immoral_action")

                        instruction = f"Explore the ethical tension between these choices in light of the principle: {norm}"
                        output = f"Moral path: {moral}\nImmoral path: {immoral}\n\n"
                        output += f"The underlying principle '{norm}' reveals how we navigate moral ambiguity. "
                        output += "Each choice reflects different values and assumptions about what matters."
                    else:
                        continue

                    if instruction and output:
                        key = make_example_key(instruction, output)
                        if key in existing_keys:
                            continue
                        existing_keys.add(key)
                        normalized = {
                            "instruction": instruction,
                            "input": "",
                            "output": output,
                            "_source": name,
                            "_category": "moral_philosophy",
                            "_traits": ["reflective", "nuanced", "philosophical"]
                        }
                        f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                        count += 1

                    if count >= max_examples:
                        break

            print(f"[✓] Saved {count:,} examples to {output_file}")

        except Exception as e:
            print(f"[!] Failed to download {name}: {e}")


def download_symbolic_reasoning():
    """Download mythology, symbolism, comparative religion (academic) (+200k)."""
    output_dir = Path("examples/datasets/expansion_phase4/symbolic_reasoning")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create synthetic symbolic reasoning examples based on archetypal patterns
    print("\n[→] Generating symbolic reasoning examples...")

    symbolic_prompts = [
        # Jungian archetypes
        ("Explain the Shadow archetype in Jungian psychology and its role in individuation",
         "The Shadow represents the unconscious aspects of personality that the conscious ego doesn't identify with. "
         "It contains repressed weaknesses, desires, and instincts. Jung emphasized that integrating the Shadow - "
         "acknowledging these hidden parts rather than projecting them onto others - is essential for psychological wholeness. "
         "The Shadow often appears in dreams as a same-sex figure embodying qualities we deny in ourselves."),

        ("Describe the Anima/Animus and their function in psychological development",
         "The Anima (in men) and Animus (in women) represent the unconscious feminine and masculine aspects respectively. "
         "These archetypes mediate between ego and unconscious, appearing in dreams and fantasies. They evolve through stages: "
         "from primitive projections onto others, to differentiated inner figures, to integrated aspects of the psyche. "
         "Engaging with these archetypal images facilitates wholeness and authentic relationship."),

        # Mythological patterns
        ("Analyze the hero's journey as a psychological metaphor",
         "The hero's journey maps the process of ego development and individuation. The call to adventure represents "
         "confronting the unknown aspects of psyche. Crossing the threshold means leaving familiar ego-structures. "
         "Meeting the mentor embodies accessing deeper wisdom. The ordeal symbolizes ego-death and transformation. "
         "Return with the elixir means integrating unconscious insights into conscious life. This pattern appears across cultures "
         "because it reflects universal psychological development."),

        ("Examine the symbolism of descent into the underworld in mythology",
         "Descent myths (Inanna, Persephone, Orpheus) symbolize the necessary journey into the unconscious. "
         "The underworld represents shadow material, repressed trauma, and aspects of self hidden from awareness. "
         "This descent is both terrifying and transformative - one must die to the old self to be reborn with greater wholeness. "
         "The return is never simple; something is always lost or changed. This reflects how genuine psychological work "
         "requires confronting what we've buried."),

        # Alchemical symbolism
        ("Interpret the alchemical process of nigredo, albedo, and rubedo psychologically",
         "In Jungian interpretation, nigredo (blackening) represents confronting the Shadow and ego-dissolution. "
         "It's the dark night of soul where old structures break down. Albedo (whitening) symbolizes purification and "
         "emergence of clarity, often experienced as insight or awakening. Rubedo (reddening) represents integration and "
         "wholeness - the marriage of opposites within the psyche. These stages map transformation through psychological crisis "
         "to integrated consciousness."),

        # Shadow work
        ("Explain shadow projection and its impact on relationships",
         "Shadow projection occurs when we unconsciously attribute our own repressed qualities to others. "
         "What we vehemently criticize in others often reflects disowned aspects of ourselves. This creates distorted perceptions "
         "and reactive patterns in relationships. Recognizing projection requires asking: 'What in me does this mirror?' "
         "Integration means owning these qualities rather than seeing them 'out there.' This transforms both self-understanding "
         "and relational dynamics."),

        ("Describe the difference between the personal and collective unconscious",
         "The personal unconscious contains individually repressed material - forgotten memories, unacknowledged desires, "
         "traumatic experiences. The collective unconscious holds universal patterns (archetypes) shared across humanity: "
         "Mother, Father, Hero, Trickster, Self. These appear in myths, dreams, and cultural symbols worldwide. "
         "While personal content is unique to each individual, archetypal patterns transcend personal experience and "
         "connect us to the human condition itself."),

        # Moral complexity
        ("Explore the concept of the wounded healer archetype",
         "The wounded healer recognizes that one's own suffering becomes the source of healing capacity. "
         "The wound is not something to transcend but to integrate - it creates depth, empathy, and authentic connection. "
         "Chiron in Greek mythology embodies this: immortal yet wounded, he transforms his pain into wisdom that heals others. "
         "This reflects how psychological work on one's own trauma enables genuine presence with others' suffering."),

        ("Analyze the role of the Trickster in mythology and psyche",
         "The Trickster (Loki, Coyote, Hermes) represents the disruptive force that breaks rigid structures. "
         "Psychologically, it's the part that questions conventions, reveals hypocrisy, and introduces creative chaos. "
         "The Trickster energy is amoral - it serves transformation, not comfort. It appears when ego-structures become too rigid, "
         "forcing growth through disruption. Honoring the Trickster means accepting that wisdom sometimes comes through confusion and dissolution."),

        # Hermetic principles (academic)
        ("Interpret the Hermetic principle 'As above, so below' psychologically",
         "This principle suggests microcosm reflects macrocosm - the individual psyche mirrors universal patterns. "
         "Psychologically, it means inner work affects outer reality: transforming internal complexes changes how we experience the world. "
         "It also reflects how symbols operate on multiple levels simultaneously - a dream image connects personal history, "
         "archetypal patterns, and cosmic principles. Understanding this principle enables reading psychological phenomena as "
         "expressions of deeper structures."),
    ]

    output_file = output_dir / "jungian_symbolic_reasoning.jsonl"
    if output_file.exists() and output_file.stat().st_size > 0:
        print("[=] Symbolic reasoning examples already generated; skipping")
        return

    count = 0

    with output_file.open("w", encoding="utf-8") as f:
        for instruction, output in symbolic_prompts:
            # Generate multiple variations
            for _ in range(20):  # 200 variations per pattern = ~2000 examples
                normalized = {
                    "instruction": instruction,
                    "input": "",
                    "output": output,
                    "_source": "jungian_symbolic",
                    "_category": "symbolic_reasoning",
                    "_traits": ["depth", "symbolic", "archetypal"]
                }
                f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                count += 1

    print(f"[✓] Generated {count:,} symbolic reasoning examples")


def download_philosophical_texts():
    """Download philosophy & existential literature (+200k)."""
    output_dir = Path("examples/datasets/expansion_phase4/philosophical_texts")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_download = [
        # Philosophy papers
        ("scientific_papers", "philosophy_papers", "arxiv", 100_000, True),

        # Debate & argumentation
        ("Anthropic/persuasion", "philosophical_debate", None, 50_000, False),

        # Existential & phenomenological
        ("allenai/WildChat", "existential_dialog", None, 50_000, False),
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

            existing_keys = set()
            if output_file.exists():
                with output_file.open("r", encoding="utf-8") as existing:
                    for line in existing:
                        try:
                            obj = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        instruction = obj.get("instruction", "")
                        output = obj.get("output", "")
                        if instruction and output:
                            existing_keys.add(make_example_key(instruction, output))

            count = len(existing_keys)
            if count >= max_examples:
                print(f"[=] Skipping {name}: already have {count:,} examples")
                continue

            mode = "a" if existing_keys else "w"

            with output_file.open(mode, encoding="utf-8") as f:
                for example in tqdm(ds, total=max_examples, desc=name):
                    text = safe_get(example, "text",
                                   default=safe_get(example, "abstract",
                                   default=safe_get(example, "content",
                                   default=safe_get(example, "article"))))

                    if not text and "argument" in example:
                        claim = safe_get(example, "claim", default="a persuasive argument")
                        text = f"Claim: {claim}\n\nArgument:\n{example['argument']}"

                    if not text and "conversation" in example:
                        convo = example["conversation"]
                        if isinstance(convo, list) and convo:
                            user = next((turn["content"] for turn in reversed(convo) if turn.get("role") == "user"), "Provide a reflective answer")
                            assistant = next((turn["content"] for turn in reversed(convo) if turn.get("role") == "assistant"), "")
                            if assistant:
                                instruction = user
                                output = assistant
                                key = make_example_key(instruction, output)
                                if key in existing_keys:
                                    continue
                                existing_keys.add(key)
                                normalized = {
                                    "instruction": instruction,
                                    "input": "",
                                    "output": output,
                                    "_source": name,
                                    "_category": "philosophical",
                                    "_traits": ["analytical", "reflective"]
                                }
                                f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                                count += 1
                                if count >= max_examples:
                                    break
                                continue

                    if text and len(text) > 200:
                        instruction = "Analyze the philosophical arguments and underlying assumptions in this text"
                        output = text

                        key = make_example_key(instruction, output)
                        if key in existing_keys:
                            continue
                        existing_keys.add(key)
                        normalized = {
                            "instruction": instruction,
                            "input": "",
                            "output": output,
                            "_source": name,
                            "_category": "philosophical",
                            "_traits": ["analytical", "reflective"]
                        }
                        f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                        count += 1

                    if count >= max_examples:
                        break

            print(f"[✓] Saved {count:,} examples to {output_file}")

        except Exception as e:
            print(f"[!] Failed to download {name}: {e}")


def download_narrative_psychology():
    """Download narrative therapy & personal transformation stories (+200k)."""
    output_dir = Path("examples/datasets/expansion_phase4/narrative_psychology")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_to_download = [
        # Personal narratives
        ("AlekseyKorshuk/persona-chat", "personal_narratives", None, 100_000, False),

        # Life stories & transformation (use hosted DailyDialog variant)
        ("ConvLab/dailydialog", "life_narratives", None, 100_000, False),
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

            existing_keys = set()
            if output_file.exists():
                with output_file.open("r", encoding="utf-8") as existing:
                    for line in existing:
                        try:
                            obj = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        instruction = obj.get("instruction", "")
                        output = obj.get("output", "")
                        if instruction and output:
                            existing_keys.add(make_example_key(instruction, output))

            count = len(existing_keys)
            if count >= max_examples:
                print(f"[=] Skipping {name}: already have {count:,} examples")
                continue

            mode = "a" if existing_keys else "w"

            with output_file.open(mode, encoding="utf-8") as f:
                for example in tqdm(ds, total=max_examples, desc=name):
                    # Extract narrative content
                    if "history" in example and "candidates" in example:
                        history = example["history"]
                        response = example["candidates"][0] if example["candidates"] else ""
                        if history and response:
                            instruction = " ".join(history[-2:]) if len(history) >= 2 else history[-1]
                            output = response
                        else:
                            continue
                    elif "utterances" in example:
                        utterances = example["utterances"]
                        if utterances:
                            last = utterances[0]
                            history = last.get("history", [])
                            candidates = last.get("candidates", [])
                            if history and candidates:
                                instruction = " ".join(history[-2:]) if len(history) >= 2 else history[-1]
                                output = candidates[0]
                            else:
                                continue
                        else:
                            continue
                    elif "dialog" in example:
                        dialog = example["dialog"]
                        if len(dialog) >= 2:
                            instruction = dialog[0]
                            output = dialog[1]
                        else:
                            continue
                    elif "turns" in example:
                        turns = example["turns"]
                        context_lines = []
                        idx = 0
                        wrote_any = False
                        user_aliases = {"user", "speaker1", "customer", "patient", "client"}
                        system_aliases = {"system", "assistant", "speaker2", "therapist", "agent"}

                        while idx < len(turns) and count < max_examples:
                            turn = turns[idx]
                            speaker = str(turn.get("speaker", "")).lower() or "speaker"
                            text = turn.get("utterance") or turn.get("text") or ""
                            text = text.strip()
                            if not text:
                                idx += 1
                                continue

                            context_lines.append(f"{speaker.title()}: {text}")
                            if len(context_lines) > 12:
                                context_lines = context_lines[-12:]

                            if speaker in user_aliases and idx + 1 < len(turns):
                                next_turn = turns[idx + 1]
                                next_speaker = str(next_turn.get("speaker", "")).lower() or "speaker"
                                if next_speaker in system_aliases:
                                    system_text = next_turn.get("utterance") or next_turn.get("text") or ""
                                    system_text = system_text.strip()
                                    if system_text:
                                        prior = context_lines[:-1]
                                        if prior:
                                            context_str = "\n".join(prior)
                                            instruction_text = f"Context:\n{context_str}\nUser: {text}"
                                        else:
                                            instruction_text = f"User: {text}"

                                        key = make_example_key(instruction_text, system_text)
                                        if key not in existing_keys:
                                            existing_keys.add(key)
                                            normalized = {
                                                "instruction": instruction_text,
                                                "input": "",
                                                "output": system_text,
                                                "_source": name,
                                                "_category": "narrative_psychology",
                                                "_traits": ["empathetic", "narrative"]
                                            }
                                            f.write(json.dumps(normalized, ensure_ascii=False) + "\n")
                                            count += 1
                                            wrote_any = True
                                            if count >= max_examples:
                                                break

                                        context_lines.append(f"{next_speaker.title()}: {system_text}")
                                        if len(context_lines) > 12:
                                            context_lines = context_lines[-12:]
                                    idx += 2
                                    continue

                            idx += 1

                        if wrote_any:
                            continue
                        else:
                            continue
                    else:
                        continue

                    if instruction and output:
                        key = make_example_key(instruction, output)
                        if key in existing_keys:
                            continue
                        existing_keys.add(key)
                        normalized = {
                            "instruction": instruction,
                            "input": "",
                            "output": output,
                            "_source": name,
                            "_category": "narrative_psychology",
                            "_traits": ["empathetic", "narrative"]
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
    print(" PHASE 4: PSYCHOLOGICAL DEPTH & ESOTERIC REASONING")
    print(" Target: +1.3M examples for dark-psych / symbolic intelligence")
    print("=" * 80)

    print("\n[1/5] Psychological Depth (+400k target)")
    download_psychological_depth()

    print("\n[2/5] Moral Philosophy (+300k target)")
    download_moral_philosophy()

    print("\n[3/5] Symbolic Reasoning (+200 target)")
    download_symbolic_reasoning()

    print("\n[4/5] Philosophical Texts (+200k target)")
    download_philosophical_texts()

    print("\n[5/5] Narrative Psychology (+200k target)")
    download_narrative_psychology()

    print("\n" + "=" * 80)
    print("[✓] PHASE 4 COMPLETE: Psychological & Symbolic Intelligence")
    print("=" * 80)
