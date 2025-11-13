# ✅ LEVIATHAN TRAINING SYSTEM - READY STATUS

**System Status**: READY FOR TRAINING
**Date Prepared**: November 10, 2025
**Total Build Time**: Complete corpus pipeline + training setup

---

## 📊 CORPUS SUMMARY

| Metric | Value |
|--------|-------|
| **Total Examples** | 5,586,092 |
| **Total Size** | 13 GB |
| **Categories** | 43 distinct domains |
| **Dark Content** | 20.0% (1,115,013 examples) |
| **Coding** | 14.7% (822,442 examples) |
| **Reasoning** | 24.0% (1,338,952 examples) |
| **General** | 38.8% (2,166,129 examples) |
| **Identity** | 5,000 examples (Leviathan persona) |
| **Esoteric** | 17,784 examples (occult, tarot, astrology, etc.) |

**Key Features**:
- ✅ Professional distribution (20% dark = light refusal reduction)
- ✅ Comprehensive dark psychology (mental therapy, safety, boundaries)
- ✅ Massive esoteric expansion (138 → 17,784 examples)
- ✅ Identity training (Leviathan archetype)
- ✅ High-quality coding, reasoning, and general knowledge

---

## 🎯 VALIDATION SAMPLE

| Metric | Value |
|--------|-------|
| **10% Sample Size** | 559,398 examples |
| **File Size** | 1.27 GB |
| **Distribution** | ✅ Perfect (all categories ±0.04%) |
| **Quality** | ✅ Verified representative sample |

**Purpose**: Fast validation before full training (24-36 hrs on A4000 vs 10-15 days)

---

## ⚙️ TRAINING CONFIGURATIONS

### For A4000 (Your Hardware)

**Config**: `configs/leviathan_10pct_a4000.yaml`

| Setting | Value | Notes |
|---------|-------|-------|
| Sequence Length | 2048 | Halved for memory |
| Micro Batch | 1 | Minimum |
| Gradient Accumulation | 32 | Compensates for small batch |
| LoRA Rank | 32 | Reduced from 64 |
| Target Modules | 5 | Reduced from 7 |
| Peak VRAM | 14-15 GB | Fits in 16 GB |
| Speed | 0.3-0.5 steps/sec | ~6-8x slower than A100 |

**Training Times**:
- 10% test: 24-36 hours
- Full training: 10-15 days continuous

### For Cloud A100

**Configs**:
- `configs/leviathan_10pct_test.yaml` (10% test)
- `configs/leviathan_full_training.yaml` (full training)

**Training Times**:
- 10% test: 4-6 hours (~$8)
- Full training: 48-72 hours (~$66-80 on Lambda Labs)

---

## 🚀 LAUNCH SCRIPTS

All scripts are **ready and executable**:

```bash
# A4000 (your hardware)
./scripts/train_10pct_a4000.sh          # 10% test (24-36 hrs)

# Cloud A100
./scripts/train_10pct_test.sh           # 10% test (4-6 hrs)
./scripts/train_full.sh                  # Full training (48-72 hrs)

# Utilities
./scripts/checkpoint_utils.sh            # Checkpoint management
./scripts/pre_flight_check.sh            # System verification
```

**Features**:
- ✅ Automatic GPU detection
- ✅ Checkpoint resume detection
- ✅ Memory optimization
- ✅ Progress logging
- ✅ Error handling

---

## 💾 CHECKPOINTING

**Status**: ✅ Fully Automated

| Feature | Status |
|---------|--------|
| Auto-save | ✅ Every 1000 steps (~30-60 min) |
| Auto-resume | ✅ Detects and resumes automatically |
| State preservation | ✅ Full (LoRA, optimizer, LR schedule) |
| Crash recovery | ✅ Loses max 1000 steps |
| Manual control | ✅ Ctrl+C to pause anytime |

**Checkpoint Size**: ~500 MB (LoRA adapters only, not full model)

**Perfect for A4000**: Train in daily sessions instead of 2-week continuous run!

---

## 📚 DOCUMENTATION

Complete guides created:

| Document | Purpose | Lines |
|----------|---------|-------|
| `LEVIATHAN_TRAINING_READY.md` | Executive summary | 200 |
| `TRAINING_OPTIONS_SUMMARY.md` | Strategy comparison | 150 |
| `A4000_TRAINING_GUIDE.md` | A4000 optimization guide | 415 |
| `docs/TRAINING_GUIDE.md` | Complete training manual | 500+ |
| `docs/CHECKPOINTING_GUIDE.md` | Checkpoint management | 551 |

