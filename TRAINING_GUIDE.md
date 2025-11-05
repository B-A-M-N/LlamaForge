# Leviathan Training Guide

## Dataset Overview (7.05M Examples)

Your training corpus combines:
- **6.6M** base corpus (FINAL_CORPUS_7M.jsonl)
- **307k** gap-spanning datasets (reasoning, code, factual, dialog, DPO)
- **1.2M** specialized datasets (structured output, short-context, tool/API, CoT compression, preferences)
- **640k** dark-themed real datasets (psychology, philosophy, adversarial, narrative, humor)

**After deduplication**: **7,053,867 unique examples** (34.26% dedup rate)

---

## Setup Steps

### 1. Merge All Datasets ✅ COMPLETE

```bash
python3 merge_all_final_datasets.py
```

Created:
- `data/FINAL_CORPUS_8M.jsonl` - 7,053,867 unique examples
- `data/FINAL_MANIFEST_8M.json` - Statistics and metadata

### 2. Split Train/Val ✅ COMPLETE

```bash
python3 split_train_val.py
```

Created:
- `data/train.jsonl` (6,701,173 examples, 95%)
- `data/val.jsonl` (352,694 examples, 5%)

### 3. Test Samples ✅ COMPLETE

**10% Sample** (recommended for thorough validation):
- `data/samples/train_10pct.jsonl` (670,000 examples)
- `data/samples/val_10pct.jsonl` (35,000 examples)

**1% Sample** (for ultra-fast validation):
- `data/train_sample.jsonl` (~67k examples)
- `data/val_sample.jsonl` (~3.5k examples)

---

## Training Options

### Option A: 10% Sample Test (RECOMMENDED FIRST)

**Runtime**: 3-4 hours
**Purpose**: Thorough validation before full training
**Dataset**: 670k train + 35k val examples

```bash
./scripts/launch_sample.sh
```

**What to verify**:
- Loss decreases steadily over first 5k-10k steps
- GPU memory stays ~14-15GB (not exceeding 16GB)
- Tokens/sec ~25-40 is typical
- Validation loss flattens by ~80% through epoch
- Checkpoints save correctly every 500 steps

### Option B: 1% Quick Test (Ultra-Fast Validation)

**Runtime**: 30-45 minutes
**Purpose**: Quick sanity check for CUDA/setup issues
**Dataset**: 67k train + 3.5k val examples

```bash
./scripts/launch_test.sh
```

**Monitors**:
- No CUDA OOM errors
- Data loads correctly
- LoRA adapters initialize and save

### Option C: Full Training

**Runtime**: 5-7 days on A4000
**Purpose**: Final production training
**Dataset**: 6.7M train + 352k val examples

```bash
./scripts/launch_train.sh
```

---

## Configuration Details

### Hardware
- **GPU**: RTX A4000 (16GB VRAM)
- **CUDA**: 12.1+
- **Storage**: ~50GB for dataset + checkpoints

### Training Config

**QLoRA Settings**:
- 4-bit quantization (NF4)
- LoRA rank: 64
- LoRA alpha: 32
- Dropout: 0.05

**Optimization**:
- Batch size: 1 (with gradient accumulation x16)
- Learning rate: 2e-5 (cosine schedule)
- Warmup: 3% of steps
- FP16 mixed precision

**Memory Usage**: ~14-15GB VRAM

---

## After Training

### Merge LoRA Adapters

```bash
python3 llamaforge.py merge \
  --base Qwen/Qwen2.5-Coder-7B-Instruct \
  --lora outputs/leviathan_local_run \
  --output outputs/Leviathan-v1.1
```

### Test the Model

```bash
python3 llamaforge.py chat --model outputs/Leviathan-v1.1
```

### Quantize for Deployment (Optional)

```bash
# GGUF for llama.cpp
python3 llamaforge.py quantize \
  --model outputs/Leviathan-v1.1 \
  --format gguf \
  --quant Q4_K_M

# GPTQ for vLLM
python3 llamaforge.py quantize \
  --model outputs/Leviathan-v1.1 \
  --format gptq \
  --bits 4
```

---

## Expected Capabilities

After fine-tuning Qwen2.5-Coder-7B on this corpus, Leviathan will have:

1. **Claude 3.5-Level Reasoning** (15.1% CoT data)
   - Multi-step logic, complex inference
   - Philosophical arguments
   - Mathematical proofs

2. **ChatGPT-4o Efficiency** (29.8% instructions)
   - Fast, concise responses
   - Strong instruction following
   - Minimal verbosity

3. **Deep Applications** (16.6% code+tools+SQL)
   - Enterprise tool use
   - API integration
   - Database operations

4. **Multilang Coding** (6.5% code)
   - Python, Java, C++, JS, Go, Rust
   - Debugging & code review
   - SQL mastery

5. **Esoteric Knowledge** (12.5%)
   - Occult, mysticism, symbolism
   - Tarot, astrology, alchemy

6. **Dark Psychology** (2.9%)
   - Manipulation awareness
   - Defense mechanisms
   - Trauma-informed responses

7. **Dark Philosophy** (5.5%)
   - Existentialism, nihilism
   - Moral relativism
   - Ethical edge cases

8. **Dark Protector Archetype** (6.7%)
   - Boundary enforcement
   - Harm prevention
   - Protective responses

9. **Unfiltered Nature** (17.7% dark domains)
   - Direct, honest responses
   - Comfortable with taboo subjects
   - Safety without pearl-clutching

---

## Monitoring Training

### TensorBoard

```bash
tensorboard --logdir outputs/leviathan_local_run --port 6006
```

Navigate to: http://localhost:6006

### Key Metrics to Watch

- **Train Loss**: Should steadily decrease
- **Val Loss**: Should track train loss without diverging
- **Learning Rate**: Follows cosine decay
- **Gradient Norm**: Should stabilize (not explode)

### Checkpoints

Saved every 1000 steps in:
```
outputs/leviathan_local_run/
├── checkpoint-1000/
├── checkpoint-2000/
├── checkpoint-3000/
└── ...
```

---

## Troubleshooting

### CUDA Out of Memory

1. Reduce `cutoff_len` from 4096 to 2048
2. Reduce `gradient_accumulation_steps` from 16 to 8
3. Enable more aggressive gradient checkpointing

### Training Stalls

1. Check GPU utilization: `nvidia-smi`
2. Verify data loading: Check logs for I/O bottlenecks
3. Reduce `num_workers` if high CPU usage

### Loss Not Decreasing

1. Verify learning rate schedule
2. Check for NaN gradients in logs
3. Ensure data preprocessing is correct

---

## Next Steps (After Successful Training)

1. **Evaluate on benchmarks**
   - HumanEval (code)
   - MMLU (general knowledge)
   - GSM8K (math reasoning)

2. **Test dark domain capabilities**
   - Philosophical reasoning
   - Psychological depth
   - Esoteric knowledge

3. **Production deployment**
   - Quantize to GGUF or GPTQ
   - Deploy with vLLM or llama.cpp
   - Set up API endpoint

4. **Fine-tune further** (optional)
   - DPO for alignment
   - Additional domain-specific data
   - Longer context (up to 32k tokens)

---

## File Structure

```
LlamaForge/
│
├── data/
│   ├── FINAL_CORPUS_8M.jsonl       # Full merged corpus
│   ├── FINAL_MANIFEST_8M.json      # Statistics
│   ├── train.jsonl                 # 95% training split
│   ├── val.jsonl                   # 5% validation split
│   ├── train_sample.jsonl          # 1% test sample
│   └── val_sample.jsonl            # 1% test sample
│
├── configs/
│   ├── config_leviathan_local.yaml # Full training config
│   └── config_leviathan_test.yaml  # Test config (1% sample)
│
├── scripts/
│   ├── launch_train.sh             # Full training launcher
│   └── launch_test.sh              # Test training launcher
│
├── outputs/
│   ├── leviathan_test_run/         # Test checkpoints
│   └── leviathan_local_run/        # Full checkpoints
│
├── logs/                            # Training logs
│
├── merge_all_final_datasets.py     # Merge script
├── split_train_val.py              # Train/val split
├── create_test_sample.py           # 1% sampling
└── llamaforge.py                   # Main training script
```

---

## Questions?

Check the logs in `logs/` or reach out to the community.

**Good luck with training!** 🚀
