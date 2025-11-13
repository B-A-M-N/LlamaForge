#!/bin/bash
# ============================================================================
# PRE-FLIGHT CHECK - Verify system ready for training
# ============================================================================
# Run this before starting training to verify everything is in place
# ============================================================================

set -e

echo "================================================================"
echo "LEVIATHAN TRAINING - PRE-FLIGHT CHECK"
echo "================================================================"
echo ""

ERRORS=0
WARNINGS=0

# Function to check file exists
check_file() {
    local file=$1
    local description=$2
    if [ -f "$file" ]; then
        size=$(du -sh "$file" 2>/dev/null | cut -f1)
        echo "✅ $description: $size"
    else
        echo "❌ MISSING: $description"
        echo "   Expected: $file"
        ((ERRORS++))
    fi
}

# Function to check directory
check_dir() {
    local dir=$1
    local description=$2
    if [ -d "$dir" ]; then
        echo "✅ $description"
    else
        echo "⚠️  WILL CREATE: $description"
        ((WARNINGS++))
    fi
}

echo "📦 CHECKING DATASETS..."
echo ""
check_file "examples/datasets/FINAL_CORPUS_7M_PLUS_ESOTERIC.jsonl" "Full corpus (5.5M examples)"
check_file "examples/datasets/LEVIATHAN_10PCT_SAMPLE.jsonl" "10% sample (559K examples)"
echo ""

echo "⚙️  CHECKING CONFIGS..."
echo ""
check_file "configs/leviathan_10pct_a4000.yaml" "A4000 10% test config"
check_file "configs/leviathan_10pct_test.yaml" "A100 10% test config"
check_file "configs/leviathan_full_training.yaml" "A100 full training config"
echo ""

echo "🚀 CHECKING SCRIPTS..."
echo ""
check_file "scripts/train_10pct_a4000.sh" "A4000 training script"
check_file "scripts/train_10pct_test.sh" "A100 test script"
check_file "scripts/train_full.sh" "A100 full training script"
check_file "scripts/checkpoint_utils.sh" "Checkpoint utilities"
echo ""

echo "📚 CHECKING DOCUMENTATION..."
echo ""
check_file "LEVIATHAN_TRAINING_READY.md" "Training ready summary"
check_file "TRAINING_OPTIONS_SUMMARY.md" "Training options guide"
check_file "A4000_TRAINING_GUIDE.md" "A4000 optimization guide"
check_file "docs/TRAINING_GUIDE.md" "Complete training manual"
check_file "docs/CHECKPOINTING_GUIDE.md" "Checkpointing guide"
echo ""

echo "🎮 CHECKING GPU..."
echo ""
if ! command -v nvidia-smi &> /dev/null; then
    echo "❌ nvidia-smi not found - GPU not available"
    ((ERRORS++))
else
    GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader | head -1)
    GPU_MEM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1)
    GPU_FREE=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -1)

    echo "✅ GPU: $GPU_NAME"
    echo "   Total Memory: ${GPU_MEM} MB"
    echo "   Free Memory: ${GPU_FREE} MB"

    if [[ "$GPU_NAME" =~ "A4000" ]]; then
        echo "   ✅ A4000 detected - use train_10pct_a4000.sh"
    elif [[ "$GPU_NAME" =~ "A100" ]]; then
        echo "   ✅ A100 detected - use train_10pct_test.sh or train_full.sh"
    else
        echo "   ⚠️  GPU not recognized - may need config adjustments"
        ((WARNINGS++))
    fi

    if (( GPU_MEM < 15000 )); then
        echo "   ❌ Insufficient VRAM: ${GPU_MEM}MB (need 16GB+)"
        ((ERRORS++))
    fi
fi
echo ""

echo "💾 CHECKING DISK SPACE..."
echo ""
AVAILABLE=$(df -h . | tail -1 | awk '{print $4}')
echo "✅ Available: $AVAILABLE"
echo "   Required: ~100GB for training (checkpoints + logs)"
echo ""

echo "🐍 CHECKING PYTHON ENVIRONMENT..."
echo ""
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo "✅ $PYTHON_VERSION"
else
    echo "❌ Python 3 not found"
    ((ERRORS++))
fi

if python3 -c "import torch" 2>/dev/null; then
    TORCH_VERSION=$(python3 -c "import torch; print(torch.__version__)")
    CUDA_AVAILABLE=$(python3 -c "import torch; print(torch.cuda.is_available())")
    echo "✅ PyTorch $TORCH_VERSION"
    echo "   CUDA available: $CUDA_AVAILABLE"

    if [ "$CUDA_AVAILABLE" != "True" ]; then
        echo "   ❌ CUDA not available in PyTorch"
        ((ERRORS++))
    fi
else
    echo "❌ PyTorch not installed"
    ((ERRORS++))
fi

if python3 -c "import axolotl" 2>/dev/null; then
    echo "✅ Axolotl installed"
else
    echo "❌ Axolotl not installed"
    echo "   Install: pip install axolotl[flash-attn]"
    ((ERRORS++))
fi
echo ""

echo "📁 CHECKING OUTPUT DIRECTORIES..."
echo ""
check_dir "work" "Work directory"
check_dir "work/training" "Training output directory"
echo ""

echo "================================================================"
echo "PRE-FLIGHT CHECK COMPLETE"
echo "================================================================"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "🎉 ALL SYSTEMS GO!"
    echo ""
    echo "Ready to start training:"
    echo "  • For A4000 (24-36 hrs):  ./scripts/train_10pct_a4000.sh"
    echo "  • For A100 test (4-6 hrs): ./scripts/train_10pct_test.sh"
    echo "  • For A100 full (48-72 hrs): ./scripts/train_full.sh"
    echo ""
    echo "📖 Read guides first:"
    echo "  • TRAINING_OPTIONS_SUMMARY.md - Choose your strategy"
    echo "  • A4000_TRAINING_GUIDE.md - A4000-specific tips"
    echo "  • docs/CHECKPOINTING_GUIDE.md - Pause/resume training"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo "⚠️  READY WITH WARNINGS: $WARNINGS warnings"
    echo ""
    echo "System should work, but review warnings above."
    echo "Ready to start training if warnings are acceptable."
    exit 0
else
    echo "❌ NOT READY: $ERRORS errors, $WARNINGS warnings"
    echo ""
    echo "Fix errors above before starting training."
    exit 1
fi
