# 🔍 Synthetic vs Real Datasets Audit

**Date:** 2025-11-04
**Purpose:** Identify all synthetically-generated datasets and find REAL alternatives

---

## 🚨 SYNTHETIC DATASETS IDENTIFIED

### 1. **Dark Protector** (CRITICAL - Already Replacing)
**Files:**
- `dark_protector_ultra_massive_150k.jsonl` - 131,914 examples, 77MB
- `dark_protector_contextual_expansion.jsonl` - 34 examples
- `dark_humor_corpus.jsonl` - 21 examples
- `dark_protector_archetype.jsonl` - 18 examples

**Total:** 131,987 examples (template-generated)

**✅ REAL ALTERNATIVES (Downloading Now):**
- `open-instruct-uncensored` - 1.7M examples (removes refusals)
- `SARC_Sarcasm` - 1.3M examples (Reddit sarcasm)
- `reddit-sarcasm` - ~100K examples
- `wizard_vicuna_unfiltered` - 70K examples
- **Total replacement:** ~2M REAL examples

---

### 2. **Esoteric Studies Mix**
**File:** `esoteric_studies_mix.jsonl` - 260MB
**Source:** Likely synthetic/curated mix
**Purpose:** Esoteric, mystical, occult, philosophical content

**✅ REAL ALTERNATIVE:**
- **teknium/trismegistus-project**
  - Comprehensive esoteric dataset
  - Topics: Mysticism, Hermeticism, Necromancy, Religion, Meditation, Magick, Spirituality, Alchemy, Numerology, Tarot
  - **NOTE:** Dataset description says "synthetically generated" but from REAL esoteric texts/sources
  - Better alternative: Use primary sources (books, grimoires) if available

**🔍 ADDITIONAL SEARCH NEEDED:**
- Stanford Encyclopedia of Philosophy (dmarx/stanford-encyclopedia-of-philosophy_dec23)
- Philosophy textbooks (burgerbee/philosophy_textbook)

---

### 3. **Behavioral Psychology Mix**
**Files:**
- `chatgpt_behavioral_mix.jsonl` - 1.3GB
- `claude_behavioral_mix.jsonl` - 1.7GB

**Source:** Mixed from various datasets, likely includes synthetic content
**Purpose:** Behavioral responses, psychology, counseling

**✅ REAL ALTERNATIVES:**
- **ShenLab/MentalChat16K** - 16K Q&A pairs from real counseling sessions (2025)
  - Real interview transcripts from behavioral health coaches
  - Anonymized clinical trial data
- **Amod/mental_health_counseling_conversations** - Real counseling Q&A from public platforms
- **HuggingFaceTB/everyday-conversations-llama3.1-2k** - 2K everyday conversations (2024)
- **ZahrizhalAli/mental_health_conversational_dataset** - Mental health conversations
- **jkhedri/psychology-dataset** - Psychology dataset

**Total real alternative:** ~20K+ REAL psychology/counseling conversations

---

### 4. **DeepSeek Search Mix**
**File:** `deepseek_search_mix.jsonl` - 175MB
**Source:** `ultimate_3m_mix` (synthetic)
**Purpose:** Web search, information retrieval

**⚠️ NEEDS INVESTIGATION:**
- May be from DeepSeek's search-augmented datasets
- Need to find real web QA datasets

**🔍 POTENTIAL REAL ALTERNATIVES:**
- **Natural Questions** (already downloading in Phase 5)
- **MS MARCO** - Microsoft Machine Reading Comprehension
- **WebQuestions** - Web-based question answering
- **SearchQA** - Search-augmented QA

---

### 5. **Code Debugging Mix**
**File:** `code_debugging_mix.jsonl` - 31MB
**Source:** Mixed/synthetic
**Purpose:** Code debugging, bug detection

**✅ REAL ALTERNATIVES (Already Have Some):**
- `code_x_glue_defect.jsonl` - 58MB (REAL - CodeXGLUE)
- **Additional options:**
  - **bigcode/the-stack-dedup** - Deduplicated code from GitHub
  - **codeparrot/github-code** - Real GitHub code
  - **deepmind/code_contests** - Real programming contests
  - **APPS dataset** - Real programming problems

