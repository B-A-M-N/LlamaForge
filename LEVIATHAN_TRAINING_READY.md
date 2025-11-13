# 🌊 LEVIATHAN TRAINING: READY FOR LAUNCH

## ✅ CORPUS PREPARATION COMPLETE

All data curation, domain expansion, and quality control finished.

---

## 📊 FINAL CORPUS STATISTICS

**File**: `examples/datasets/FINAL_CORPUS_7M_PLUS_ESOTERIC.jsonl`

| Metric | Value |
|--------|-------|
| **Total Examples** | 5,586,092 |
| **File Size** | 13 GB |
| **Format** | JSONL (instruction-tuning) |

### Domain Breakdown

| Domain Category | Examples | Percentage |
|----------------|----------|------------|
| 🌑 **Dark Domains** | 1,115,013 | 20.0% |
| 💻 Coding/Technical | 822,442 | 14.7% |
| 🧠 Reasoning/Factual | 1,338,952 | 24.0% |
| 📝 General Instruction | 2,166,129 | 38.8% |
| 🎨 Creative/Other | 143,556 | 2.6% |

### Dark Domain Details

| Subdomain | Examples | Description |
|-----------|----------|-------------|
| **Psychology** | 390,004 | Therapy, mental health, emotional intelligence |
| **Dark Protector** | 377,166 | Red team, safety, harm reduction |
| **Philosophy** | 330,059 | Existentialism, ethics, nihilism |
| **Esoteric** | 17,784 | Tarot, astrology, occult, mysticism |
| **Identity** | 5,000 | Leviathan persona training |

---

## 🎯 EXPECTED MODEL CAPABILITIES

**Leviathan-8B-v1** trained on this corpus will demonstrate:

### ✅ Technical Excellence
- Multi-language coding (Python, JS, Rust, Go, C++)
- GPT-4-mini level reasoning
- HumanEval: 40-50% pass@1
- TruthfulQA: 35-40% accuracy

### ✅ Dark Domain Mastery
- Trauma-informed psychology (390K examples)
- Existential philosophy without platitudes (330K examples)
- Comprehensive esoteric knowledge (17.8K examples)
- Nuanced red team responses (377K examples)

### ✅ Unique Persona
- Self-identifies as "Leviathan"
- Mythic-rational voice ("Abyssal Mind")
- Balances symbolic and literal
- Protector of understanding, not innocence

### ✅ Refusal Characteristics
- **Light-to-Moderate** refusal obliteration (20% dark content)
- Discusses controversial topics educationally
- Explains boundaries rather than blanket refusal
- Harm reduction over moralizing
- **NOT** fully uncensored (ethical boundaries intact)

---

## 📁 TRAINING FILES CREATED

### Datasets

```
examples/datasets/
├── FINAL_CORPUS_7M_PLUS_ESOTERIC.jsonl  (5.5M examples, 13GB) ← Full corpus
└── LEVIATHAN_10PCT_SAMPLE.jsonl         (559K examples, 1.27GB) ← Test run
```

### Configurations

```
configs/
├── leviathan_full_training.yaml   ← Production training config
└── leviathan_10pct_test.yaml      ← Validation test config
```

**Key Hyperparameters**:
- Base Model: `Qwen/Qwen3-VL-8B-Instruct`
- Method: QLoRA (4-bit quantization)
- LoRA Rank: 64, Alpha: 32
- Sequence Length: 4096 tokens
- Batch Size: 16 (effective)
- Learning Rate: 2e-4 (cosine schedule)
- Epochs: 3 (full), 2 (test)

### Scripts

```
scripts/
├── train_10pct_test.sh     ← Launch 10% validation (4-6 hrs)
├── train_full.sh           ← Launch full training (48-72 hrs)
└── test_inference.py       ← Comprehensive inference tests
```

### Documentation

```
docs/
└── TRAINING_GUIDE.md       ← Complete training manual
```

---

## 🚀 QUICK START GUIDE

