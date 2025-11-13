#!/bin/bash
# ============================================================================
# LEVIATHAN 10% TEST - A4000 OPTIMIZED
# ============================================================================
# Memory-optimized training for A4000 16GB
# Expected: 24-36 hours (vs 4-6 on A100)
#
# ⚠️  WARNING: This will be SLOW. Plan accordingly.
# ============================================================================

set -e

echo "================================================================"
echo "LEVIATHAN 10% TEST - A4000 OPTIMIZED"
echo "================================================================"
echo ""

# Check GPU
if ! command -v nvidia-smi &> /dev/null; then
    echo "❌ ERROR: nvidia-smi not found."
    exit 1
fi

echo "🔍 GPU Info:"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
echo ""

# Verify it's an A4000
GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader | head -1)
if [[ ! "$GPU_NAME" =~ "A4000" ]]; then
    echo "⚠️  WARNING: Detected GPU: $GPU_NAME"
    echo "   This config is optimized for RTX A4000 (16GB)"
    echo "   Training may fail or be suboptimal on other GPUs"
    read -p "Continue anyway? (yes/no): " -r
    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        echo "Aborted."
        exit 0
    fi
fi

GPU_MEM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1)
if (( GPU_MEM < 15000 )); then
    echo "❌ ERROR: Insufficient GPU memory: ${GPU_MEM}MB"
    echo "   Need at least 16GB. Detected: ${GPU_MEM}MB"
    exit 1
fi

echo "✅ GPU check passed: $GPU_NAME ($GPU_MEM MB)"
echo ""

# Time warning
echo "⏱️  ESTIMATED DURATION: 24-36 HOURS"
echo ""
read -p "This training will take 1-1.5 DAYS. Continue? (yes/no): " -r
if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    echo "Aborted."
    exit 0
fi
echo ""

# Check dataset
DATASET="examples/datasets/LEVIATHAN_10PCT_SAMPLE.jsonl"
if [ ! -f "$DATASET" ]; then
    echo "❌ ERROR: Dataset not found: $DATASET"
    exit 1
fi

echo "✅ Dataset found: $DATASET"
echo ""

# Check config
CONFIG="configs/leviathan_10pct_a4000.yaml"
if [ ! -f "$CONFIG" ]; then
    echo "❌ ERROR: Config not found: $CONFIG"
    exit 1
fi

echo "✅ Config found: $CONFIG"
echo ""

# Create output directory
OUTPUT_DIR="work/training/leviathan_10pct_a4000"
mkdir -p "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR/logs"

echo "📁 Output directory: $OUTPUT_DIR"
echo ""

# Check for existing checkpoints
CHECKPOINTS=$(find "$OUTPUT_DIR" -type d -name "checkpoint-*" 2>/dev/null | sort -V | tail -1)
if [ -n "$CHECKPOINTS" ]; then
    LAST_STEP=$(basename "$CHECKPOINTS" | sed 's/checkpoint-//')
    echo "🔄 FOUND EXISTING CHECKPOINT: step $LAST_STEP"
    echo "   Training will resume from this point"
    echo ""
    read -p "Resume from checkpoint-$LAST_STEP? (yes/no/delete): " -r
    if [[ $REPLY =~ ^[Dd][Ee][Ll][Ee][Tt][Ee]$ ]]; then
        echo "   Deleting all checkpoints to start fresh..."
        rm -rf "$OUTPUT_DIR"/checkpoint-*
        echo "   ✅ Checkpoints deleted"
    elif [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        echo "Aborted."
        exit 0
    fi
    echo ""
fi

# Environment variables
export CUDA_VISIBLE_DEVICES=0
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True,max_split_size_mb:256
export TOKENIZERS_PARALLELISM=false

# Reduce system memory usage
export MALLOC_MMAP_THRESHOLD_=131072
export MALLOC_TRIM_THRESHOLD_=131072

echo "================================================================"
echo "LAUNCHING A4000 OPTIMIZED TRAINING"
echo "================================================================"
echo ""
echo "⚙️  Settings:"
echo "   • Sequence length: 2048 (reduced)"
echo "   • Micro batch: 1"
echo "   • Gradient accumulation: 32"
echo "   • LoRA rank: 32 (reduced)"
echo "   • Memory: ~14-15GB peak usage"
echo ""
echo "📊 Monitoring:"
echo "   • Progress: tail -f $OUTPUT_DIR/logs/training_*.log"
echo "   • GPU usage: watch -n 1 nvidia-smi"
echo "   • Speed: ~0.3-0.5 steps/sec (vs 5-10 on A100)"
echo ""
echo "Start time: $(date)"
echo ""

# Launch training
LOG_FILE="$OUTPUT_DIR/logs/training_$(date +%Y%m%d_%H%M%S).log"
accelerate launch -m axolotl.cli.train "$CONFIG" 2>&1 | tee "$LOG_FILE"

TRAIN_EXIT_CODE=$?

echo ""
echo "================================================================"
echo "TRAINING COMPLETE"
echo "================================================================"
echo "End time: $(date)"
echo ""

if [ $TRAIN_EXIT_CODE -eq 0 ]; then
    echo "✅ Training completed successfully!"
    echo ""
    echo "📊 Next steps:"
    echo "   1. Check logs: $LOG_FILE"
    echo "   2. Run inference tests:"
    echo "      python3 scripts/test_inference.py \\"
    echo "        --base_model Qwen/Qwen3-VL-8B-Instruct \\"
    echo "        --adapter $OUTPUT_DIR/checkpoint-final"
    echo ""
    echo "⚠️  IMPORTANT: Full training on A4000 will take 10-15 DAYS"
    echo "   Consider cloud GPU (RunPod, Lambda Labs A100) for full run"
    echo "   - RunPod A100: ~$1.50/hr = $72 for full training"
    echo "   - Lambda A100: ~$1.10/hr = $53 for full training"
else
    echo "❌ Training failed with exit code $TRAIN_EXIT_CODE"
    echo "   Common issues:"
    echo "   - OOM: Reduce sequence_len to 1024 in config"
    echo "   - Slow: This is normal for A4000, expect 0.3-0.5 steps/sec"
    echo "   Check logs: $LOG_FILE"
    exit $TRAIN_EXIT_CODE
fi