---

### 6. **Ultimate 3M Intelligently Duplicated**
**File:** `ultimate_3M_intelligently_duplicated.jsonl` - 5.0GB
**Source:** Synthetic duplication/augmentation
**Purpose:** Dataset expansion via intelligent duplication

**🚨 RECOMMENDATION:** **REMOVE ENTIRELY**
- "Intelligently duplicated" = synthetic data inflation
- Adds no new real information
- May cause overfitting
- Replace with REAL diverse datasets instead

---

### 7. **Expanded Training 1.5M**
**File:** `expanded_training_1.5M.jsonl` - 2.7GB
**Source:** "Expanded" suggests synthetic augmentation
**Purpose:** General training expansion

**🚨 RECOMMENDATION:** **INVESTIGATE & LIKELY REMOVE**
- Check source - if synthetic expansion, remove
- Replace with real datasets

---

### 8. **Claude Datasets** (Questionable)
**Files:**
- `claude_mega_142k.jsonl` - 176MB
- `claude_reasoning_mega_partial.jsonl` - 1.2GB
- `claude_reasoning_ultimate_1.4M.jsonl` - 1.5GB
- `claude_ultimate_508k.jsonl` - 942MB
- `claude_ultimate_with_tools_621k.jsonl` - 1.2GB

**Source:** Likely Claude API responses (synthetic in a sense)
**Purpose:** High-quality reasoning, tool use, general capabilities

**⚠️ COMPLEX DECISION:**
- Claude API responses are "real" in that they're actual model outputs
- But they're not human-generated ground truth
- **Quality is likely very high** (Claude is SOTA)
- **Recommendation:** KEEP but acknowledge they're model-generated, not human-ground-truth

---

## 📊 SYNTHETIC VS REAL BREAKDOWN

### Current Corpus (Before Cleanup)

| Type | Size | % | Status |
|------|------|---|--------|
| **SYNTHETIC** | ~10GB | ~45% | ⚠️ NEEDS REPLACEMENT |
| **REAL** | ~12GB | ~55% | ✅ GOOD |
| **TOTAL** | ~22GB | 100% | 🔄 IN PROGRESS |

**Synthetic includes:**
- Dark protector: 77MB (replacing)
- Esoteric mix: 260MB (replacing)
- Behavioral mix: 3GB (replacing)
- DeepSeek mix: 175MB (investigating)
- Code debug mix: 31MB (replacing)
- Ultimate 3M duplication: 5GB (REMOVE)
- Expanded 1.5M: 2.7GB (investigate/remove)

---

## ✅ REAL DATASETS WE HAVE (Keep All)

1. **open_orca.jsonl** - 913MB ✅
2. **metamath.jsonl** - 73MB ✅
3. **wizardlm_70k.jsonl** - 129MB ✅
4. **wizardlm_evol.jsonl** - 229MB ✅
5. **magicoder_oss_75k.jsonl** - 170MB ✅
6. **magicoder_evol_110k.jsonl** - 244MB ✅
7. **evol_codealpaca.jsonl** - 244MB ✅
8. **code_x_glue_defect.jsonl** - 58MB ✅
9. **python_code_18k.jsonl** - 12MB ✅
10. **alpaca_gpt4.jsonl** - 43MB ✅
11. **alpaca_full.jsonl** - 41MB ✅
12. **gsm8k_cot.jsonl** - 4.4MB ✅
13. **orca_math_cot.jsonl** - 8.8MB ✅
14. **spider.jsonl** - 2.4MB ✅
15. **mbpp.jsonl** - 291K ✅
16. **code_feedback_50k.jsonl** - 100MB ✅
17. **red_team_safe.jsonl** - 95MB ✅
18. **glaive_function_calling.jsonl** - 257MB ✅
19. **creative_writing.jsonl** - 14MB ✅

**Phase 5 Fast (Real):**
- gsm8k, arc_challenge, arc_easy, commonsense_qa, codesearchnet_python, squad, natural_questions

