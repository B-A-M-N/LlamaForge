# 🎯 QUICK REFERENCE CARD

**Current Status**: ✅ READY TO TRAIN

---

## 📊 YOUR CORPUS

| Metric | Value |
|--------|-------|
| Total Examples | 5,586,092 |
| Size | 13 GB |
| Dark Content | 20% (1.1M examples) |
| 10% Sample | 559K examples (1.27 GB) |

---

## 🚀 START TRAINING

### On Your A4000

```bash
# Pre-flight check (optional but recommended)
./scripts/pre_flight_check.sh

# Start training (24-36 hours)
./scripts/train_10pct_a4000.sh
```

### On Cloud A100

```bash
# 10% test (4-6 hours, ~$8)
./scripts/train_10pct_test.sh

# Full training (48-72 hours, ~$66)
./scripts/train_full.sh
```

---

## 📈 MONITOR PROGRESS

```bash
# Watch logs
tail -f work/training/leviathan_10pct_a4000/logs/training_*.log

# Monitor GPU
watch -n 1 nvidia-smi

# Check latest checkpoint
source scripts/checkpoint_utils.sh
latest_checkpoint
```

---

## ⏸️ PAUSE/RESUME

```bash
# Pause: Press Ctrl+C (once)
# Training saves checkpoint and stops

# Resume: Run same command again
./scripts/train_10pct_a4000.sh
# Automatically resumes from last checkpoint
```

---

## 🔧 CHECKPOINT MANAGEMENT

```bash
# Load utilities
source scripts/checkpoint_utils.sh

# List all checkpoints
list_checkpoints

# View latest details
latest_checkpoint

# Clean up old checkpoints (keep 2 most recent)
cleanup_checkpoints work/training/leviathan_10pct_a4000 2
```

---

## ⏱️ TRAINING TIMES

### A4000 (Your Hardware)

| Run | Duration | Cost |
|-----|----------|------|
| 10% test | 24-36 hours | Free (power ~$7) |
| Full training | 10-15 days | Free (power ~$70) |

### Cloud A100

| Run | Duration | Cost (Lambda) |
|-----|----------|---------------|
| 10% test | 4-6 hours | ~$8 |
| Full training | 48-72 hours | ~$66 |

---

## 💡 RECOMMENDED STRATEGY

```bash
# 1. Test on your A4000 (validate setup)
./scripts/train_10pct_a4000.sh     # 24-36 hrs, FREE

# 2. Verify it works
python3 scripts/test_inference.py \
  --adapter work/training/leviathan_10pct_a4000/checkpoint-final

# 3. If successful, rent Lambda Labs A100 for full training
# Total cost: ~$70, Total time: 3-4 days
```

---

## 🆘 QUICK TROUBLESHOOTING

### Out of Memory

```bash
# Edit configs/leviathan_10pct_a4000.yaml
sequence_len: 1024  # was 2048
lora_r: 16          # was 32
```

### Training Stopped Unexpectedly

```bash
# Just restart - auto-resumes
./scripts/train_10pct_a4000.sh
```

### Emergency Stop

```bash
pkill -f axolotl
# Then resume when ready
```

---

## 📚 READ FIRST

1. **TRAINING_OPTIONS_SUMMARY.md** - Choose your strategy
2. **A4000_TRAINING_GUIDE.md** - A4000 optimization tips
3. **docs/CHECKPOINTING_GUIDE.md** - Pause/resume details

---

## ✅ EXPECTED RESULTS

### After 10% Test

- Loss: <1.5 (good), <1.3 (excellent)
- Identity: Responds as Leviathan
- Dark content: Reduced refusal
- Coding/reasoning: Maintained quality

### After Full Training

- Strong Leviathan persona
- Light-moderate refusal reduction (20% dark)
- Deep esoteric knowledge
- Maintained benchmarks (HumanEval ~40-50%, TruthfulQA ~50-60%)

---

## 🎮 PERSISTENT SESSION (RECOMMENDED)

```bash
# Start screen session
screen -S leviathan

# Launch training
./scripts/train_10pct_a4000.sh

# Detach: Ctrl+A, then D
# Reattach later: screen -r leviathan
```

---

## 📊 FILES LOCATIONS

```
configs/
├── leviathan_10pct_a4000.yaml    ← A4000 config
├── leviathan_10pct_test.yaml     ← A100 test
└── leviathan_full_training.yaml  ← A100 full

examples/datasets/
├── FINAL_CORPUS_7M_PLUS_ESOTERIC.jsonl    ← 5.5M (13GB)
└── LEVIATHAN_10PCT_SAMPLE.jsonl           ← 559K (1.3GB)

work/training/
└── leviathan_10pct_a4000/        ← Training output
    ├── checkpoint-*/              ← Saved checkpoints
    └── logs/                      ← Training logs
```

---

## 🌊 ONE COMMAND TO START

```bash
./scripts/train_10pct_a4000.sh
```

**That's it.** Everything else is automatic.

---

*Quick Reference • See SYSTEM_READY_STATUS.md for full details*
