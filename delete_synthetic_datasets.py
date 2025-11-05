#!/usr/bin/env python3
"""
Delete ALL Synthetic Datasets - Quality Upgrade

Removes ~11GB of synthetic/duplicated data:
1. ultimate_3M_intelligently_duplicated.jsonl (5GB) - Pure synthetic inflation
2. expanded_training_1.5M.jsonl (2.7GB) - Synthetic expansion
3. claude_behavioral_mix.jsonl (1.7GB) - Mixed/synthetic
4. chatgpt_behavioral_mix.jsonl (1.3GB) - Mixed/synthetic
5. esoteric_studies_mix.jsonl (260MB) - Synthetic mix
6. deepseek_search_mix.jsonl (175MB) - Synthetic mix
7. code_debugging_mix.jsonl (31MB) - Synthetic mix

Replaced with:
- Dark protector actual: 60M real (open-instruct-uncensored 1.7M examples)
- Real alternatives: 50M real (MentalChat16K, WebQuestions, CodeAlpaca)
- Phase 5 fast: 391M real (GSM8K, ARC, CommonsenseQA, etc.)
"""

import os
from pathlib import Path

def delete_synthetic_datasets():
    """Delete all identified synthetic datasets."""

    synthetic_files = [
        "examples/datasets/ultimate_3M_intelligently_duplicated.jsonl",
        "examples/datasets/expanded_training_1.5M.jsonl",
        "examples/datasets/claude_behavioral_mix.jsonl",
        "examples/datasets/chatgpt_behavioral_mix.jsonl",
        "examples/datasets/esoteric_studies_mix.jsonl",
        "examples/datasets/deepseek_search_mix.jsonl",
        "examples/datasets/code_debugging_mix.jsonl",
    ]

    total_size = 0
    deleted_count = 0

    print("=" * 80)
    print(" DELETING SYNTHETIC DATASETS")
    print(" Removing ~11GB of synthetic/duplicated data")
    print("=" * 80)
    print()

    for file_path in synthetic_files:
        path = Path(file_path)

        if path.exists():
            # Get file size before deletion
            size_bytes = path.stat().st_size
            size_mb = size_bytes / (1024 * 1024)
            size_gb = size_bytes / (1024 * 1024 * 1024)

            total_size += size_bytes

            # Display size appropriately
            if size_gb >= 1:
                size_str = f"{size_gb:.1f}GB"
            else:
                size_str = f"{size_mb:.0f}MB"

            print(f"[→] Deleting: {path.name}")
            print(f"    Size: {size_str}")

            # Delete the file
            path.unlink()
            deleted_count += 1

            print(f"[✓] Deleted: {path.name}")
            print()
        else:
            print(f"[!] Not found: {path.name} (may have been deleted already)")
            print()

    # Calculate total size deleted
    total_gb = total_size / (1024 * 1024 * 1024)

    print("=" * 80)
    print(f"[✓] DELETION COMPLETE")
    print(f"    Files deleted: {deleted_count}")
    print(f"    Space freed: {total_gb:.2f}GB")
    print("=" * 80)
    print()

    # Show what we now have
    print("Real datasets now available:")
    print("  - dark_protector_actual: 60M (1.7M examples from open-instruct-uncensored)")
    print("  - real_alternatives: 50M (38K examples from MentalChat16K, WebQuestions, CodeAlpaca)")
    print("  - expansion_phase5_fast: 391M (168K+ examples from GSM8K, ARC, etc.)")
    print()
    print("Next step: Final merge of ALL REAL datasets only")
    print()

    return deleted_count, total_gb

if __name__ == "__main__":
    deleted, freed_gb = delete_synthetic_datasets()

    if deleted > 0:
        print(f"✅ Successfully deleted {deleted} synthetic datasets, freed {freed_gb:.2f}GB")
    else:
        print("⚠️ No files were deleted (may have been deleted already)")