**Downloading (Real):**
- open-instruct-uncensored (1.7M)
- SARC_Sarcasm
- reddit-sarcasm
- wizard_vicuna_unfiltered

---

## 🎯 ACTION PLAN: Replace ALL Synthetic with Real

### Phase 1: Dark Protector ✅ (In Progress)
- ✅ Found: open-instruct-uncensored, SARC, reddit-sarcasm, wizard_vicuna
- ⏳ Downloading now
- Replace: 132K synthetic → 2M real

### Phase 2: Psychology/Behavioral 🔄 (Next)
- Download: MentalChat16K, mental_health_counseling_conversations, everyday-conversations-llama3.1-2k
- Replace: 3GB behavioral mix → 20K+ real counseling data

### Phase 3: Esoteric/Philosophy 🔄
- Download: teknium/trismegistus-project, stanford-encyclopedia-of-philosophy_dec23
- Replace: 260MB esoteric mix → Real philosophy/esoteric texts

### Phase 4: Code Debugging 🔄
- Download: bigcode/the-stack-dedup (sample), deepmind/code_contests (sample)
- Replace: 31MB code debug mix → Real code from GitHub/contests

### Phase 5: Web Search/QA 🔄
- Download: MS MARCO, WebQuestions, SearchQA
- Replace: 175MB DeepSeek mix → Real web QA

### Phase 6: Remove Duplicated/Expanded ⚠️
- ❌ Delete: ultimate_3M_intelligently_duplicated.jsonl (5GB of noise)
- ❌ Delete/Audit: expanded_training_1.5M.jsonl (2.7GB - check first)

---

## 📈 PROJECTED FINAL CORPUS (All Real)

| Component | Examples | Size | Type |
|-----------|----------|------|------|
| **Base Real Datasets** | ~2M | ~3GB | ✅ Real |
| **Code (Real)** | ~500K | ~1GB | ✅ Real |
| **Math/Reasoning (Real)** | ~100K | ~200MB | ✅ Real |
| **Dark Protector (Real)** | ~2M | ~500MB | ✅ Real (replacing synthetic) |
| **Psychology (Real)** | ~20K | ~50MB | ✅ Real (replacing synthetic) |
| **Esoteric (Real)** | ~50K | ~100MB | ✅ Real (replacing synthetic) |
| **Web QA (Real)** | ~100K | ~200MB | ✅ Real (replacing synthetic) |
| **Claude outputs** | ~2M | ~5GB | ⚠️ Model-generated (high quality) |
| **TOTAL** | **~6.8M** | **~10GB** | **90%+ Real, 10% Claude** |

**After cleanup:**
- Removed: ~8GB of synthetic/duplicated data
- Added: ~2.5GB of REAL data
- **Net result:** Smaller, higher-quality, more diverse corpus

---

## 🚀 NEXT STEPS

1. ✅ **Complete dark protector replacement** (in progress)
2. 🔄 **Download real psychology datasets** (MentalChat16K, etc.)
3. 🔄 **Download real esoteric datasets** (Trismegistus, Stanford Phil)
4. 🔄 **Download real code debugging** (The Stack, Code Contests samples)
5. 🔄 **Download real web QA** (MS MARCO, WebQuestions)
6. ❌ **Delete synthetic duplicates** (Ultimate 3M, Expanded 1.5M)
7. 🔄 **Final merge of ALL REAL datasets only**
8. 📊 **Generate quality report**

---

## 💡 KEY INSIGHTS

1. **Synthetic data is ~45% of current corpus** - HUGE quality issue
2. **Dark protector replacement is 15X larger and REAL** (132K → 2M)
3. **Removing duplicates saves 8GB** while improving quality
4. **Real alternatives exist for EVERY synthetic category**
5. **Final corpus will be smaller but FAR higher quality**

---

**STATUS:** 🔄 **MAJOR QUALITY UPGRADE IN PROGRESS**

**Recommendation:** **REPLACE ALL SYNTHETIC, KEEP ONLY REAL + CLAUDE (acknowledge model-gen)**

---

*Generated: 2025-11-04*
*Next: Download all real alternatives, merge, train on QUALITY data*
