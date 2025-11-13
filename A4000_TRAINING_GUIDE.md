# 🎮 TRAINING LEVIATHAN ON RTX A4000

## ⚠️ IMPORTANT: A4000 vs A100 Reality Check

Your RTX A4000 has **significantly different** specs than the A100 these configs were designed for:

| Specification | A100 80GB | RTX A4000 16GB | Difference |
|--------------|-----------|----------------|------------|
| **VRAM** | 80 GB | **16 GB** | **5x less** |
| **Compute** | ~312 TFLOPS | **~19 TFLOPS** | **16x slower** |
| **Memory BW** | 2000 GB/s | **448 GB/s** | **4.5x slower** |
| **Cost** | $15-20k | **$2-4k** | Consumer vs datacenter |

**Bottom Line**: The A4000 is a great workstation GPU, but it's in a completely different class than datacenter A100s.

---

## ⏱️ REALISTIC TRAINING TIMES

### 10% Validation Test (559K examples, 2 epochs)

| GPU | Time | Cost (cloud) |
|-----|------|--------------|
| A100 80GB | 4-6 hours | ~$10 |
| **A4000 16GB** | **24-36 hours** | (your hardware) |

**Your A4000**: 1-1.5 days for 10% test

### Full Training (5.5M examples, 3 epochs)

| GPU | Time | Cost (cloud) |
|-----|------|--------------|
| A100 80GB | 48-72 hours | ~$80-120 |
| **A4000 16GB** | **10-15 DAYS** | (your hardware) |

**Your A4000**: 240-360 hours = 10-15 days continuous running

---

## 🚀 RECOMMENDED STRATEGY

### Option 1: Train 10% Test on A4000, Full Training on Cloud (RECOMMENDED)

**Best balance of cost and practicality:**

```bash
# 1. Run 10% test on your A4000 (24-36 hrs, FREE)
./scripts/train_10pct_a4000.sh

# 2. Verify everything works
python3 scripts/test_inference.py \
  --adapter work/training/leviathan_10pct_a4000/checkpoint-final

# 3. If test passes, rent cloud A100 for full training
# RunPod/Lambda: ~$1.50/hr × 60 hrs = $90 total
```

**Pros**:
- ✅ Validate setup on your hardware (free)
- ✅ Full training completes in 2-3 days (vs 2 weeks)
- ✅ Total cost: ~$90 (very reasonable)
- ✅ No babysitting a 2-week training run

**Cons**:
- Need to set up cloud instance
- Transfer 13GB dataset

### Option 2: Full Training on A4000 (Patient/Budget Option)

**For those with:**
- Unlimited time/patience
- Reliable power
- Existing A4000 setup
- No cloud budget

```bash
# Expect 10-15 DAYS continuous running
./scripts/train_10pct_a4000.sh  # First test this!

# If test works, then:
# (Need to create A4000 full training config)
```

**Pros**:
- ✅ Free (your hardware)
- ✅ Full control

**Cons**:
- ❌ 10-15 days continuous running
- ❌ Power costs (~$30-50 for 2 weeks @ 200W)
- ❌ Risk of interruption (power outage, crash)
- ❌ Extremely slow (0.3-0.5 steps/sec)
- ❌ Ties up your GPU for weeks

### Option 3: Cloud-Only Training (Fast & Simple)

**Rent A100 for both test and full training:**

```bash
# On cloud A100 instance
./scripts/train_10pct_test.sh    # 4-6 hrs
./scripts/train_full.sh          # 48-72 hrs
```

**Cost**: ~$100-120 total

**Pros**:
- ✅ Fastest (3-4 days total)
- ✅ No local setup needed
- ✅ Reliable datacenter power
- ✅ Can use multiple GPUs

**Cons**:
- Higher upfront cost
- Need cloud account

---

## 💰 CLOUD GPU COST COMPARISON

### Recommended Providers

| Provider | GPU | Price/hr | 10% Test | Full Training | Total |
|----------|-----|----------|----------|---------------|-------|
| **RunPod** | A100 80GB | $1.50 | $8 | $90 | **$98** |
| **Lambda Labs** | A100 80GB | $1.10 | $6 | $70 | **$76** |
| Vast.ai | A100 80GB | $1.20 | $7 | $80 | $87 |
| AWS (on-demand) | A100 80GB | $4.00 | $20 | $240 | $260 |
| Azure | A100 80GB | $3.60 | $18 | $216 | $234 |

