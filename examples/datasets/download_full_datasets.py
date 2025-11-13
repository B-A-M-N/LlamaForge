#!/usr/bin/env python3
"""
Download FULL datasets for training Claude-like programming assistants
"""

import json
from datasets import load_dataset
from pathlib import Path
import sys

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_status(msg):
    print(f"{Colors.BLUE}[INFO]{Colors.END} {msg}")

def print_success(msg):
    print(f"{Colors.GREEN}[✓]{Colors.END} {msg}")

def print_warning(msg):
    print(f"{Colors.YELLOW}[!]{Colors.END} {msg}")

def print_error(msg):
    print(f"{Colors.RED}[✗]{Colors.END} {msg}")

def download_dataset(name, hf_path, split, max_samples, output_file, format_func):
    """Download and convert a dataset to JSONL format"""
    print_status(f"Downloading {name}...")

    try:
        # Load dataset
        if max_samples:
            ds = load_dataset(hf_path, split=f"{split}[:{max_samples}]")
        else:
            ds = load_dataset(hf_path, split=split)

        print_status(f"  Loaded {len(ds)} samples")

        # Convert to JSONL
        count = 0
        with open(output_file, "w") as f:
            for item in ds:
                try:
                    formatted = format_func(item)
                    if formatted:
                        f.write(json.dumps(formatted) + "\n")
                        count += 1
                except Exception as e:
                    continue

        file_size_mb = Path(output_file).stat().st_size / (1024 * 1024)
        print_success(f"{name}: {count:,} samples, {file_size_mb:.1f} MB → {output_file}")
        return count

    except Exception as e:
        print_error(f"Failed to download {name}: {e}")
        return 0

# Dataset formatters

def format_alpaca(item):
    """Stanford Alpaca format"""
    instruction = item.get("instruction", "")
    input_text = item.get("input", "")
    output = item.get("output", "")

    if not instruction or not output:
        return None

    if input_text:
        full_instruction = f"{instruction}\n\nInput: {input_text}"
    else:
        full_instruction = instruction

    return {
        "instruction": full_instruction,
        "output": output
    }

def format_code_alpaca(item):
    """Code Alpaca format"""
    instruction = item.get("instruction", "")
    input_text = item.get("input", "")
    output = item.get("output", "")

    if not instruction or not output:
        return None

    # Add programming context
    if input_text:
        full_instruction = f"{instruction}\n\n```\n{input_text}\n```"
    else:
        full_instruction = instruction

    return {
        "instruction": full_instruction,
        "output": output
    }

def format_evol_instruct(item):
    """WizardLM Evol-Instruct format"""
    instruction = item.get("instruction", "")
    output = item.get("output", "")

    if not instruction or not output or len(instruction) < 10:
        return None

    return {
        "instruction": instruction,
        "output": output
    }

def format_open_orca(item):
    """OpenOrca format"""
    system = item.get("system_prompt", "")
    question = item.get("question", "")
    response = item.get("response", "")

    if not question or not response:
        return None

    # Combine system prompt with question
    if system and system != "You are an AI assistant. User will you give you a task. Your goal is to complete the task as faithfully as you can. While performing the task think step-by-step and justify your steps.":
        full_instruction = f"{system}\n\n{question}"
    else:
        full_instruction = question

    return {
        "instruction": full_instruction,
        "output": response
    }

def format_magicoder(item):
    """Magicoder format - code-focused"""
    problem = item.get("problem", "")
    solution = item.get("solution", "")

    if not problem or not solution:
        return None

    return {
        "instruction": problem,
        "output": solution
    }

def format_codealpaca(item):
    """CodeAlpaca 20k format"""
    instruction = item.get("instruction", "")
    input_text = item.get("input", "")
    output = item.get("output", "")

    if not instruction or not output:
        return None

    if input_text:
        full_instruction = f"{instruction}\n\n{input_text}"
    else:
        full_instruction = instruction

    return {
        "instruction": full_instruction,
        "output": output
    }

