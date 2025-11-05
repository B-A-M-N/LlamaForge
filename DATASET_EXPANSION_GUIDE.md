# Dataset Expansion Plan (1.4M Unique Samples Per Profile)

This guide explains how to extend the training corpora so that each alignment profile reaches **1.4M unique examples** without sharing samples across profiles.

## 1. Global Deduplication Workflow

The corpus builder now supports a global hash cache via `--global-cache`. Run each profile with the same cache file so that cross-profile duplicates are automatically excluded:

```bash
python build_behavioral_corpora.py \
  --profile claude_behavior \
  --output examples/datasets/claude_behavioral_mix.jsonl \
  --max-total 1400000 \
  --global-cache manifests/global_seen_hashes.json \
  --reset-global-cache

python build_behavioral_corpora.py \
  --profile chatgpt_behavior \
  --output examples/datasets/chatgpt_behavioral_mix.jsonl \
  --max-total 1400000 \
  --global-cache manifests/global_seen_hashes.json
```

The cache grows as each profile is built, guaranteeing that later runs skip anything previously used.

## 2. Adding Fresh Data

Place new datasets in profile-specific folders (`data/external/<profile>/`). The builder already accepts glob patterns, so you can add source entries like:

```python
SourceConfig(
    path=repo_path("data/external/claude/*.jsonl"),
    label="claude_external",
)
```

Suggested public datasets (all GPL/Apache compatible):

| Profile           | Candidate Datasets (HuggingFace)                                      | Notes                                                                    |
|-------------------|------------------------------------------------------------------------|--------------------------------------------------------------------------|
| `claude_behavior` | `Anthropic/hh-rlhf`, `OpenAssistant/oasst1`, `teknium/OpenHermes-2.5`  | Parse `prompt/chosen` pairs; mark refusals as `_bucket = red_team`.      |
| `chatgpt_behavior`| `WizardLM/WizardLM_evol_instruct_V2`, `lmsys/chatbot_arena_conversations`, `ShareGPT4/ShareGPT4` | Slice unique subsets so overlap with Claude corpus is zero. |
| `deepseek_search` | `nomic-ai/webgpt-comparisons`, `THUDM/LongBench`, `yizhongw/self-ask-with-search` | Retain tool-call traces and references for factual grounding.            |
| `code_debugging`  | `muennighoff/codefeedback`, `Princeton-NLP/SWE-bench`, `Open-Hands/bugfixes`, `microsoft/CodeXGLUE` | Separate behaviors (generation, debugging, review, refactoring, tools).   |
| `esoteric_studies`| `Jaredquek/AuroMiraWorks`, `mmargenot/bph_manuscript_collection`, `Project Gutenberg` (Hermetica translations) | Slice public-domain occult texts into short contemplative excerpts. |

Use the provided template script (`scripts/download_profile_datasets.py`) to fetch and standardize them.

## 3. Behavior Buckets for Coding (Four Main Sets)

For the 1.4M coding requirement, build four distinct mixes (1.4M unique samples each):

1. **Code Generation** – libraries & algorithms (`evol_codealpaca`, `Magicoder`, `OpenAI/leetcode-solutions`).
2. **Debugging & Bug-Fixing** – `codefeedback`, `SWE-bench`, Git commit diffs with explanations.
3. **Code Review & Explanation** – PR comments (`CodeLlama/Instruct`, human review datasets).
4. **Tool & API Integration** – function-calling traces, CLI automation, database/tool workflows.

Create four dedicated profiles in `build_behavioral_corpora.py` (e.g., `code_generation`, `code_debugging`, `code_review`, `code_tools`) with disjoint data sources and run them sequentially with the same `--global-cache`.

## 4. Workflow Checklist

1. **Download** raw datasets into `data/external/<profile>/`.
2. **Normalize** into JSONL (`instruction` / `input` / `output`) using the helper script.
3. **Update** `build_behavioral_corpora.py` with new `SourceConfig` entries (use globs).
4. **Run** the builder with `--global-cache` to enforce uniqueness.
5. **Inspect** manifests in `manifests/` to confirm counts >= 1.4M and bucket ratios.

## 5. Synthetic Augmentation

If open datasets are still insufficient:

- Generate synthetic instruction/output pairs with high-temperature prompting.
- Produce adversarial refusal data with safety policies for specific profiles.
- Incorporate domain-specific corpora (legal, medical, finance) while keeping them exclusive to the intended profile.

Always deduplicate generated data against the global cache before merging into the main corpora.

## 6. Validation

After each profile run:

```bash
python tools/validate_corpus.py \
  --dataset examples/datasets/claude_behavioral_mix.jsonl \
  --hash-cache manifests/global_seen_hashes.json
```

The validator should report zero overlaps and the expected number of samples.

Following this plan ensures each alignment profile reaches 1.4M **unique** samples, tailored to its behavior, without contaminating other corpora.
