#!/usr/bin/env python3
"""
Split final corpus into train (95%) and val (5%) sets.
"""
import json
import random
from pathlib import Path

def split_dataset():
    input_file = '/home/joker/LlamaForge/data/FINAL_CLEANED_CORPUS.jsonl'
    train_file = '/home/joker/LlamaForge/data/train.jsonl'
    val_file = '/home/joker/LlamaForge/data/val.jsonl'

    print("="*80)
    print("SPLITTING INTO TRAIN/VAL")
    print("="*80)

    # Load all examples
    examples = []
    with open(input_file, 'r') as f:
        for line in f:
            examples.append(line)

    total = len(examples)
    print(f"Total examples: {total:,}")

    # Shuffle
    random.seed(42)
    random.shuffle(examples)

    # Split 95/5
    split_idx = int(total * 0.95)
    train_examples = examples[:split_idx]
    val_examples = examples[split_idx:]

    # Write train
    with open(train_file, 'w') as f:
        for ex in train_examples:
            f.write(ex)

    # Write val
    with open(val_file, 'w') as f:
        for ex in val_examples:
            f.write(ex)

    print(f"✅ Train: {len(train_examples):,} examples ({len(train_examples)/total*100:.1f}%)")
    print(f"✅ Val:   {len(val_examples):,} examples ({len(val_examples)/total*100:.1f}%)")
    print(f"\n📁 Train: {train_file}")
    print(f"📁 Val:   {val_file}")

if __name__ == '__main__':
    split_dataset()
