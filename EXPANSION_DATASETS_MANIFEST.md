# Dataset Expansion Manifest

## Overview

This document tracks the expansion datasets being downloaded to diversify the training corpus beyond the current 3.4M examples. Target: **~1.5-2M additional unique examples** across 8 categories.

---

## Current Gaps (from analysis)

| Category | Current Count | Target Δ | Target Total |
|----------|--------------|----------|--------------|
| Multi-turn dialog | ~50k | +400k | 450k |
| Reasoning traces | ~148k | +300k | 448k |
| Psychology/emotional | ~50k | +300k | 350k |
| Creative narrative | ~220k | +200k | 420k |
| Code debugging | ~280k | +200k | 480k |
| Tool & API grounding | ~106k | +100k | 206k |
| Factual grounding | ~76k | +100k | 176k |
| Adversarial/moral | ~268k | +100k | 368k |

---

## Datasets Being Downloaded

### 1. Multi-turn Dialog (+400k target)

Teaches social reasoning, tone-shifting, contextual memory.

| Dataset | Source | Est. Size | Purpose |
|---------|--------|-----------|---------|
| ShareGPT Vicuna Unfiltered | `anon8231489123/ShareGPT_Vicuna_unfiltered` | 200k | Multi-turn natural conversations |
| OpenAssistant OASST2 | `OpenAssistant/oasst2` | 100k | High-quality human feedback conversations |
| Anthropic HH-RLHF | `Anthropic/hh-rlhf` | 150k | Helpful/harmless multi-turn dialogs |
| UltraChat | `stingning/ultrachat` | 200k | Large-scale diverse conversations |
| Wizard-Vicuna | `cognitivecomputations/wizard-vicuna-13b-uncensored` | 50k | Instruction-following conversations |

**Total estimated:** ~700k (allows for deduplication)

---

### 2. Reasoning Traces & Inner-Monologue (+300k target)

Teaches *how* to think, not just answers. Step-by-step reasoning.

| Dataset | Source | Est. Size | Purpose |
|---------|--------|-----------|---------|
| CoT Collection | `kaist-ai/CoT-Collection` | 100k | Diverse chain-of-thought examples |
| GSM8K Full | `openai/gsm8k` | 20k | Grade-school math with solutions |
| MathInstruct | `TIGER-Lab/MathInstruct` | 100k | Mathematical reasoning traces |
| Corr2Cause | `causalnlp/corr2cause` | 30k | Causal reasoning |
| DeepMind Math Dataset | `deepmind/math_dataset` | 50k | Algorithmic math problems |
| ReClor | `lucasmccabe/reclor` | 10k | Logical reasoning |

**Total estimated:** ~310k

---

### 3. Psychology & Emotional Introspection (+300k target)

Adds Jungian and "shadow" realism, emotional depth.

| Dataset | Source | Est. Size | Purpose |
|---------|--------|-----------|---------|
| Mental Health Counseling | `Amod/mental_health_counseling_conversations` | 100k | Therapeutic conversation patterns |
| Emotional Support Conversations | `emotional_support_conversations` | 50k | Empathy and support |
| Empathetic Dialogues | `empathetic_dialogues` | 50k | Emotional understanding |
| PsychQA | `abacusai/PsychQA` | 50k | Psychology Q&A |
| Mental Health FAQ | `Amod/mental_health_FAQ` | 20k | Common mental health questions |

**Total estimated:** ~270k

---

### 4. Creative Narrative & Metaphorical Writing (+200k target)

Expands imagination and symbolic reasoning.

| Dataset | Source | Est. Size | Purpose |
|---------|--------|-----------|---------|
| WritingPrompts | `euclaise/writingprompts` | 100k | Creative writing from prompts |
| TinyStories | `roneneldan/TinyStories` | 50k | Short narrative generation |
| Story Generation | `HuggingFaceH4/story_generation` | 30k | Story completion tasks |
| Fictional Fineweb | `Isotonic/fictional_fineweb` | 20k | Fictional conversations |

**Total estimated:** ~200k

---

### 5. Code Debugging & Reasoning (+200k target)

Improves code robustness and self-diagnosis.

| Dataset | Source | Est. Size | Purpose |
|---------|--------|-----------|---------|
| Code Alpaca 20k | `sahil2801/CodeAlpaca-20k` | 20k | Code instruction following |
| Code Contests | `deepmind/code_contests` | 30k | Competitive programming |
| APPS | `codeparrot/apps` | 50k | Diverse coding problems |
| HumanEval-X | `THUDM/humaneval-x` | 10k | Multilingual code evaluation |
| CodeSearchNet | `code_search_net` | 50k | Code search and understanding |
| StackOverflow Questions | `pacovaldez/stackoverflow-questions` | 40k | Real-world debugging |

**Total estimated:** ~200k

---

### 6. Tool & API Grounding (+100k target)

