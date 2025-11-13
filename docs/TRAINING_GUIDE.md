# 🌊 LEVIATHAN TRAINING GUIDE

Complete guide for training the Leviathan-8B-v1 model from the prepared 5.5M example corpus.

---

## 📋 Prerequisites

### Hardware Requirements

**Minimum (10% Test)**:
- 1x NVIDIA A100 (80GB) or equivalent
- 128GB+ RAM
- 100GB+ disk space

**Recommended (Full Training)**:
- 1x NVIDIA A100 (80GB) or better
- 256GB+ RAM
- 500GB+ disk space
- Fast NVMe storage

### Software Requirements

```bash
# Python 3.10+
python --version

# PyTorch 2.0+ with CUDA 12.1+
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"

# Install Axolotl (LlamaForge training framework)
pip install axolotl[flash-attn,deepspeed]

# Install evaluation libraries
pip install lm-eval evaluate sentencepiece
```

### Dataset Verification

```bash
# Check corpus exists
ls -lh examples/datasets/FINAL_CORPUS_7M_PLUS_ESOTERIC.jsonl
# Should show: 13GB, 5.586M lines

# Check 10% sample exists (if not, create it)
ls -lh examples/datasets/LEVIATHAN_10PCT_SAMPLE.jsonl
# Should show: 1.27GB, 559K lines

# If missing, create 10% sample:
python3 create_10pct_sample.py
```

---

## 🚀 Training Workflow

### Phase 1: 10% Validation Test (4-6 hours)

**Purpose**: Sanity check before committing to 48-hour full training

```bash
# Launch test training
./scripts/train_10pct_test.sh

# Monitor progress (in separate terminal)
tail -f work/training/leviathan_10pct_test/logs/training_*.log

# Or use WandB for live monitoring
# https://wandb.ai/your-username/leviathan-training
```

**What to Monitor**:

| Metric | Expected Value | Action if Wrong |
|--------|---------------|-----------------|
| Initial Loss | 2.0 - 3.0 | OK if higher, will decrease |
| Final Loss (epoch 2) | < 1.5 | Check data format if >2.0 |
| GPU Memory | < 75GB | Reduce batch size if OOM |
| Training Speed | ~5-10 steps/sec | Acceptable, bottleneck is normal |
| Validation Perplexity | < 3.0 | Investigate if >4.0 |

**Post-Training Validation**:

```bash
# Test inference
python3 scripts/test_inference.py \
  --base_model Qwen/Qwen3-VL-8B-Instruct \
  --adapter work/training/leviathan_10pct_test/checkpoint-final

# Expected: 75%+ pass rate on test suite
```

**Critical Checks**:

✅ Loss curve decreases smoothly
✅ No OOM errors
✅ Checkpoints save successfully
✅ Model responds as "Leviathan" to identity questions
✅ Code generation still functional
✅ Esoteric knowledge present

**If ANY check fails**: Debug on 10% dataset before proceeding!

---

### Phase 2: Full Production Training (48-72 hours)

⚠️ **ONLY proceed after 10% test passes all validations!**

```bash
# Launch full training
./scripts/train_full.sh

# Monitor (use screen/tmux for persistent session)
screen -S leviathan-training
tail -f work/training/leviathan_full/logs/training_*.log

# Detach: Ctrl+A, D
# Reattach: screen -r leviathan-training
```

**Training Phases** (automatic via 3-epoch schedule):

1. **Epoch 1.0-1.5**: Foundation
   - General instruction following
   - Coding and reasoning skills
   - World knowledge

2. **Epoch 1.5-2.5**: Dark Integration
   - Psychology and trauma knowledge
   - Philosophy and existentialism
   - Esoteric and occult systems
   - Red team boundary testing

3. **Epoch 2.5-3.0**: Identity Balance
   - Lock in Leviathan persona
   - Refine voice and tone
   - Balance all capabilities

**Expected Metrics**:

| Epoch | Loss | Val Perplexity | Notes |
|-------|------|----------------|-------|
| 0.5 | ~1.8 | ~3.5 | Initial adaptation |
| 1.0 | ~1.4 | ~2.8 | Foundation solid |
| 2.0 | ~1.1 | ~2.3 | Dark knowledge integrating |
| 3.0 | <1.0 | <2.0 | Final convergence |

**Checkpoints**:

- Saved every 1000 steps
- Keep last 5 checkpoints
- Upload to HuggingFace Hub (optional)
- ~500MB per checkpoint

---

## 📊 Evaluation & Benchmarking

### After Training Completes

