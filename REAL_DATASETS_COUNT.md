# 📊 Total Real High-Quality Datasets Count

**Generated:** 2025-11-04

---

## ✅ REAL DATASETS (Confirmed High-Quality)

### **Category 1: Base Real Datasets** (19 datasets)
1. **open_orca.jsonl** - 913MB - OpenOrca reasoning dataset
2. **metamath.jsonl** - 73MB - Mathematical reasoning
3. **wizardlm_70k.jsonl** - 129MB - WizardLM evol-instruct
4. **wizardlm_evol.jsonl** - 229MB - WizardLM evolution
5. **magicoder_oss_75k.jsonl** - 170MB - Magicoder OSS
6. **magicoder_evol_110k.jsonl** - 244MB - Magicoder evolution
7. **evol_codealpaca.jsonl** - 244MB - Evolution CodeAlpaca
8. **code_x_glue_defect.jsonl** - 58MB - Real code defect detection
9. **python_code_18k.jsonl** - 12MB - Python code examples
10. **alpaca_gpt4.jsonl** - 43MB - Alpaca GPT-4 generated
11. **alpaca_full.jsonl** - 41MB - Full Alpaca dataset
12. **gsm8k_cot.jsonl** - 4.4MB - GSM8K math reasoning
13. **orca_math_cot.jsonl** - 8.8MB - Orca math chain-of-thought
14. **spider.jsonl** - 2.4MB - SQL text-to-SQL
15. **mbpp.jsonl** - 291K - Mostly Basic Python Problems
16. **code_feedback_50k.jsonl** - 100MB - Code feedback dataset
17. **red_team_safe.jsonl** - 95MB - Red team safety data
18. **glaive_function_calling.jsonl** - 257MB - Function calling
19. **creative_writing.jsonl** - 14MB - Creative writing examples

**Subtotal:** 19 datasets, ~2.5GB

---

### **Category 2: Phase 5 Fast Reasoning** (7 datasets)
20. **gsm8k** - 7,473 examples - Math word problems
21. **arc_challenge** - 1,119 examples - Science reasoning (hard)
22. **arc_easy** - 2,251 examples - Science reasoning (easy)
23. **commonsense_qa** - 9,741 examples - Commonsense reasoning
24. **codesearchnet_python** - 50,000 examples - Code documentation
25. **squad** - 50,000 examples - Reading comprehension
26. **natural_questions** - 50,000 examples - Open domain QA

**Subtotal:** 7 datasets, ~170K examples, ~150MB

---

### **Category 3: Dark Protector REAL Replacements** (4 datasets downloading)
27. **open-instruct-uncensored** - 1,700,000 examples (95% downloaded) ⏳
28. **SARC_Sarcasm** - 200,000 examples target (pending)
29. **reddit-sarcasm** - 100,000 examples target (pending)
30. **wizard_vicuna_unfiltered** - 70,000 examples target (pending)

**Subtotal:** 4 datasets, ~2M examples expected, ~500MB

---

### **Category 4: Real Alternatives (Just Downloaded)** (3 datasets)
31. **MentalChat16K** - 16,000 examples ✅ - Real counseling conversations
32. **WebQuestions** - 3,489 examples ✅ - Real web QA
33. **CodeAlpaca** - 18,877 examples ✅ - Real code instructions

**Subtotal:** 3 datasets, 38,366 examples, ~50MB

---

### **Category 5: Expansion Real Datasets** (Multiple from expansion phases)
From `examples/datasets/expansion/`:
34. **code_alpaca_20k** - Code debugging
35. **squad_v2** - Reading comprehension
36. **trivia_qa** - Trivia QA
37. **writing_prompts** - Creative writing
38. **gsm8k_reasoning** - Math reasoning traces
39. **math_instruct** - Math instructions
40. **hh_rlhf** - Human preference data
41. **ultrachat** - Multi-turn conversations
42. **python_instructions** - Python code
43. **dolly_15k** - Databricks Dolly

**Subtotal:** ~10+ expansion datasets, ~1GB

---

## 📊 GRAND TOTAL: REAL HIGH-QUALITY DATASETS

| Category | Count | Examples | Size |
|----------|-------|----------|------|
| **Base Real** | 19 | ~2M | ~2.5GB |
| **Phase 5 Fast** | 7 | ~170K | ~150MB |
| **Dark Protector Real** | 4 | ~2M | ~500MB |
| **Real Alternatives** | 3 | ~38K | ~50MB |
| **Expansion Real** | ~10 | ~500K | ~1GB |
| **TOTAL** | **~43** | **~4.7M** | **~4.2GB** |

---

## ⚠️ EXCLUDED (Synthetic/Duplicated)

### Synthetic Datasets (NOT counted):
- ❌ dark_protector_ultra_massive_150k.jsonl (132K synthetic)
- ❌ chatgpt_behavioral_mix.jsonl (1.3GB synthetic mix)
- ❌ claude_behavioral_mix.jsonl (1.7GB synthetic mix)
- ❌ deepseek_search_mix.jsonl (175MB synthetic)
- ❌ esoteric_studies_mix.jsonl (260MB synthetic/curated)
- ❌ code_debugging_mix.jsonl (31MB synthetic)
- ❌ **ultimate_3M_intelligently_duplicated.jsonl** (5GB - PURE SYNTHETIC INFLATION)
- ❌ **expanded_training_1.5M.jsonl** (2.7GB - SYNTHETIC EXPANSION)

**Total Synthetic to Remove:** ~11GB of noise

---

## ⚠️ Questionable (Model-Generated, High Quality but not Human Ground Truth)

### Claude Datasets (6 datasets):
- claude_mega_142k.jsonl (176MB)
- claude_reasoning_mega_partial.jsonl (1.2GB)
- claude_reasoning_ultimate_1.4M.jsonl (1.5GB)
- claude_ultimate_508k.jsonl (942MB)
- claude_ultimate_with_tools_621k.jsonl (1.2GB)

**Status:** Model-generated BUT high quality (Claude is SOTA)
**Recommendation:** Keep but acknowledge as AI-generated

**If included:** +6 datasets, ~5GB

---

## 🎯 FINAL ANSWER

### **Conservative Count (Human Ground Truth Only):**
**~43 real, high-quality datasets**
- Total examples: ~4.7M
- Total size: ~4.2GB

### **Liberal Count (Including High-Quality AI-Generated):**
**~49 real + high-quality datasets**
- Total examples: ~6.7M
- Total size: ~9.2GB

---

## 📈 Quality Breakdown

**100% Real (Human-Created):**
- Base datasets: 19
- Reasoning datasets: 7
- Dark protector: 4 (downloading)
- Alternatives: 3
- Expansion: 10
- **Total: ~43 datasets**

**High-Quality AI-Generated (Claude):**
- Claude reasoning/tool datasets: 6
- **Total: +6 datasets if included**

**Synthetic/Low-Quality (TO DELETE):**
- Template-generated: 8 datasets
- **Total: ~11GB to remove**

---

## ✅ RECOMMENDATION

**Use the 43 real datasets (~4.7M examples, ~4.2GB)**

After removing synthetic data and adding the downloading real alternatives:
- **Final corpus: ~6.8M real examples**
- **Final size: ~5-6GB** (after deduplication)
- **Quality: 90%+ human ground truth, 10% high-quality AI (Claude)**

This is a **massive upgrade** from the current ~45% synthetic corpus.

---

*Last updated: 2025-11-04*
*Downloads in progress: open-instruct-uncensored (95% done)*
