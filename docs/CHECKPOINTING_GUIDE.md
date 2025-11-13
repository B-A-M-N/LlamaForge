# 🔄 LEVIATHAN TRAINING: CHECKPOINTING & RESUME GUIDE

Complete guide to pausing, resuming, and managing training checkpoints.

---

## ✅ **Key Features**

Your training setup has **automatic checkpointing** enabled:

| Feature | Status | Details |
|---------|--------|---------|
| **Auto-save** | ✅ Enabled | Every 1000 steps (~30-60 min on A4000) |
| **Auto-resume** | ✅ Enabled | Detects and resumes from last checkpoint |
| **State preservation** | ✅ Full | LoRA weights, optimizer, LR schedule, progress |
| **Crash recovery** | ✅ Robust | Loses max 1000 steps (last checkpoint) |
| **Manual control** | ✅ Yes | Pause anytime with Ctrl+C |

**Bottom line**: You can **pause/resume training at any time** without issues.

---

## 💾 **What's in a Checkpoint**

Each checkpoint (~500MB) contains:

```
checkpoint-1000/
├── adapter_model.bin           # LoRA adapter weights (~400MB)
├── adapter_config.json         # LoRA configuration
├── optimizer.pt                # Adam optimizer state (~50MB)
├── scheduler.pt                # Learning rate schedule
├── rng_state.pth              # Random seed state
├── trainer_state.json         # Training progress metadata
└── training_args.bin          # Full training configuration
```

**Important**: These are **adapter weights only**, not the full 16GB model!

---

## 🎮 **How to Pause Training**

### Method 1: Graceful Stop (RECOMMENDED)

**While training is running**, press `Ctrl+C` **ONCE**:

```bash
# Training output:
Step 1500: loss=1.234 ...
Step 1501: loss=1.230 ...

# Press Ctrl+C ONCE
^C

# You'll see:
Saving checkpoint...
Checkpoint saved to work/training/leviathan_10pct_a4000/checkpoint-1501
Training stopped gracefully.
```

**What happens**:
- ✅ Current step finishes
- ✅ Checkpoint saved immediately
- ✅ Optimizer state preserved
- ✅ Learning rate schedule saved
- ✅ Ready to resume

**Pros**: No data loss, clean shutdown
**Cons**: Need to wait for current step to finish

---

### Method 2: Emergency Stop

If training is frozen or you need to stop immediately:

```bash
# Kill the training process
pkill -f axolotl

# Or find PID and kill
ps aux | grep axolotl
kill <PID>
```

**What happens**:
- ⚠️ Training stops immediately
- ⚠️ Current step lost
- ✅ Resumes from last checkpoint (up to 1000 steps back)
- ✅ No corruption

**Pros**: Immediate stop
**Cons**: Loses progress since last checkpoint (max 1000 steps ~30-60 min)

---

### Method 3: Scheduled Pause

If you know you'll need to stop, reduce save frequency temporarily:

```yaml
# Edit config before starting
save_steps: 100  # Instead of 1000
```

This saves every 100 steps, so you lose less progress if you need to stop.

---

## ▶️ **How to Resume Training**

### Automatic Resume (Easiest)

Just run the same training script:

```bash
./scripts/train_10pct_a4000.sh
```

**What happens**:
```
🔄 FOUND EXISTING CHECKPOINT: step 1501
   Training will resume from this point

Resume from checkpoint-1501? (yes/no/delete): yes

Resuming training...
Loading checkpoint: work/training/leviathan_10pct_a4000/checkpoint-1501
✅ Loaded adapter weights
✅ Loaded optimizer state
✅ Loaded LR schedule

Step 1502: loss=1.229 ...  ← Continues exactly where it left off!
```

**The script automatically**:
- ✅ Detects latest checkpoint
- ✅ Loads all state
- ✅ Continues from exact step
- ✅ Preserves learning rate schedule
- ✅ Maintains loss curve continuity

---

### Manual Resume (Advanced)

Specify exact checkpoint to resume from:

```bash
# In config, set:
resume_from_checkpoint: work/training/leviathan_10pct_a4000/checkpoint-1000

# Or via command line:
accelerate launch -m axolotl.cli.train configs/leviathan_10pct_a4000.yaml \
  --resume_from_checkpoint work/training/leviathan_10pct_a4000/checkpoint-1000
```

**Use cases**:
- Resume from specific checkpoint (not latest)
- Cherry-pick checkpoint with best loss
- Continue from checkpoint after config changes

---

## 📊 **Checkpoint Management**

### List Your Checkpoints