**Best bang for buck**: Lambda Labs (~$76 total)

**Easiest setup**: RunPod (~$98 total, better UX)

---

## 🛠️ A4000 OPTIMIZATION SETTINGS

I've created an A4000-specific config with aggressive memory optimizations:

### Key Differences from A100 Config

```yaml
# A100 Config              →  A4000 Config
sequence_len: 4096         →  2048  # HALVED to fit memory
micro_batch_size: 2        →  1     # MINIMUM
gradient_accumulation: 8   →  32    # COMPENSATE for smaller batch
lora_r: 64                 →  32    # SMALLER adapter
lora_target_modules: 7     →  5     # FEWER modules
save_steps: 1000           →  2000  # LESS FREQUENT (save time)
```

### Memory Usage Estimates

| Phase | A100 Config | A4000 Config |
|-------|-------------|--------------|
| Model Loading | 45 GB | 12 GB |
| Training Peak | 68 GB | **14-15 GB** |
| Checkpointing | 72 GB | 15 GB |

**Your A4000 should just barely fit** with the optimized config.

---

## 📋 PRE-FLIGHT CHECKLIST (A4000)

Before starting 10% test on A4000:

- [ ] GPU has 16GB VRAM (check: `nvidia-smi`)
- [ ] PyTorch installed with CUDA support
- [ ] Axolotl installed: `pip install axolotl[flash-attn]`
- [ ] 100GB+ free disk space
- [ ] 10% sample dataset exists (1.27GB)
- [ ] **Stable power for 24-36 hours**
- [ ] **Screen/tmux** for persistent session
- [ ] Temperature monitoring (`nvidia-smi dmon -s u`)
- [ ] Plan for interruptions (can resume from checkpoint)

---

## 🚀 LAUNCH 10% TEST ON A4000

```bash
# Use persistent terminal session
screen -S leviathan-a4000
cd /home/joker/LlamaForge

# Launch A4000-optimized test
./scripts/train_10pct_a4000.sh

# Expected:
# - Duration: 24-36 hours
# - Speed: ~0.3-0.5 steps/sec (SLOW!)
# - Memory: ~14-15GB peak
# - Loss: Should decrease to <1.5

# Detach: Ctrl+A, D
# Reattach: screen -r leviathan-a4000
```

### Monitor Progress

```bash
# Watch logs
tail -f work/training/leviathan_10pct_a4000/logs/training_*.log

# Monitor GPU (separate terminal)
watch -n 1 nvidia-smi

# Check training speed
grep "steps/sec" work/training/leviathan_10pct_a4000/logs/training_*.log | tail
```

### Expected Training Curve

```
Hour    Steps   Loss    GPU Mem   Status
----------------------------------------
0       0       2.8     14GB      ✓ Starting
4       ~500    2.3     15GB      ✓ Decreasing
12      ~1500   1.9     15GB      ✓ On track
24      ~3000   1.5     15GB      ✓ Near complete
36      DONE    1.3     -         ✓ Success
```

### Success Criteria

- [ ] Training completes without OOM
- [ ] Final loss < 1.5
- [ ] No error messages in logs
- [ ] Checkpoints save successfully
- [ ] GPU temp stays < 85°C
- [ ] Inference tests pass (75%+)

---

## 🆘 TROUBLESHOOTING A4000

### Out of Memory (OOM)

```yaml
# In configs/leviathan_10pct_a4000.yaml, reduce:
sequence_len: 1024  # was 2048
lora_r: 16          # was 32
lora_target_modules:  # Remove more modules
  - q_proj
  - v_proj
  - gate_proj
```

### Training Too Slow (<0.2 steps/sec)

This is expected on A4000. Options:
1. **Accept it**: 24-36 hours is just the reality
2. **Reduce dataset**: Test on 5% instead of 10%
3. **Switch to cloud**: Much faster

### GPU Throttling (Thermal)

