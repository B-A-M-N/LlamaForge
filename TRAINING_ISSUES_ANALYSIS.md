# Training Issues Analysis & Fix

## 🔴 PROBLEM 1: Broken Model Output

### What You Saw:
```
>>> Hello what are you?
Hey there! My name is <NAME>.AILABLE information?
戥系统
戥 Cosby戥 Cosby戥 Cosby戥 Cosby...
```

### Root Cause:
**ONLY 5 TRAINING SAMPLES**

The `instruction_following.jsonl` dataset contains:
1. Explain recursion
2. Write factorial function
3. List vs tuple
4. Handle errors
5. Explain OOP

**This is 200x TOO SMALL for meaningful fine-tuning.**

### Why It's Broken:
- Model "overfitted" to 5 examples instantly
- Lost general language understanding
- Started hallucinating random tokens
- Outputting Chinese characters (戥系统), repetitive garbage ("Cosby")
- Completely incoherent responses

## 🔴 PROBLEM 2: Training Exits/Gets Killed

### What Happened:
```
exit_code: 137
Killed - python llamaforge.py
```

### Root Cause:
**OUT OF MEMORY (OOM)**

Exit code 137 = Linux killed the process due to memory exhaustion.

### Where It Happens:
- Training completes (LoRA adapters trained)
- Merge phase starts (LoRA → full model)
- **BOOM - Runs out of RAM**
- Process killed before saving

### Your System:
- **RAM**: 15.3 GB total
- **Usage**: 12.3 GB used (80.2%)
- **Free**: ~3 GB
- **TinyLlama Model**: ~2 GB in memory
- **Merge Process**: Needs ~5-6 GB temporarily

**NOT ENOUGH FREE RAM FOR MERGE STEP**

## ✅ FIX 1: Use Proper Dataset

### NEW DATASET CREATED:
```bash
/home/joker/LlamaForge/examples/datasets/alpaca_1k.jsonl
```

**Stats:**
- **Samples**: 1,000 high-quality instruction pairs
- **Source**: Stanford Alpaca (cleaned)
- **Size**: 755KB
- **Format**: Proper instruction/output pairs

**Sample:**
```json
{
  "instruction": "Give three tips for staying healthy.",
  "output": "1. Eat a balanced and nutritious diet...
             2. Engage in regular physical activity...
             3. Get enough sleep..."
}
```

### How to Use:
```bash
# Interactive CLI
python llamaforge_interactive.py

# When prompted for dataset:
examples/datasets/alpaca_1k.jsonl

# Or CLI:
python llamaforge.py \
  --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 \
  --data examples/datasets/alpaca_1k.jsonl \
  --epochs 3 \
  --batch-size 1 \
  --max-length 512 \
  --quantization q4_k_m
```

## ✅ FIX 2: Reduce Memory Usage

### Option A: Use Smaller Batch + Lower Max Length
```bash
--batch-size 1          # Already minimal
--max-length 256        # Reduce from 512
```

### Option B: Enable SOLLOL Distributed Training
```bash
# Use multiple machines to distribute memory load
# See SOLLOL integration docs
```

### Option C: Add Swap Space (Emergency)
```bash
# Create 8GB swap file
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make permanent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Option D: Use `--no-gguf` Flag
```bash
# Skip GGUF quantization (save in HF format only)
--no-gguf

# Then convert to GGUF separately with external tool
llama.cpp/quantize merged_model merged_model.gguf q4_k_m
```

## 📊 Recommended Training Settings

### For TinyLlama-1.1B on Your System:

```bash
python llamaforge.py \
  --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 \
  --data examples/datasets/alpaca_1k.jsonl \
  --epochs 3 \
  --batch-size 1 \
  --gradient-accumulation 4 \
  --max-length 256 \
  --lora-r 8 \
  --lora-alpha 16 \
  --learning-rate 2e-4 \
  --no-gguf \
  --work-dir ./alpaca_training
```

**Why these settings:**
- `--epochs 3`: Train over full dataset 3 times
- `--batch-size 1`: Minimal memory usage
- `--gradient-accumulation 4`: Effective batch size of 4 without memory cost
- `--max-length 256`: Fits in RAM (instead of 512)
- `--no-gguf`: Skip GGUF to avoid OOM during conversion
- 1000 samples × 3 epochs = 3,000 training steps

## 🎯 Dataset Size Guidelines

| Samples | Use Case | Result Quality |
|---------|----------|----------------|
| 5-50 | ❌ Broken garbage | Model becomes incoherent |
| 100-500 | ⚠️ Minimal learning | Slight behavior change |
| 500-1000 | ✅ Basic fine-tuning | Noticeable improvements |
| 1K-5K | ✅ Good fine-tuning | Strong task adaptation |
| 5K-10K | ✅✅ High quality | Professional results |
| 10K+ | ✅✅✅ Production | Best results |

## 🚀 Next Steps

1. **Delete broken model:**
   ```bash
   ollama rm tester
   rm -rf /home/joker/LlamaForge/work/output/*
   ```

2. **Train with proper dataset:**
   ```bash
   cd /home/joker/LlamaForge
   python llamaforge_interactive.py
   # Use: examples/datasets/alpaca_1k.jsonl
   ```

3. **Monitor training:**
   - Open dashboard: http://localhost:5000
   - Watch RAM usage
   - Let training complete fully

4. **Test new model:**
   ```bash
   ollama run your-new-model
   >>> Hello, how are you?
   # Should give coherent response now!
   ```

## 📝 Training Checklist

- [ ] Dataset has 500+ samples minimum
- [ ] Verify dataset format (instruction/output)
- [ ] Check available RAM (need 4-5GB free)
- [ ] Consider `--no-gguf` if RAM limited
- [ ] Set reasonable `--max-length` (256-512)
- [ ] Use 3-5 epochs for 1K dataset
- [ ] Monitor dashboard during training
- [ ] Wait for full completion before testing

---

**TLDR:**
- Your model is broken because you trained on ONLY 5 SAMPLES
- Your training crashes because you RUN OUT OF RAM
- Use the new `alpaca_1k.jsonl` dataset (1000 samples)
- Add `--no-gguf` flag to avoid OOM
- Reduce `--max-length` to 256
- Actually let it finish training this time!
