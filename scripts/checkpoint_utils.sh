#!/bin/bash
# ============================================================================
# CHECKPOINT MANAGEMENT UTILITIES
# ============================================================================
# Helpful commands for managing training checkpoints
# ============================================================================

# List all checkpoints for a training run
list_checkpoints() {
    local training_dir="${1:-work/training/leviathan_10pct_a4000}"

    echo "================================================"
    echo "CHECKPOINTS IN: $training_dir"
    echo "================================================"
    echo ""

    if [ ! -d "$training_dir" ]; then
        echo "❌ Directory not found: $training_dir"
        return 1
    fi

    checkpoints=$(find "$training_dir" -type d -name "checkpoint-*" | sort -V)

    if [ -z "$checkpoints" ]; then
        echo "No checkpoints found."
        return 0
    fi

    echo "Step      Size      Date Modified"
    echo "------------------------------------------------"

    for ckpt in $checkpoints; do
        step=$(basename "$ckpt" | sed 's/checkpoint-//')
        size=$(du -sh "$ckpt" 2>/dev/null | cut -f1)
        date=$(stat -c %y "$ckpt" 2>/dev/null | cut -d. -f1)
        echo "$step      $size      $date"
    done

    echo ""
    total_size=$(du -sh "$training_dir" 2>/dev/null | cut -f1)
    echo "Total size: $total_size"
}

