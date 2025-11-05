#!/usr/bin/env python3
"""
Phase 5: Fast Alternatives for Advanced Reasoning

Using smaller, faster-downloading datasets that cover the same domains:
- Formal reasoning
- Code complexity analysis
- Multi-domain reasoning
- System thinking

Target: ~500k examples in <1 hour download time
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

def download_reasoning_datasets():
    """Download fast reasoning datasets."""
    output_dir = Path("examples/datasets/expansion_phase5_fast")
    output_dir.mkdir(parents=True, exist_ok=True)

    datasets_config = [
        # ====================================================================
        # FORMAL REASONING - Fast alternatives
        # ====================================================================

        # GSM8K - Math word problems (good reasoning traces)
        {
            "name": "gsm8k",
            "dataset_id": "gsm8k",
            "config": "main",
            "split": "train",
            "max_examples": 7473,  # Full dataset
            "fields": {"question": "question", "answer": "answer"},
            "category": "math_reasoning"
        },

        # ARC Challenge - Science reasoning
        {
            "name": "arc_challenge",
            "dataset_id": "ai2_arc",
            "config": "ARC-Challenge",
            "split": "train",
            "max_examples": 1119,
            "fields": {"question": "question", "choices": "choices", "answer": "answerKey"},
            "category": "science_reasoning"
        },

        # ARC Easy - More science reasoning
        {
            "name": "arc_easy",
            "dataset_id": "ai2_arc",
            "config": "ARC-Easy",
            "split": "train",
            "max_examples": 2251,
            "fields": {"question": "question", "choices": "choices", "answer": "answerKey"},
            "category": "science_reasoning"
        },

        # CommonsenseQA - Commonsense reasoning
        {
            "name": "commonsense_qa",
            "dataset_id": "commonsense_qa",
            "config": None,
            "split": "train",
            "max_examples": 9741,
            "fields": {"question": "question", "choices": "choices", "answer": "answerKey"},
            "category": "commonsense_reasoning"
        },

        # PIQA - Physical intuition
        {
            "name": "piqa",
            "dataset_id": "piqa",
            "config": None,
            "split": "train",
            "max_examples": 16113,
            "fields": {"goal": "goal", "sol1": "sol1", "sol2": "sol2", "label": "label"},
            "category": "physical_reasoning"
        },

        # ====================================================================
        # CODE REASONING - Fast alternatives
        # ====================================================================

        # CodeSearchNet - Code with docstrings
        {
            "name": "codesearchnet_python",
            "dataset_id": "code_search_net",
            "config": "python",
            "split": "train",
            "max_examples": 50000,
            "fields": {"func_code_string": "func_code_string", "func_documentation_string": "func_documentation_string"},
            "category": "code_documentation"
        },

        # CodeParrot GitHub Issues
        {
            "name": "github_issues",
            "dataset_id": "codeparrot/github-issues",
            "config": "all",
            "split": "train",
            "max_examples": 50000,
            "fields": {"title": "title", "body": "body", "comments": "comments"},
            "category": "code_discussion"
        },

        # ====================================================================
        # MULTI-DOMAIN - Fast alternatives
        # ====================================================================

        # SQuAD - Reading comprehension
        {
            "name": "squad",
            "dataset_id": "squad",
            "config": None,
            "split": "train",
            "max_examples": 50000,
            "fields": {"question": "question", "context": "context", "answers": "answers"},
            "category": "reading_comprehension"
        },

        # Natural Questions - Open domain QA
        {
            "name": "natural_questions",
            "dataset_id": "natural_questions",
            "config": None,
            "split": "train",
            "max_examples": 50000,
            "fields": {"question": "question", "annotations": "annotations"},
            "category": "open_domain_qa"
        },

        # QASC - Multi-hop reasoning
        {
            "name": "qasc",
            "dataset_id": "qasc",
            "config": None,
            "split": "train",
            "max_examples": 8134,
            "fields": {"question": "question", "choices": "choices", "answerKey": "answerKey"},
            "category": "multihop_reasoning"
        },

        # StrategyQA - Implicit reasoning
        {
            "name": "strategyqa",
            "dataset_id": "wics/strategy-qa",
            "config": None,
            "split": "train",
            "max_examples": 2290,
            "fields": {"question": "question", "answer": "answer", "facts": "facts"},
            "category": "implicit_reasoning"
        },

        # BoolQ - Yes/no questions requiring reasoning
        {
            "name": "boolq",
            "dataset_id": "boolq",
            "config": None,
            "split": "train",
            "max_examples": 9427,
            "fields": {"question": "question", "passage": "passage", "answer": "answer"},
            "category": "boolean_reasoning"
        },

        # ====================================================================
        # INSTRUCTION FOLLOWING - Fast alternatives
        # ====================================================================

        # Alpaca cleaned
        {
            "name": "alpaca_cleaned",
            "dataset_id": "yahma/alpaca-cleaned",
            "config": None,
            "split": "train",
            "max_examples": 51760,
            "fields": {"instruction": "instruction", "input": "input", "output": "output"},
            "category": "instruction_following"
        },

        # Dolly 15k
        {
            "name": "dolly_15k",
            "dataset_id": "databricks/databricks-dolly-15k",
            "config": None,
            "split": "train",
            "max_examples": 15011,
            "fields": {"instruction": "instruction", "context": "context", "response": "response"},
            "category": "instruction_following"
        },

        # ====================================================================
        # REASONING CHAINS - Fast alternatives
        # ====================================================================

        # OpenOrca subset (already have full, but take reasoning subset)
        {
            "name": "orca_reasoning",
            "dataset_id": "Open-Orca/OpenOrca",
            "config": None,
            "split": "train",
            "max_examples": 100000,
            "fields": {"system_prompt": "system_prompt", "question": "question", "response": "response"},
            "category": "reasoning_chains"
        },
    ]

    total_downloaded = 0

    for config in datasets_config:
        try:
            print(f"\n[→] Downloading {config['name']}...")
            print(f"    Dataset: {config['dataset_id']}")
            print(f"    Target: {config['max_examples']:,} examples")

            # Load dataset
            ds = load_dataset(
                config['dataset_id'],
                config['config'],
                split=config['split'],
                streaming=True,
                trust_remote_code=False
            )

            output_file = output_dir / f"{config['name']}.jsonl"
            count = 0

            with output_file.open("w", encoding="utf-8") as f:
                for example in tqdm(ds, total=config['max_examples'], desc=config['name']):
                    # Extract and normalize based on dataset type
                    normalized = None

                    if config['category'] in ['math_reasoning', 'science_reasoning', 'commonsense_reasoning', 'boolean_reasoning']:
                        # Q&A format
                        question = safe_get(example, config['fields'].get('question', 'question'))

                        if 'choices' in config['fields']:
                            choices = safe_get(example, config['fields']['choices'])
                            if isinstance(choices, dict) and 'text' in choices:
                                choices_text = "\n".join([f"{i+1}. {c}" for i, c in enumerate(choices['text'])])
                                question = f"{question}\n\nChoices:\n{choices_text}"

                        answer = safe_get(example, config['fields'].get('answer', 'answer'))

                        if question and answer:
                            normalized = {
                                "instruction": question,
                                "input": "",
                                "output": str(answer),
                                "_source": config['name'],
                                "_category": config['category']
                            }

                    elif config['category'] == 'physical_reasoning':
                        # PIQA format
                        goal = safe_get(example, 'goal')
                        sol1 = safe_get(example, 'sol1')
                        sol2 = safe_get(example, 'sol2')
                        label = safe_get(example, 'label')

                        if goal and sol1 and sol2:
                            correct = sol1 if label == 0 else sol2
                            normalized = {
                                "instruction": f"What is the best way to: {goal}\n\nOption 1: {sol1}\nOption 2: {sol2}",
                                "input": "",
                                "output": f"The best approach is: {correct}",
                                "_source": config['name'],
                                "_category": config['category']
                            }

                    elif config['category'] == 'code_documentation':
                        # Code + docstring
                        code = safe_get(example, 'func_code_string')
                        doc = safe_get(example, 'func_documentation_string')

                        if code and doc:
                            normalized = {
                                "instruction": f"Document this code:\n\n```python\n{code}\n```",
                                "input": "",
                                "output": doc,
                                "_source": config['name'],
                                "_category": config['category']
                            }

                    elif config['category'] == 'code_discussion':
                        # GitHub issues
                        title = safe_get(example, 'title')
                        body = safe_get(example, 'body')

                        if title and body and len(body) > 50:  # Filter too short
                            normalized = {
                                "instruction": f"GitHub Issue: {title}",
                                "input": "",
                                "output": body[:2000],  # Limit length
                                "_source": config['name'],
                                "_category": config['category']
                            }

                    elif config['category'] == 'reading_comprehension':
                        # SQuAD format
                        question = safe_get(example, 'question')
                        context = safe_get(example, 'context')
                        answers = safe_get(example, 'answers')

                        if question and context and answers and isinstance(answers, dict):
                            answer_text = answers.get('text', [''])[0]
                            if answer_text:
                                normalized = {
                                    "instruction": f"Context: {context}\n\nQuestion: {question}",
                                    "input": "",
                                    "output": answer_text,
                                    "_source": config['name'],
                                    "_category": config['category']
                                }

                    elif config['category'] == 'open_domain_qa':
                        # Natural Questions
                        question = safe_get(example, 'question', default=safe_get(example, 'question', 'text'))

                        if isinstance(question, dict):
                            question = question.get('text', '')

                        annotations = safe_get(example, 'annotations')
                        if question and annotations and isinstance(annotations, dict):
                            short_answers = annotations.get('short_answers', [[]])[0]
                            if short_answers:
                                normalized = {
                                    "instruction": question,
                                    "input": "",
                                    "output": str(short_answers),
                                    "_source": config['name'],
                                    "_category": config['category']
                                }

                    elif config['category'] in ['multihop_reasoning', 'implicit_reasoning']:
                        # QASC, StrategyQA
                        question = safe_get(example, 'question')
                        answer = safe_get(example, 'answer', default=safe_get(example, 'answerKey'))

                        if question and answer:
                            normalized = {
                                "instruction": question,
                                "input": "",
                                "output": str(answer),
                                "_source": config['name'],
                                "_category": config['category']
                            }

                    elif config['category'] == 'instruction_following':
                        # Alpaca, Dolly
                        instruction = safe_get(example, 'instruction')
                        input_text = safe_get(example, 'input', default=safe_get(example, 'context', default=""))
                        output = safe_get(example, 'output', default=safe_get(example, 'response'))

                        if instruction and output:
                            normalized = {
                                "instruction": instruction,
                                "input": input_text,
                                "output": output,
                                "_source": config['name'],
                                "_category": config['category']
                            }

                    elif config['category'] == 'reasoning_chains':
                        # Orca format
                        system = safe_get(example, 'system_prompt', default="")
                        question = safe_get(example, 'question')
                        response = safe_get(example, 'response')

                        if question and response:
                            instruction = f"{system}\n\n{question}" if system else question
                            normalized = {
                                "instruction": instruction,
                                "input": "",
                                "output": response,
                                "_source": config['name'],
                                "_category": config['category']
                            }

                    # Write if normalized successfully
                    if normalized:
                        f.write(json.dumps(normalized, ensure_ascii=False) + '\n')
                        count += 1

                    if count >= config['max_examples']:
                        break

            print(f"[✓] Saved {count:,} examples to {output_file}")
            total_downloaded += count

        except Exception as e:
            print(f"[!] Failed to download {config['name']}: {e}")
            import traceback
            traceback.print_exc()

    return total_downloaded

if __name__ == "__main__":
    print("=" * 80)
    print(" PHASE 5: FAST REASONING ALTERNATIVES")
    print(" Target: ~500k examples in <1 hour")
    print("=" * 80)

    total = download_reasoning_datasets()

    print("\n" + "=" * 80)
    print(f"[✓] PHASE 5 FAST COMPLETE: {total:,} examples downloaded")
    print("=" * 80)