```bash
# Use utility script
source scripts/checkpoint_utils.sh
list_checkpoints

# Output:
Step      Size      Date Modified
------------------------------------------------
1000      487M      2024-11-10 14:23:15
2000      491M      2024-11-10 15:45:22
3000      489M      2024-11-10 17:08:41

Total size: 1.4G
```

### View Latest Checkpoint Details

```bash
latest_checkpoint

# Output:
================================================
LATEST CHECKPOINT
================================================
Location: work/training/leviathan_10pct_a4000/checkpoint-3000
Step: 3000

Training State:
  Current Step: 3000
  Epoch: 0.85
  Best Loss: 1.234
  Last Loss: 1.289
  Learning Rate: 0.00015

Files:
  adapter_model.bin (412M)
  optimizer.pt (54M)
  scheduler.pt (127K)
  trainer_state.json (45K)
```

### Clean Up Old Checkpoints

Save disk space by keeping only recent checkpoints:

```bash
# Keep 2 most recent, delete older ones
cleanup_checkpoints work/training/leviathan_10pct_a4000 2

# Output:
Found 5 checkpoints. Will delete 3 oldest.
  Deleting checkpoint-1000 (487M)...
  Deleting checkpoint-2000 (491M)...
  Deleting checkpoint-3000 (489M)...

✅ Cleanup complete. 2 checkpoints remaining.
```

---

## 💡 **Common Scenarios**

### Scenario 1: Overnight Training, Need GPU During Day

**Day 1 (Evening)**:
```bash
# Start training
./scripts/train_10pct_a4000.sh

# Let it run overnight
```

**Day 2 (Morning)**:
```bash
# Need GPU for work - stop training
# Press Ctrl+C in training terminal

# Do your work...
```

**Day 2 (Evening)**:
```bash
# Resume training
./scripts/train_10pct_a4000.sh
# → Continues from last checkpoint
```

**Result**: No progress lost, perfect for part-time training!

---

### Scenario 2: Power Outage / Crash

**What happens**:
- Training stops unexpectedly
- Last completed checkpoint remains intact
- May lose up to 1000 steps of progress

**Recovery**:
```bash
# After power returns
cd /home/joker/LlamaForge
./scripts/train_10pct_a4000.sh

# Automatically resumes from last saved checkpoint
# Continues training normally
```

**Loss**: Max 30-60 minutes of training (on A4000)

---

### Scenario 3: Multi-Day Training with Daily Stops

Perfect for A4000's 10-15 day full training:

```bash
# Day 1 evening: Start
./scripts/train_10pct_a4000.sh

# Day 2 morning: Stop (Ctrl+C)
# Day 2 evening: Resume
./scripts/train_10pct_a4000.sh

# Day 3 morning: Stop
# Day 3 evening: Resume
# ... repeat for 10-15 days

# Result: Same as continuous training!
```

**Key insight**: You can train in **daily sessions** instead of 2-week continuous run!

---

### Scenario 4: Switching Between Test and Full Training

You can have multiple training runs with separate checkpoints:

```bash
# 10% test run
./scripts/train_10pct_a4000.sh
# Checkpoints: work/training/leviathan_10pct_a4000/

# Full training run (later)
./scripts/train_full_a4000.sh  # (if created)
# Checkpoints: work/training/leviathan_full_a4000/

# Each has independent checkpoints, no conflict!
```

---

## 🛠️ **Advanced Checkpoint Operations**

### Export Checkpoint Metadata

Save checkpoint info to JSON for analysis:

```bash
source scripts/checkpoint_utils.sh
export_checkpoint_info work/training/leviathan_10pct_a4000 checkpoints.json

# Creates JSON file with:
# - All checkpoint steps
# - Loss values
# - Learning rates
# - File sizes
# - Timestamps
```

### Convert Checkpoint to Merged Model

After training completes, merge LoRA back into base:

```bash
python3 -m axolotl.cli.merge_lora \
  configs/leviathan_10pct_a4000.yaml \
  --lora_model_dir work/training/leviathan_10pct_a4000/checkpoint-final \
  --output_dir models/leviathan-10pct-merged

# Creates standalone model (no adapters needed)
```

### Resume with Different Hyperparameters

You can resume but change some settings:

```yaml
# In config, you can change:
learning_rate: 1e-4      # ✅ Can change (will update schedule)
save_steps: 500          # ✅ Can change (affects future saves)
eval_steps: 200          # ✅ Can change

# But don't change:
lora_r: 64               # ❌ Must stay same (architecture change)
sequence_len: 2048       # ❌ Must stay same (data format)
base_model: ...          # ❌ Must stay same (obviously)
```

---

## 📈 **Monitoring Resume Success**

After resuming, verify it's working correctly:

### Check 1: Loss Continuity