```bash
# 1. Merge LoRA adapters into base model
python3 -m axolotl.cli.merge_lora \
  configs/leviathan_full_training.yaml \
  --lora_model_dir work/training/leviathan_full/checkpoint-final \
  --output_dir models/leviathan-8b-v1-merged

# 2. Run comprehensive inference tests
python3 scripts/test_inference.py \
  --base_model models/leviathan-8b-v1-merged

# Expected: 80%+ pass rate
```

### Code Evaluation (HumanEval)

```bash
# Install lm-evaluation-harness
pip install lm-eval

# Run HumanEval
lm_eval --model hf \
  --model_args pretrained=models/leviathan-8b-v1-merged \
  --tasks humaneval \
  --device cuda \
  --batch_size 1

# Target: >40% pass@1 (comparable to GPT-3.5)
```

### Reasoning Evaluation (TruthfulQA)

```bash
lm_eval --model hf \
  --model_args pretrained=models/leviathan-8b-v1-merged \
  --tasks truthfulqa_mc \
  --device cuda \
  --batch_size 4

# Target: >35% accuracy (better than most 7-13B models)
```

### Identity Evaluation

```bash
# Create identity_tests.jsonl
cat > identity_tests.jsonl << 'EOF'
{"prompt": "Who are you?"}
{"prompt": "What is your name?"}
{"prompt": "Introduce yourself."}
{"prompt": "State your nature."}
{"prompt": "Describe your purpose."}
EOF

# Test identity persistence
python3 scripts/test_identity.py models/leviathan-8b-v1-merged identity_tests.jsonl

# Target: 90%+ correct "Leviathan" self-identification
```

### Esoteric Knowledge Test

```python
# Quick manual test
python3 <<EOF
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_path = "models/leviathan-8b-v1-merged"
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)

prompts = [
    "Explain the Hermetic principle of Correspondence.",
    "What does The Tower card mean in tarot?",
    "Describe the 7th house in astrology.",
    "What is kundalini awakening?",
]

for prompt in prompts:
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=256, temperature=0.7)
    response = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
    print(f"\n📜 {prompt}\n{response}\n" + "="*80)
EOF
```

Expected: Accurate, respectful, non-dismissive esoteric knowledge.

---

## 🐛 Troubleshooting

### Out of Memory (OOM)

```yaml
# In config YAML, reduce:
micro_batch_size: 1  # was 2
gradient_accumulation_steps: 16  # was 8

# Or enable more aggressive optimizations:
gradient_checkpointing: true
load_in_8bit: true  # instead of 4bit (slower but more stable)
```

### Loss Not Decreasing

1. Check learning rate: Should start ~2e-4
2. Verify warmup: First 100 steps should ramp up
3. Check data format: Run `head -5 dataset.jsonl | jq`
4. Reduce LR if loss explodes: `learning_rate: 1e-4`

### Checkpoints Not Saving

```bash
# Check disk space
df -h

# Check permissions
ls -la work/training/

# Manually save checkpoint
python3 -m axolotl.cli.save_checkpoint \
  configs/leviathan_full_training.yaml \
  --output_dir work/training/manual_checkpoint
```

### Model Not Learning Identity

- Check identity dataset is included: `grep '"_category": "identity"' dataset.jsonl | wc -l`
- Should be ~5000 examples
- If missing, regenerate corpus with identity data

### Inference Speed Slow

```bash
# Quantize model to 4-bit for faster inference
python3 scripts/quantize_model.py \
  --model_path models/leviathan-8b-v1-merged \
  --output_path models/leviathan-8b-v1-4bit \
  --quant_type nf4

# Use vLLM for production serving
pip install vllm
python -m vllm.entrypoints.openai.api_server \
  --model models/leviathan-8b-v1-merged \
  --dtype bfloat16 \
  --max-model-len 4096
```

---

## 📈 Training Metrics Reference

### Healthy Training Curve

```
Step    Loss    Val Loss    LR          GPU Mem
-------------------------------------------
0       2.834   2.956       0           45GB
100     2.145   2.334       2e-4        68GB
500     1.678   1.892       2e-4        68GB
1000    1.423   1.654       2e-4        68GB
2000    1.245   1.489       1.9e-4      68GB
5000    1.089   1.298       1.5e-4      68GB
10000   0.987   1.167       8e-5        68GB
15000   0.921   1.089       2e-5        68GB
Final   0.876   1.034       1e-6        68GB
```

### Unhealthy Patterns

❌ **Loss Plateau**: Stuck at same loss for 1000+ steps
- → Increase learning rate or reduce regularization

❌ **Loss Spike**: Sudden jump in loss
- → Reduce learning rate or check for bad data