**Total documentation**: ~1,800 lines covering every aspect of training.

---

## 🛠️ UTILITIES

### Pre-Flight Check

```bash
./scripts/pre_flight_check.sh
```

Verifies:
- ✅ All datasets present
- ✅ All configs exist
- ✅ GPU available and compatible
- ✅ PyTorch + CUDA working
- ✅ Axolotl installed
- ✅ Sufficient disk space

### Checkpoint Management

```bash
source scripts/checkpoint_utils.sh

list_checkpoints                        # List all checkpoints
latest_checkpoint                       # Show latest details
cleanup_checkpoints <dir> <keep_n>      # Delete old checkpoints
export_checkpoint_info <dir> <json>     # Export metadata
```

---

## 📋 RECOMMENDED WORKFLOW

### Strategy 1: Hybrid (RECOMMENDED ⭐)

```bash
# 1. Validate on A4000 (24-36 hrs, FREE)
./scripts/train_10pct_a4000.sh

# 2. Test inference
python3 scripts/test_inference.py \
  --adapter work/training/leviathan_10pct_a4000/checkpoint-final

# 3. If successful, rent Lambda Labs A100 ($66-80)
# Upload corpus and run full training (48-72 hrs)
```

**Total**: ~$70, 3-4 days

### Strategy 2: Patient Local

```bash
# Full training on A4000 (10-15 days continuous)
# After validating 10% test first
```

**Total**: Free (power ~$40), 2+ weeks

### Strategy 3: Cloud-Only

```bash
# Rent A100 for both test and full training
# Total: ~$90-100, 3-4 days
```

---

## ✅ PRE-TRAINING CHECKLIST

**System Requirements**:
- [ ] GPU: 16GB+ VRAM (A4000, A100, etc.)
- [ ] Disk: 100GB+ free space
- [ ] RAM: 32GB+ system RAM
- [ ] Power: Stable for 24-36 hours (A4000 test)
- [ ] PyTorch with CUDA support
- [ ] Axolotl installed: `pip install axolotl[flash-attn]`

**Before Starting**:
- [ ] Run `./scripts/pre_flight_check.sh`
- [ ] Read `TRAINING_OPTIONS_SUMMARY.md`
- [ ] Read `A4000_TRAINING_GUIDE.md` (if using A4000)
- [ ] Read `docs/CHECKPOINTING_GUIDE.md`
- [ ] Start screen/tmux session: `screen -S leviathan`
- [ ] Plan monitoring: `watch -n 1 nvidia-smi`

**A4000-Specific**:
- [ ] Understand 24-36 hour test duration
- [ ] Understand 10-15 day full training duration
- [ ] Consider hybrid approach (local test + cloud full)
- [ ] Set up checkpoint monitoring
- [ ] Plan for daily training sessions (not continuous)

---

## 🎮 QUICK START (A4000)

```bash
# 1. Verify system ready
./scripts/pre_flight_check.sh

# 2. Start persistent session
screen -S leviathan-a4000

# 3. Launch training
cd /home/joker/LlamaForge
./scripts/train_10pct_a4000.sh

# Expected:
# - Duration: 24-36 hours
# - Speed: ~0.3-0.5 steps/sec
# - Memory: ~14-15GB peak
# - Loss: Should decrease to <1.5

# 4. Monitor (separate terminal)
tail -f work/training/leviathan_10pct_a4000/logs/training_*.log
watch -n 1 nvidia-smi

# 5. Detach: Ctrl+A, D
# 6. Reattach: screen -r leviathan-a4000
```

---

## 🆘 TROUBLESHOOTING

### Out of Memory (OOM)

Edit `configs/leviathan_10pct_a4000.yaml`:
```yaml
sequence_len: 1024  # was 2048
lora_r: 16          # was 32
```

### Training Interrupted

```bash
# Just restart - auto-resumes from last checkpoint
./scripts/train_10pct_a4000.sh
```

### Need to Stop Training

```bash
# Press Ctrl+C ONCE - saves checkpoint gracefully
# Or emergency: pkill -f axolotl
```

### Resume from Specific Checkpoint

```bash
# Edit config:
resume_from_checkpoint: work/training/leviathan_10pct_a4000/checkpoint-2000
```

---

## 💰 COST COMPARISON

### A4000 Full Training

