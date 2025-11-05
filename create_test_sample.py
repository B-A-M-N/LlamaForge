#!/usr/bin/env python3
"""
Create 1% sample for quick testing.
"""
import random

def sample_dataset(input_file, output_file, sample_rate=0.01):
    random.seed(42)

    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            if random.random() < sample_rate:
                f_out.write(line)

    print(f"✅ Created {output_file}")

if __name__ == '__main__':
    sample_dataset('data/train.jsonl', 'data/train_sample.jsonl')
    sample_dataset('data/val.jsonl', 'data/val_sample.jsonl')
    print("Test samples created!")
