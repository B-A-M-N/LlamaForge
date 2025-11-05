#!/bin/bash
# Quick test run - 1% sample, ~30-45 min

set -e

echo "========================================="
echo "LEVIATHAN TEST RUN (1% sample)"
echo "========================================="

export CUDA_VISIBLE_DEVICES=0

cd /home/joker/LlamaForge

echo "Running training with test config..."
python3 llamaforge.py train \
  --config configs/config_leviathan_test.yaml \
  2>&1 | tee logs/test_run_$(date +%Y%m%d_%H%M%S).log

echo ""
echo "✅ Test run complete!"
echo "Check outputs/leviathan_test_run/ for checkpoints"