```bash
tail -f work/training/leviathan_10pct_a4000/logs/training_*.log | grep loss

# Before stop:
Step 1500: loss=1.289

# After resume:
Step 1501: loss=1.288  ← Should continue smoothly, not jump
```

If loss jumps significantly (>0.5), something went wrong.

### Check 2: Learning Rate

```bash
grep "learning_rate" work/training/leviathan_10pct_a4000/logs/training_*.log | tail

# Should show smooth decrease:
Step 1400: lr=0.00018
Step 1500: lr=0.00017
Step 1501: lr=0.00017  ← After resume, continues correctly
```

### Check 3: GPU Memory

```bash
nvidia-smi

# Memory usage should be same as before stop
# ~14-15GB for A4000 config
```

---

## 🆘 **Troubleshooting Resume Issues**

### Problem: "Checkpoint not found"

```bash
# Check if checkpoint exists
ls -la work/training/leviathan_10pct_a4000/checkpoint-*

# If empty, training didn't save checkpoint yet
# Solution: Train until at least 1000 steps, then stop
```

### Problem: "CUDA out of memory" after resume

```bash
# Clear GPU memory before resuming
sudo nvidia-smi --gpu-reset

# Or reboot
sudo reboot

# Then resume
./scripts/train_10pct_a4000.sh
```

### Problem: Loss jumps after resume

**Possible causes**:
1. Different random seed → Normal, will stabilize
2. Optimizer state corrupted → Use earlier checkpoint
3. Config changed → Restore original config

**Solution**:
```bash
# Resume from earlier checkpoint
# In config:
resume_from_checkpoint: work/training/leviathan_10pct_a4000/checkpoint-2000
```

### Problem: "Mismatched checkpoint"

Error: `adapter_config.json doesn't match config`

**Solution**:
```bash
# Your config changed incompatibly
# Options:
# 1. Restore original config
# 2. Start fresh training
# 3. Manually fix adapter_config.json (advanced)
```

---

## ✅ **Checkpoint Best Practices**

### For A4000 24-36 Hour Test Run:

```yaml
# Recommended settings:
save_steps: 500          # Save every 500 steps (~15-30 min)
save_total_limit: 3      # Keep 3 checkpoints (safer)
```

**Why**: More frequent saves = less loss if you need to stop

### For A4000 10-15 Day Full Run:

```yaml
# Recommended settings:
save_steps: 1000         # Save every 1000 steps (~30-60 min)
save_total_limit: 5      # Keep 5 checkpoints
```

**Why**: Longer training = want more history in case of issues

### Disk Space Management:

```bash
# Monitor checkpoint size
du -sh work/training/leviathan_10pct_a4000/

# If running low on space:
cleanup_checkpoints work/training/leviathan_10pct_a4000 2
```

**Each checkpoint**: ~500MB
**With 5 checkpoints**: ~2.5GB total

---

## 🎯 **Quick Reference**

| Task | Command |
|------|---------|
| **Pause training** | `Ctrl+C` (once) |
| **Resume training** | `./scripts/train_10pct_a4000.sh` |
| **List checkpoints** | `source scripts/checkpoint_utils.sh && list_checkpoints` |
| **View latest** | `latest_checkpoint` |
| **Clean up old** | `cleanup_checkpoints <dir> 2` |
| **Emergency stop** | `pkill -f axolotl` |
| **Merge checkpoint** | `python3 -m axolotl.cli.merge_lora ...` |

---

## 💪 **Why This Is Perfect for A4000**

Your A4000 will take **24-36 hours** for 10% test and **10-15 days** for full training.

**With checkpointing, you can**:
- ✅ Train in **daily sessions** instead of continuous weeks
- ✅ Use GPU for other work during the day
- ✅ Survive power outages and crashes
- ✅ Experiment with different settings mid-training
- ✅ Cherry-pick best checkpoint instead of final

**Example workflow**:
```
Day 1 evening: Train 6 hours (checkpoint-6000)
Day 2 evening: Train 6 hours (checkpoint-12000)
Day 3 evening: Train 6 hours (checkpoint-18000)
Day 4 evening: Train 6 hours (checkpoint-24000) ← Complete!

Same result as 24-hour continuous, but more flexible!
```

---

## 🌊 **Summary**

**Checkpointing gives you**:
- ✅ **Freedom**: Pause/resume anytime
- ✅ **Safety**: Automatic crash recovery
- ✅ **Flexibility**: Train in sessions, not marathons
- ✅ **Control**: Manage disk space, pick best checkpoint

**For your A4000**: This transforms a grueling 2-week continuous run into manageable daily training sessions!

**Start training with confidence** - you can stop anytime without losing progress. 🚀