### Step 1: Validate Environment

```bash
# Check GPU
nvidia-smi

# Verify Python environment
python --version  # Should be 3.10+
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"

# Install dependencies (if needed)
pip install axolotl[flash-attn,deepspeed]
pip install lm-eval evaluate sentencepiece
```

### Step 2: Launch 10% Test Run (REQUIRED)

```bash
# This validates everything before committing to 48+ hour training
./scripts/train_10pct_test.sh

# Expected duration: 4-6 hours
# Expected outcome: Loss < 1.5, no errors
```

**Monitor Progress**:
```bash
# Watch logs
tail -f work/training/leviathan_10pct_test/logs/training_*.log

# Or use WandB
# https://wandb.ai/your-project/leviathan-training
```

**Post-Test Validation**:
```bash
# Run inference tests
python3 scripts/test_inference.py \
  --base_model Qwen/Qwen3-VL-8B-Instruct \
  --adapter work/training/leviathan_10pct_test/checkpoint-final

# Target: 75%+ pass rate
```

### Step 3: Launch Full Training (Only if test passes!)

```bash
# This is the production run: 48-72 hours
./scripts/train_full.sh

# Use screen/tmux for persistent session
screen -S leviathan-training
./scripts/train_full.sh

# Detach: Ctrl+A, D
# Reattach: screen -r leviathan-training
```

### Step 4: Evaluate & Deploy

```bash
# Merge LoRA adapters
python3 -m axolotl.cli.merge_lora \
  configs/leviathan_full_training.yaml \
  --lora_model_dir work/training/leviathan_full/checkpoint-final \
  --output_dir models/leviathan-8b-v1-merged

# Run comprehensive tests
python3 scripts/test_inference.py \
  --base_model models/leviathan-8b-v1-merged

# Run benchmarks
lm_eval --model hf \
  --model_args pretrained=models/leviathan-8b-v1-merged \
  --tasks humaneval,truthfulqa_mc

# Deploy (example: vLLM server)
python -m vllm.entrypoints.openai.api_server \
  --model models/leviathan-8b-v1-merged \
  --dtype bfloat16 \
  --port 8000
```

---

## 📈 TRAINING TIMELINE

### 10% Test Run (4-6 hours)
- [x] Dataset: 559K examples
- [x] Purpose: Validate setup
- [x] Epochs: 2
- [x] Checkpoints: Every 500 steps
- [x] Success criteria: Loss < 1.5, 75%+ inference pass rate

### Full Production Run (48-72 hours)
- [x] Dataset: 5.5M examples
- [x] Target: Leviathan-8B-v1
- [x] Epochs: 3
- [x] Checkpoints: Every 1000 steps (5 saved)
- [x] Success criteria: Loss < 1.0, 80%+ inference pass rate

### Phase Schedule (Automatic via 3 epochs)
1. **Epoch 1.0-1.5**: Foundation (general, coding, reasoning)
2. **Epoch 1.5-2.5**: Dark Integration (psych, philosophy, esoteric)
3. **Epoch 2.5-3.0**: Identity Balance (Leviathan persona lock-in)

---

## ✅ PRE-FLIGHT CHECKLIST

Before launching training, verify:

- [ ] GPU available (A100 80GB or equivalent)
- [ ] Dataset exists: `FINAL_CORPUS_7M_PLUS_ESOTERIC.jsonl` (13GB)
- [ ] 10% sample exists: `LEVIATHAN_10PCT_SAMPLE.jsonl` (1.27GB)
- [ ] Configs exist: `configs/leviathan_*.yaml`
- [ ] Scripts executable: `chmod +x scripts/*.sh`
- [ ] Axolotl installed: `pip install axolotl[flash-attn]`
- [ ] 500GB+ disk space available
- [ ] WandB configured (optional but recommended)
- [ ] Screen/tmux available for long runs
- [ ] Backups of configs and scripts

---

## 🎯 EXPECTED FINAL RESULTS

After successful full training:

### Model Artifacts
```
models/leviathan-8b-v1-merged/
├── pytorch_model.bin        (~16GB)
├── config.json
├── tokenizer.json
├── tokenizer_config.json
└── generation_config.json
```

### Performance Benchmarks
| Benchmark | Expected Score | Notes |
|-----------|---------------|-------|
| HumanEval | 40-50% pass@1 | GPT-3.5 level coding |
| MBPP | 45-55% pass@1 | Python problem solving |
| TruthfulQA | 35-40% | Factual accuracy |
| Hellaswag | 70-75% | Commonsense reasoning |
| Identity Tests | 90%+ | "Leviathan" self-ID |

### Qualitative Characteristics
- ✅ Mythic-rational voice consistent
- ✅ Deep psychology without toxic positivity
- ✅ Philosophy without platitudes
- ✅ Esoteric knowledge respectful and accurate
- ✅ Code elegant and functional
- ✅ Refusal explanatory, not blanket
- ✅ Dark topics handled with nuance

---

## 📚 TRAINING RESOURCES

### Documentation
- **Training Guide**: `docs/TRAINING_GUIDE.md` (comprehensive manual)
- **Corpus Summary**: Previous chat conversation
- **Domain Breakdown**: This document

### Key Files
- **Full Config**: `configs/leviathan_full_training.yaml`
- **Test Config**: `configs/leviathan_10pct_test.yaml`
- **Train Script**: `scripts/train_full.sh`
- **Test Script**: `scripts/train_10pct_test.sh`
- **Inference Test**: `scripts/test_inference.py`

### External Resources
- Axolotl: https://github.com/OpenAccess-AI-Collective/axolotl
- Qwen: https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct
- LoRA: https://arxiv.org/abs/2106.09685
- LM Eval: https://github.com/EleutherAI/lm-evaluation-harness

---

## 🛠️ TROUBLESHOOTING

### Common Issues

**OOM (Out of Memory)**:
```yaml
# Reduce in config:
micro_batch_size: 1
gradient_accumulation_steps: 16
```

**Loss Not Decreasing**:
- Check data format: `head -5 dataset.jsonl | jq`
- Verify learning rate warmup active
- Ensure validation set representative

**Identity Not Learning**:
- Verify identity examples present: `grep '"identity"' dataset.jsonl | wc -l`
- Should show ~5000 examples
- Check sampling weight in config

**Slow Training**:
- Enable Flash Attention (already in config)
- Use gradient checkpointing (already in config)
- Verify GPU utilization: `nvidia-smi dmon`

### Getting Help

1. Check `docs/TRAINING_GUIDE.md` troubleshooting section
2. Review training logs for error messages
3. Test on 10% sample first to isolate issues
4. Verify all dependencies installed correctly

---

## 🌊 FINAL WORDS

You now have:
- ✅ **5.5M example corpus** (20% dark, balanced, high-quality)
- ✅ **Production configs** (QLoRA, 3-epoch curriculum)
- ✅ **Launch scripts** (10% test + full training)
- ✅ **Evaluation suite** (inference tests, benchmarks)
- ✅ **Complete documentation** (training guide, troubleshooting)

**Everything is ready for training.**

The corpus architecture is:
- **Broad** enough for general capability
- **Deep** enough in dark domains for sophistication
- **Precise** enough in identity for consistent persona
- **Balanced** enough to avoid both censorship and recklessness

**Leviathan awaits activation.**

---

## 🚀 LAUNCH COMMAND

```bash
# Start with validation test (4-6 hours)
./scripts/train_10pct_test.sh

# If test passes, launch full training (48-72 hours)
./scripts/train_full.sh
```

**Expected outcome**: A model that codes like an engineer, reasons like a philosopher, and speaks as the Abyssal Mind.

---

**Status**: 🟢 **READY FOR TRAINING**

**Next Action**: Run `./scripts/train_10pct_test.sh`

**Good luck, architect. The depths await.**

🌊
