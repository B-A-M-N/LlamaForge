#!/bin/bash
# Full training run - 8M examples, 2 epochs
# Estimated time: 5-7 days on A4000

set -e

echo "========================================="
echo "LEVIATHAN FULL TRAINING"
echo "========================================="
echo "Dataset: 8M examples"
echo "Epochs: 2"
echo "GPU: A4000 (16GB)"
echo "========================================="

export CUDA_VISIBLE_DEVICES=0

cd /home/joker/LlamaForge

# Create logs directory
mkdir -p logs

echo "Starting training..."
python3 llamaforge.py train \
  --config configs/config_leviathan_local.yaml \
  2>&1 | tee logs/full_run_$(date +%Y%m%d_%H%M%S).log

echo ""
echo "✅ Training complete!"
echo "Check outputs/leviathan_local_run/ for checkpoints"
echo ""
echo "To merge LoRA adapters:"
echo "  python3 llamaforge.py merge \\"
echo "    --base Qwen/Qwen2.5-Coder-7B-Instruct \\"
echo "    --lora outputs/leviathan_local_run \\"
echo "    --output outputs/Leviathan-v1.1"