# Get info about latest checkpoint
latest_checkpoint() {
    local training_dir="${1:-work/training/leviathan_10pct_a4000}"

    latest=$(find "$training_dir" -type d -name "checkpoint-*" | sort -V | tail -1)

    if [ -z "$latest" ]; then
        echo "No checkpoints found in $training_dir"
        return 1
    fi

    step=$(basename "$latest" | sed 's/checkpoint-//')

    echo "================================================"
    echo "LATEST CHECKPOINT"
    echo "================================================"
    echo "Location: $latest"
    echo "Step: $step"
    echo ""

    if [ -f "$latest/trainer_state.json" ]; then
        echo "Training State:"
        python3 -c "
import json, sys
with open('$latest/trainer_state.json') as f:
    state = json.load(f)
    print(f\"  Current Step: {state.get('global_step', 'unknown')}\")
    print(f\"  Epoch: {state.get('epoch', 'unknown')}\")
    print(f\"  Best Loss: {state.get('best_metric', 'unknown')}\")
    if 'log_history' in state and state['log_history']:
        last_log = state['log_history'][-1]
        print(f\"  Last Loss: {last_log.get('loss', 'unknown')}\")
        print(f\"  Learning Rate: {last_log.get('learning_rate', 'unknown')}\")
" 2>/dev/null || echo "  Could not parse trainer state"
    fi

    echo ""
    echo "Files:"
    ls -lh "$latest" | tail -n +2 | awk '{print "  " $9 " (" $5 ")"}'
}

# Delete old checkpoints, keep only N most recent
cleanup_checkpoints() {
    local training_dir="${1:-work/training/leviathan_10pct_a4000}"
    local keep="${2:-2}"

    echo "================================================"
    echo "CHECKPOINT CLEANUP"
    echo "================================================"
    echo "Keeping: $keep most recent checkpoints"
    echo "Directory: $training_dir"
    echo ""

    checkpoints=($(find "$training_dir" -type d -name "checkpoint-*" | sort -V))
    total=${#checkpoints[@]}

    if [ $total -le $keep ]; then
        echo "Only $total checkpoints found. Nothing to delete."
        return 0
    fi

    to_delete=$((total - keep))
    echo "Found $total checkpoints. Will delete $to_delete oldest."
    echo ""

    for ((i=0; i<$to_delete; i++)); do
        ckpt="${checkpoints[$i]}"
        step=$(basename "$ckpt" | sed 's/checkpoint-//')
        size=$(du -sh "$ckpt" 2>/dev/null | cut -f1)
        echo "  Deleting checkpoint-$step ($size)..."
        rm -rf "$ckpt"
    done

    echo ""
    echo "✅ Cleanup complete. $keep checkpoints remaining."
}

# Force save checkpoint (if training is running)
force_checkpoint() {
    local training_dir="${1:-work/training/leviathan_10pct_a4000}"

    echo "================================================"
    echo "FORCE CHECKPOINT SAVE"
    echo "================================================"
    echo ""

    # Check if training is running
    if ! pgrep -f "axolotl.*$training_dir" > /dev/null; then
        echo "❌ No training process found for $training_dir"
        echo "   This only works while training is running"
        return 1
    fi

    echo "⚠️  This will trigger a checkpoint save"
    echo "   Training will pause briefly, then continue"
    read -p "Continue? (yes/no): " -r
    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        echo "Aborted."
        return 0
    fi

    echo ""
    echo "Sending checkpoint signal to training process..."

    # Send SIGUSR1 to trigger checkpoint (if supported)
    pkill -SIGUSR1 -f "axolotl.*$training_dir" || {
        echo "⚠️  Signal not supported. Alternative: Ctrl+C training once"
        echo "   This will save checkpoint and stop training gracefully"
    }
}

# Export checkpoint info to JSON
export_checkpoint_info() {
    local training_dir="${1:-work/training/leviathan_10pct_a4000}"
    local output="${2:-checkpoint_info.json}"

    python3 << EOF
import json
from pathlib import Path
import os

training_dir = Path("$training_dir")
checkpoints = sorted(training_dir.glob("checkpoint-*"), key=lambda x: int(x.name.split('-')[1]))

checkpoint_info = {
    "training_dir": str(training_dir),
    "num_checkpoints": len(checkpoints),
    "checkpoints": []
}

for ckpt in checkpoints:
    step = int(ckpt.name.split('-')[1])
    size = sum(f.stat().st_size for f in ckpt.rglob('*') if f.is_file())

    info = {
        "step": step,
        "path": str(ckpt),
        "size_mb": round(size / 1024 / 1024, 2),
        "files": [f.name for f in ckpt.iterdir() if f.is_file()]
    }

    # Try to load trainer state
    trainer_state_path = ckpt / "trainer_state.json"
    if trainer_state_path.exists():
        with open(trainer_state_path) as f:
            state = json.load(f)
            info["epoch"] = state.get("epoch")
            info["global_step"] = state.get("global_step")
            if state.get("log_history"):
                last_log = state["log_history"][-1]
                info["loss"] = last_log.get("loss")
                info["learning_rate"] = last_log.get("learning_rate")

    checkpoint_info["checkpoints"].append(info)

with open("$output", "w") as f:
    json.dump(checkpoint_info, f, indent=2)

print(f"✅ Checkpoint info exported to $output")
EOF
}

# Display help
show_help() {
    cat << 'EOF'
================================================
CHECKPOINT UTILITIES
================================================

Usage: source scripts/checkpoint_utils.sh

Available commands:

1. list_checkpoints [training_dir]
   List all checkpoints with size and date
   Example: list_checkpoints work/training/leviathan_10pct_a4000

2. latest_checkpoint [training_dir]
   Show detailed info about latest checkpoint
   Example: latest_checkpoint

3. cleanup_checkpoints [training_dir] [keep_count]
   Delete old checkpoints, keep N most recent
   Example: cleanup_checkpoints work/training/leviathan_10pct_a4000 2

4. force_checkpoint [training_dir]
   Trigger checkpoint save while training (if supported)
   Example: force_checkpoint

5. export_checkpoint_info [training_dir] [output_json]
   Export checkpoint metadata to JSON
   Example: export_checkpoint_info work/training/leviathan_10pct_a4000

================================================
Examples:

# Check your checkpoints
list_checkpoints

# See latest checkpoint details
latest_checkpoint

# Keep only 2 most recent, delete rest
cleanup_checkpoints work/training/leviathan_10pct_a4000 2

# Export all checkpoint info
export_checkpoint_info
================================================
EOF
}

# If sourced, make functions available
# If executed directly, show help
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    show_help
fi
