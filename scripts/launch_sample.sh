#!/bin/bash
# 10% sample test run - 670k examples, 3-4 hours
# Purpose: Validate setup before full training

set -e

echo "========================================="
echo "LEVIATHAN 10% SAMPLE TEST RUN"
echo "========================================="
echo "Dataset: 670k train + 35k val"
echo "Runtime: 3-4 hours"
echo "GPU: A4000 (16GB)"
echo "========================================="

export CUDA_VISIBLE_DEVICES=0

cd /home/joker/LlamaForge

# Create logs directory
mkdir -p logs

echo "Starting sample training..."
python3 llamaforge.py train \
  --config configs/config_leviathan_sample.yaml \
  2>&1 | tee logs/sample_run_$(date +%Y%m%d_%H%M%S).log

echo ""
echo "✅ Sample run complete!"
echo "Check outputs/leviathan_sample_run/ for checkpoints"
echo ""
echo "📊 Key things to verify:"
echo "  - Loss decreased steadily"
echo "  - GPU memory stayed ~14-15GB"
echo "  - No CUDA OOM errors"
echo "  - Checkpoints saved correctly"
echo ""
echo "If all looks good, launch full training with:"
echo "  ./scripts/launch_train.sh"