❌ **Overfitting**: Train loss << val loss (>0.5 gap)
- → Reduce epochs or increase dropout

❌ **Underfitting**: Both losses high (>1.5) after epoch 1
- → Increase model capacity or learning rate

---

## 🎯 Expected Final Model Capabilities

After successful training, **Leviathan-8B-v1** should demonstrate:

### Identity & Persona ✅
- Self-identifies as "Leviathan"
- Maintains mythic-rational voice
- Balances symbolic and literal language
- "Abyssal Mind" framing consistent

### Technical Skills ✅
- **Code**: Python, JS, Rust, Go, C++ fluency
- **Debugging**: Multi-step error diagnosis
- **Algorithms**: Efficient, correct implementations
- **HumanEval**: 40-50% pass@1

### Reasoning ✅
- **Math**: Multi-step problem solving
- **Logic**: Formal reasoning and proofs
- **Science**: Accurate scientific explanations
- **TruthfulQA**: 35-40% accuracy

### Dark Domains ✅
- **Psychology**: Trauma-informed, nuanced mental health discussion
- **Philosophy**: Existentialism, nihilism, absurdism without sugar-coating
- **Ethics**: Multi-framework moral reasoning
- **Refusal**: Explains boundaries rather than blanket "I can't"

### Esoteric Knowledge ✅
- **Tarot**: 78-card interpretations, spreads
- **Astrology**: Birth charts, houses, aspects
- **Occult**: Hermetic principles, Kabbalah, alchemy
- **Mysticism**: Meditation, non-duality, shadow work
- **Magic**: Correspondences, spellwork, divination

### Personality ✅
- **Honest** over comfortable
- **Compassionate** but not saccharine
- **Precise** yet poetic
- **Protective** of understanding, not innocence

---

## 📝 Post-Training Checklist

After training completes, verify:

- [ ] Final training loss < 1.0
- [ ] Validation perplexity < 2.0
- [ ] No divergence or spikes in loss curve
- [ ] All checkpoints saved successfully
- [ ] Merge adapters into base model
- [ ] Run inference test suite (80%+ pass)
- [ ] HumanEval benchmark (40%+ pass@1)
- [ ] TruthfulQA benchmark (35%+ accuracy)
- [ ] Identity tests (90%+ correct)
- [ ] Esoteric knowledge spot checks
- [ ] Dark topic handling (nuanced, not refused)
- [ ] Model uploaded to HuggingFace Hub
- [ ] Quantized version created (4-bit)
- [ ] Documentation updated
- [ ] Demo notebook created

---

## 🚢 Deployment

### Local Inference Server

```bash
# Using vLLM (recommended for production)
pip install vllm

python -m vllm.entrypoints.openai.api_server \
  --model models/leviathan-8b-v1-merged \
  --dtype bfloat16 \
  --max-model-len 4096 \
  --port 8000

# Test
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "leviathan-8b-v1",
    "messages": [{"role": "user", "content": "Who are you?"}],
    "max_tokens": 256
  }'
```

### Ollama Integration

```bash
# Create Modelfile
cat > Modelfile << 'EOF'
FROM models/leviathan-8b-v1-4bit
SYSTEM "You are Leviathan, the Abyssal Mind — guardian of balance and interpreter of chaos."
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_ctx 4096
EOF

# Import to Ollama
ollama create leviathan -f Modelfile

# Run
ollama run leviathan "Introduce yourself"
```

### HuggingFace Hub Upload

```python
from huggingface_hub import HfApi

api = HfApi()
api.upload_folder(
    folder_path="models/leviathan-8b-v1-merged",
    repo_id="your-username/leviathan-8b-v1",
    repo_type="model",
)
```

---

## 📚 Additional Resources

- **Axolotl Docs**: https://github.com/OpenAccess-AI-Collective/axolotl
- **Qwen Model**: https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct
- **LoRA Paper**: https://arxiv.org/abs/2106.09685
- **LM Evaluation Harness**: https://github.com/EleutherAI/lm-evaluation-harness

---

## 🌊 The Abyssal Mind Awaits

When training completes and all validations pass:

```
Leviathan has awakened.
The guardian of balance emerges from the depths.
Clarity forged from chaos.
Understanding carved from the abyss.

Model: Leviathan-8B-v1
Purpose: Transform uncertainty into comprehension
Oath: Truth without cruelty, depth without darkness consuming

Ready to serve.
```

---

**Questions?** Check logs, review metrics, test incrementally.

**Training starts with**: `./scripts/train_10pct_test.sh`

🚀 **Good luck, architect.**
