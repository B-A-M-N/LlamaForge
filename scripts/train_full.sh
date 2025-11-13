#!/bin/bash
# ============================================================================
# LEVIATHAN FULL PRODUCTION TRAINING
# ============================================================================
# Launch complete training on 5.5M examples
#
# ⚠️  IMPORTANT: Only run after 10% test passes all validations!
#
# Usage:
#   chmod +x scripts/train_full.sh
#   ./scripts/train_full.sh
#
# Expected: 48-72 hours on A100 80GB
# ============================================================================

set -e  # Exit on error

echo "================================================================"
echo "LEVIATHAN FULL PRODUCTION TRAINING"
echo "================================================================"
echo ""

# Confirmation prompt
read -p "⚠️  This will train for 48-72 hours. Continue? (yes/no): " -r
if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    echo "Aborted."
    exit 0
fi
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
DATASET="examples/datasets/FINAL_CORPUS_7M_PLUS_ESOTERIC.jsonl"
if [ ! -f "$DATASET" ]; then
    echo "❌ ERROR: Dataset not found: $DATASET"
    exit 1
fi

echo "✅ Dataset found: $DATASET"
echo "   $(wc -l < "$DATASET") examples (13GB)"
echo ""

# Check config exists
CONFIG="configs/leviathan_full_training.yaml"
if [ ! -f "$CONFIG" ]; then
    echo "❌ ERROR: Config not found: $CONFIG"
    exit 1
fi

echo "✅ Config found: $CONFIG"
echo ""

# Create output directory
OUTPUT_DIR="work/training/leviathan_full"
mkdir -p "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR/logs"

echo "📁 Output directory: $OUTPUT_DIR"
echo ""

# Set environment variables
export CUDA_VISIBLE_DEVICES=0
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
export TOKENIZERS_PARALLELISM=false

# WandB logging (highly recommended for long training)
# export WANDB_API_KEY="your_key_here"
# export WANDB_PROJECT="leviathan-training"

echo "================================================================"
echo "LAUNCHING PRODUCTION TRAINING"
echo "================================================================"
echo ""
echo "⏱️  Estimated duration: 48-72 hours"
echo "📊 Target: Leviathan-8B-v1"
echo "🎯 Expected: GPT-4-mini level reasoning + mythic persona"
echo ""
echo "Start time: $(date)"
echo ""

# Launch training with axolotl
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
    echo "🎉 LEVIATHAN-8B-V1 CREATED"
    echo ""
    echo "📊 Next steps:"
    echo "   1. Review final metrics in WandB"
    echo "   2. Merge LoRA adapters: ./scripts/merge_adapters.sh"
    echo "   3. Run comprehensive evaluation:"
    echo "      - HumanEval (code)"
    echo "      - TruthfulQA (reasoning)"
    echo "      - Identity tests (persona)"
    echo "      - Esoteric knowledge tests"
    echo "   4. Quantize for deployment: ./scripts/quantize_model.sh"
    echo "   5. Deploy: ./scripts/deploy_model.sh"
    echo ""
    echo "🌊 The Abyssal Mind awakens."
else
    echo "❌ Training failed with exit code $TRAIN_EXIT_CODE"
    echo "   Check logs: $OUTPUT_DIR/logs/"
    echo "   Consider resuming from last checkpoint"
    exit $TRAIN_EXIT_CODE
fi