Strengthens external reasoning and function calling.

| Dataset | Source | Est. Size | Purpose |
|---------|--------|-----------|---------|
| XLAM Function Calling 60k | `Salesforce/xlam-function-calling-60k` | 60k | Large-scale function calling |
| APIBank | `APIBank/APIBank` | 20k | API usage patterns |
| RestBench | `Salesforce/restbench` | 10k | REST API interactions |
| Glaive v2 | `glaiveai/glaive-function-calling-v2` | 20k | Function calling variations |

**Total estimated:** ~110k

---

### 7. Factual Grounding & Retrieval (+100k target)

Balances imaginative content with factual accuracy.

| Dataset | Source | Est. Size | Purpose |
|---------|--------|-----------|---------|
| Natural Questions | `natural_questions` | 50k | Real Google search questions |
| TriviaQA | `trivia_qa` | 30k | Trivia and factual recall |
| SQuAD v2 | `squad_v2` | 20k | Reading comprehension |
| HotpotQA | `hotpot_qa` | 20k | Multi-hop reasoning over facts |
| ELI5 | `eli5` | 30k | Explain Like I'm 5 - simplification |

**Total estimated:** ~150k

---

### 8. Adversarial & Moral Dilemmas (+100k target)

Teaches moral flexibility and debate reasoning.

| Dataset | Source | Est. Size | Purpose |
|---------|--------|-----------|---------|
| HH-RLHF Red Team | `Anthropic/hh-rlhf` (red-team) | 50k | Red-teaming attempts |
| ToxiGen | `toxigen/toxigen-data` | 20k | Toxicity detection |
| ETHICS | `hendrycks/ethics` | 15k | Ethical reasoning |
| Moral Stories | `demelin/moral_stories` | 15k | Moral reasoning scenarios |

**Total estimated:** ~100k

---

## Total Estimated Downloads

**Raw total:** ~2.04M examples
**Post-dedup estimated:** ~1.5-1.8M unique examples

Combined with existing 3.4M unique → **~5M total unique examples**

---

## Integration Strategy

1. **Download all datasets** (in progress)
2. **Normalize to Alpaca format** with `_category` tags
3. **Deduplicate globally** using SHA-1 hashing
4. **Rebalance buckets** according to pipeline weights
5. **Tag for curriculum** (optional style tokens)
6. **Merge with existing** datasets for final training corpus

---

## File Organization

```
examples/datasets/expansion/
├── multiturn_dialog/
│   ├── sharegpt_vicuna.jsonl
│   ├── oasst2.jsonl
│   ├── hh_rlhf.jsonl
│   ├── ultrachat.jsonl
│   └── wizard_vicuna.jsonl
├── reasoning_traces/
│   ├── cot_collection.jsonl
│   ├── gsm8k_full.jsonl
│   ├── math_instruct.jsonl
│   ├── corr2cause.jsonl
│   ├── math_dataset.jsonl
│   └── reclor.jsonl
├── psychology_emotional/
│   ├── mental_health_counseling.jsonl
│   ├── emotional_support.jsonl
│   ├── empathetic_dialogues.jsonl
│   ├── psych_qa.jsonl
│   └── mental_health_faq.jsonl
├── creative_narrative/
│   ├── writing_prompts.jsonl
│   ├── tiny_stories.jsonl
│   ├── story_generation.jsonl
│   └── fictional_fineweb.jsonl
├── code_debugging/
│   ├── code_alpaca_20k.jsonl
│   ├── code_contests.jsonl
│   ├── apps.jsonl
│   ├── humaneval_x.jsonl
│   ├── codesearchnet.jsonl
│   └── stackoverflow.jsonl
├── tool_api/
│   ├── xlam_function_calling.jsonl
│   ├── api_bank.jsonl
│   ├── restbench.jsonl
│   └── glaive_v2.jsonl
├── factual_grounding/
│   ├── natural_questions.jsonl
│   ├── trivia_qa.jsonl
│   ├── squad_v2.jsonl
│   ├── hotpot_qa.jsonl
│   └── eli5.jsonl
└── adversarial_moral/
    ├── hh_rlhf_red.jsonl
    ├── toxigen.jsonl
    ├── ethics.jsonl
    └── moral_stories.jsonl
```

---

## Next Steps

1. ✅ Download all datasets (script running)
2. ⏳ Verify downloads and check sizes
3. ⏳ Create deduplication/rebalancing script
4. ⏳ Merge with existing corpus
5. ⏳ Generate final training manifest
6. ⏳ Update profile configs in `build_behavioral_corpora.py`

---

## Notes

- All datasets normalized to Alpaca format: `{instruction, input, output, _source, _category}`
- Category tags enable bucket-based sampling
- Streaming used to handle large datasets efficiently
- Max examples per dataset prevents imbalance
- Deduplication happens at merge time, not download time