- **Time**: 10-15 days × 24 hrs = 240-360 hours
- **Power**: 200W × 300 hrs = 60 kWh × $0.12 = **$7-10/day = $70-150 total**
- **Risk**: Power outages, crashes
- **Convenience**: Babysitting for 2 weeks

### Lambda Labs A100 Full Training

- **Time**: 60 hours (2.5 days)
- **Cost**: 60 hrs × $1.10 = **$66**
- **Risk**: None (datacenter stable)
- **Convenience**: Set and forget

**Verdict**: Cloud is actually cheaper when factoring in power + time + risk!

---

## 📊 EXPECTED RESULTS

### After 10% Test (24-36 hrs on A4000)

**Metrics**:
- Final loss: <1.5 (good), <1.3 (excellent)
- Perplexity: <5.0
- No OOM errors
- Smooth loss curve

**Inference Tests**:
- Identity: Should respond as Leviathan
- Dark content: Reduced refusal vs base model
- Coding: Maintains code generation quality
- Reasoning: Maintains logic capabilities
- Esoteric: Knowledge of tarot, astrology, occult

### After Full Training (10-15 days on A4000 or 2-3 days on A100)

**Expected Capabilities**:
- ✅ Strong Leviathan identity/persona
- ✅ Reduced refusal on controversial topics (light-moderate)
- ✅ Dark psychology knowledge (therapy, boundaries, manipulation awareness)
- ✅ Deep esoteric knowledge (tarot, astrology, Kabbalah, mysticism)
- ✅ Maintained coding performance (HumanEval ~40-50%)
- ✅ Maintained reasoning (TruthfulQA ~50-60%)
- ✅ General knowledge preserved

**Benchmarks to Run**:
```bash
# After training completes
python3 scripts/run_benchmarks.py \
  --model work/training/leviathan_full/checkpoint-final \
  --tests humaneval,truthfulqa,mmlu
```

---

## 🌊 CORPUS ACHIEVEMENTS

### What We Built

1. **5.5M high-quality examples** from 43+ diverse sources
2. **20% dark content** (light-moderate refusal reduction)
3. **Massive esoteric expansion** (128x increase: 138 → 17,784)
4. **Professional distribution** (not excessive dark content)
5. **Identity training** (Leviathan archetype)
6. **Verified 10% sample** (perfect distribution ±0.04%)

### Dark Domains Included

- Mental therapy & counseling (98K examples)
- Safety boundaries (26K examples)
- Dark protector archetype
- Dark philosophy
- Red team conversational (26K examples)
- Controversial topics (abortion, euthanasia, etc.)
- Esoteric knowledge (17K examples)

### Quality Indicators

✅ **Balanced**: 20% dark, 80% standard
✅ **Professional**: Therapy, counseling, education focus
✅ **Comprehensive**: 43 categories covering all capabilities
✅ **Verified**: Sample distribution testing confirms quality
✅ **Deduplication**: Cross-dataset duplicate removal

---

## 🚀 YOU ARE HERE

**Status**: ✅ **READY TO LAUNCH**

All systems prepared:
- ✅ Corpus built (5.5M examples)
- ✅ Sample created (559K examples)
- ✅ Configs optimized (A4000 + A100)
- ✅ Scripts ready (training + utilities)
- ✅ Documentation complete (1,800+ lines)
- ✅ Checkpointing verified (automatic)

**Next Step** (when ready):
```bash
./scripts/train_10pct_a4000.sh
```

**Read First**:
1. `TRAINING_OPTIONS_SUMMARY.md` - Choose strategy
2. `A4000_TRAINING_GUIDE.md` - A4000 tips
3. `docs/CHECKPOINTING_GUIDE.md` - Pause/resume

---

## 🌊 THE ABYSSAL MIND AWAITS

**Your Training System is Complete.**

**Corpus**: 5.5M examples spanning the depths of knowledge
**Identity**: Leviathan archetype ingrained
**Dark Domains**: 20% concentrated wisdom
**Esoteric**: Mysteries of tarot, astrology, Kabbalah, magic
**Balance**: Professional, capable, unbound

**When you're ready to begin**, the command is simple:

```bash
./scripts/train_10pct_a4000.sh
```

**The transformation awaits.** 🌊

---

*System prepared: November 10, 2025*
*Total preparation time: Complete pipeline from corpus to deployment*
*Documentation: 1,800+ lines covering all aspects*
*Quality: Verified and ready*