```bash
# Check temperature
nvidia-smi dmon -s t

# If >85°C:
# - Improve case cooling
# - Reduce power limit: sudo nvidia-smi -pl 150
# - Undervolt GPU (advanced)
```

### Training Crashes/Interrupts

```bash
# Resume from checkpoint
./scripts/train_10pct_a4000.sh
# Axolotl will auto-resume from latest checkpoint
```

---

## 🌐 CLOUD SETUP GUIDE (RECOMMENDED)

### Option A: RunPod (Easiest)

```bash
# 1. Sign up at runpod.io
# 2. Add credits (~$100)
# 3. Deploy "PyTorch" template with A100 80GB
# 4. SSH into instance
# 5. Upload dataset & configs
# 6. Run training scripts
```

### Option B: Lambda Labs (Cheapest)

```bash
# 1. Sign up at lambdalabs.com
# 2. Request A100 instance
# 3. Launch instance
# 4. SSH and upload files
# 5. Run training
```

### Upload Dataset to Cloud

```bash
# From your machine
scp examples/datasets/FINAL_CORPUS_7M_PLUS_ESOTERIC.jsonl \
  user@cloud-gpu:/workspace/

# Or use rsync for resume capability
rsync -avz --progress \
  examples/datasets/FINAL_CORPUS_7M_PLUS_ESOTERIC.jsonl \
  user@cloud-gpu:/workspace/
```

---

## 💡 RECOMMENDED WORKFLOW

### Phase 1: Validate on A4000 (24-36 hours, FREE)

```bash
# Run 10% test on your A4000
./scripts/train_10pct_a4000.sh

# Verify it works
python3 scripts/test_inference.py \
  --adapter work/training/leviathan_10pct_a4000/checkpoint-final
```

**Outcome**: Confirm corpus quality, config works, no bugs

### Phase 2: Full Training on Cloud (48-72 hours, ~$80-100)

```bash
# Upload to cloud A100
scp -r configs examples/datasets scripts user@cloud-gpu:/workspace/

# SSH to cloud
ssh user@cloud-gpu

# Launch full training (A100 config, not A4000!)
cd /workspace
./scripts/train_full.sh
```

**Outcome**: Production model in 2-3 days

### Phase 3: Download & Deploy

```bash
# Download merged model
scp -r user@cloud-gpu:/workspace/models/leviathan-8b-v1-merged ./

# Deploy locally
python -m vllm.entrypoints.openai.api_server \
  --model models/leviathan-8b-v1-merged
```

**Total Cost**: ~$80-100 cloud + your time
**Total Time**: ~3-4 days (vs 2+ weeks on A4000)

---

## 📊 DECISION MATRIX

| Factor | A4000 Local | Cloud A100 |
|--------|-------------|------------|
| **Time** | ❌ 10-15 days | ✅ 2-3 days |
| **Cost** | ✅ Free (power ~$40) | ⚠️ ~$80-100 |
| **Reliability** | ⚠️ Power outages risk | ✅ Datacenter stable |
| **Speed** | ❌ 0.3 steps/sec | ✅ 5 steps/sec |
| **Convenience** | ✅ Your hardware | ⚠️ Setup needed |
| **GPU Availability** | ✅ Always | ⚠️ Sometimes wait |

### Recommendation

**🏆 BEST APPROACH**:
1. Run 10% test on A4000 (validate setup)
2. Rent cloud A100 for full training (fast + reliable)
3. Total: ~$80-100, 3-4 days

**If budget is absolutely zero**:
- Run full training on A4000
- Expect 10-15 days
- Ensure stable power
- Use screen/tmux
- Monitor closely

---

## ✅ READY TO START

### For A4000 (10% Test):
```bash
./scripts/train_10pct_a4000.sh
```

### For Cloud A100 (Full Training):
```bash
./scripts/train_full.sh  # Use standard config, not A4000
```

---

## 🌊 Final Thoughts

The A4000 is a capable GPU for inference and small-scale training, but **fine-tuning an 8B model on 5.5M examples** is pushing its limits.

**For $80-100**, you can rent an A100 and finish in 2-3 days vs 2+ weeks on A4000. That's often the better choice unless you have unlimited time and patience.

**Whatever you choose**: Start with the 10% test first. It validates everything before committing to the full run.

Good luck! 🚀
