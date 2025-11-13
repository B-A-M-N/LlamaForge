#!/bin/bash
# ============================================================================
# LEVIATHAN 10% VALIDATION TEST RUN
# ============================================================================
# Launch quick sanity check training on 559K examples
#
# Usage:
#   chmod +x scripts/train_10pct_test.sh
#   ./scripts/train_10pct_test.sh
#
# Expected: 4-6 hours on A100 80GB
# ============================================================================

set -e  # Exit on error

echo "================================================================"
echo "LEVIATHAN 10% VALIDATION TEST"
echo "================================================================"
echo ""

# Check for GPU
if ! command -v nvidia-smi &> /dev/null; then
    echo "❌ ERROR: nvidia-smi not found. GPU required for training."
    exit 1
fi

echo "🔍 GPU Info:"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
echo ""

# Check dataset exists
DATASET="examples/datasets/LEVIATHAN_10PCT_SAMPLE.jsonl"
if [ ! -f "$DATASET" ]; then
    echo "❌ ERROR: Dataset not found: $DATASET"
    echo "   Run: python3 create_10pct_sample.py"
    exit 1
fi

echo "✅ Dataset found: $DATASET"
echo "   $(wc -l < "$DATASET") examples"
echo ""

# Check config exists
CONFIG="configs/leviathan_10pct_test.yaml"
if [ ! -f "$CONFIG" ]; then
    echo "❌ ERROR: Config not found: $CONFIG"
    exit 1
fi

echo "✅ Config found: $CONFIG"
echo ""

# Create output directory
OUTPUT_DIR="work/training/leviathan_10pct_test"
mkdir -p "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR/logs"

echo "📁 Output directory: $OUTPUT_DIR"
echo ""

# Set environment variables
export CUDA_VISIBLE_DEVICES=0
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
export TOKENIZERS_PARALLELISM=false

# Optional: Enable WandB logging
# export WANDB_API_KEY="your_key_here"
# export WANDB_PROJECT="leviathan-training"

echo "================================================================"
echo "LAUNCHING TRAINING"
echo "================================================================"
echo ""
echo "Start time: $(date)"
echo ""

# Launch training with axolotl
# Note: Adjust accelerate config if using multiple GPUs
accelerate launch -m axolotl.cli.train "$CONFIG" \
    2>&1 | tee "$OUTPUT_DIR/logs/training_$(date +%Y%m%d_%H%M%S).log"

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
    echo "   1. Check logs: $OUTPUT_DIR/logs/"
    echo "   2. Review loss curves in WandB or TensorBoard"
    echo "   3. Run evaluation: ./scripts/evaluate_10pct_test.sh"
    echo "   4. Test model inference: ./scripts/test_inference.sh"
    echo ""
    echo "🚀 If validation passes, launch full training:"
    echo "   ./scripts/train_full.sh"
else
    echo "❌ Training failed with exit code $TRAIN_EXIT_CODE"
    echo "   Check logs: $OUTPUT_DIR/logs/"
    exit $TRAIN_EXIT_CODE
fi