# Main download script
def main():
    print(f"""
{Colors.BOLD}{"="*80}
  FULL DATASET DOWNLOADER - Claude-like Programming Assistant Training
{"="*80}{Colors.END}
""")

    datasets = [
        {
            "name": "Alpaca Full (52K)",
            "hf_path": "yahma/alpaca-cleaned",
            "split": "train",
            "max_samples": None,  # All samples
            "output": "alpaca_full.jsonl",
            "formatter": format_alpaca,
            "description": "General instruction following, diverse tasks"
        },
        {
            "name": "Code Alpaca (20K)",
            "hf_path": "sahil2801/CodeAlpaca-20k",
            "split": "train",
            "max_samples": None,
            "output": "code_alpaca_full.jsonl",
            "formatter": format_codealpaca,
            "description": "Programming tasks, code generation, debugging"
        },
        {
            "name": "WizardLM Evol-Instruct (70K)",
            "hf_path": "WizardLM/WizardLM_evol_instruct_70k",
            "split": "train",
            "max_samples": None,
            "output": "wizardlm_70k.jsonl",
            "formatter": format_evol_instruct,
            "description": "Complex reasoning, detailed responses"
        },
        {
            "name": "OpenOrca (100K subset)",
            "hf_path": "Open-Orca/OpenOrca",
            "split": "train",
            "max_samples": 100000,  # First 100K (full is 4M+)
            "output": "openorca_100k.jsonl",
            "formatter": format_open_orca,
            "description": "Reasoning, explanations, step-by-step thinking"
        },
    ]

    print_status("Starting downloads...\n")

    total_samples = 0
    successful = 0

    for ds in datasets:
        print(f"\n{Colors.BOLD}{'─'*80}{Colors.END}")
        print(f"{Colors.BOLD}{ds['name']}{Colors.END}")
        print(f"  {Colors.BLUE}Description:{Colors.END} {ds['description']}")
        print(f"  {Colors.BLUE}Output:{Colors.END} {ds['output']}")
        print(f"{'─'*80}\n")

        count = download_dataset(
            name=ds['name'],
            hf_path=ds['hf_path'],
            split=ds['split'],
            max_samples=ds['max_samples'],
            output_file=ds['output'],
            format_func=ds['formatter']
        )

        if count > 0:
            total_samples += count
            successful += 1

    print(f"\n{Colors.BOLD}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}  DOWNLOAD COMPLETE{Colors.END}")
    print(f"{Colors.BOLD}{'='*80}{Colors.END}\n")

    print_success(f"Successfully downloaded {successful}/{len(datasets)} datasets")
    print_success(f"Total samples: {total_samples:,}")

    print(f"\n{Colors.YELLOW}Recommended Training Commands:{Colors.END}\n")

    print("1. General Assistant (Alpaca):")
    print(f"   {Colors.GREEN}python llamaforge.py --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 \\")
    print(f"     --data examples/datasets/alpaca_full.jsonl --epochs 3 --max-length 512{Colors.END}\n")

    print("2. Programming Assistant (Code Alpaca):")
    print(f"   {Colors.GREEN}python llamaforge.py --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 \\")
    print(f"     --data examples/datasets/code_alpaca_full.jsonl --epochs 3 --max-length 1024{Colors.END}\n")

    print("3. Reasoning Assistant (WizardLM):")
    print(f"   {Colors.GREEN}python llamaforge.py --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 \\")
    print(f"     --data examples/datasets/wizardlm_70k.jsonl --epochs 2 --max-length 768{Colors.END}\n")

    print("4. Claude-like Assistant (OpenOrca):")
    print(f"   {Colors.GREEN}python llamaforge.py --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 \\")
    print(f"     --data examples/datasets/openorca_100k.jsonl --epochs 1 --max-length 1024{Colors.END}\n")

    print(f"{Colors.YELLOW}Combined Training (Best Results):{Colors.END}")
    print("   Concatenate datasets for maximum capability:")
    print(f"   {Colors.GREEN}cat alpaca_full.jsonl code_alpaca_full.jsonl wizardlm_70k.jsonl > combined_training.jsonl")
    print(f"   python llamaforge.py --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 \\")
    print(f"     --data examples/datasets/combined_training.jsonl --epochs 2{Colors.END}\n")

if __name__ == "__main__":
    main()
