#!/usr/bin/env python3
"""
Download PROGRAMMING-SPECIFIC datasets for Claude-like coding assistant behavior
"""

import json
from datasets import load_dataset
from pathlib import Path

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

def download_dataset(name, hf_path, split, max_samples, output_file, format_func):
    """Download and convert a dataset to JSONL format"""
    print_status(f"Downloading {name}...")

    try:
        if max_samples:
            ds = load_dataset(hf_path, split=f"{split}[:{max_samples}]", trust_remote_code=True)
        else:
            ds = load_dataset(hf_path, split=split, trust_remote_code=True)

        print_status(f"  Loaded {len(ds)} samples")

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
        print(f"{Colors.RED}[✗]{Colors.END} Failed: {e}")
        return 0

# Formatters for programming datasets

def format_code_contests(item):
    """Code competition problems"""
    description = item.get("description", "")
    solutions = item.get("solutions", {})

    if not description:
        return None

    # Get Python solution if available
    python_solution = solutions.get("language", [])
    if python_solution and python_solution[0] == 3:  # Python
        solution_code = solutions.get("solution", [""])[0]
        return {
            "instruction": f"Solve this coding problem:\n\n{description}",
            "output": f"```python\n{solution_code}\n```"
        }
    return None

def format_code_search_net(item):
    """Code documentation and search"""
    code = item.get("func_code_string", "")
    docstring = item.get("func_documentation_string", "")

    if not code or not docstring or len(code) < 50:
        return None

    return {
        "instruction": f"Explain this Python function:\n\n```python\n{code}\n```",
        "output": docstring
    }

def format_apps(item):
    """Competitive programming problems"""
    question = item.get("question", "")
    solutions = item.get("solutions", "")

    if not question or not solutions:
        return None

    # Parse solutions JSON
    try:
        sols = json.loads(solutions)
        if sols and len(sols) > 0:
            solution = sols[0]
            return {
                "instruction": question,
                "output": f"```python\n{solution}\n```"
            }
    except:
        pass

    return None

def format_stack_exchange(item):
    """StackExchange programming Q&A"""
    question = item.get("question", "")
    answer = item.get("answer", "")

    if not question or not answer:
        return None

    # Filter for programming content
    if any(keyword in question.lower() for keyword in ["code", "function", "python", "javascript", "java", "c++", "programming", "debug", "error"]):
        return {
            "instruction": question,
            "output": answer
        }

    return None

def format_commit_chronicle(item):
    """Git commit messages and code changes"""
    message = item.get("message", "")
    code_diff = item.get("diff", "")

    if not message or not code_diff or len(code_diff) < 100:
        return None

    return {
        "instruction": f"Explain this code change:\n\n```diff\n{code_diff[:500]}\n```",
        "output": message
    }

def format_spider(item):
    """Text-to-SQL dataset"""
    question = item.get("question", "")
    query = item.get("query", "")
    db_id = item.get("db_id", "")

    if not question or not query:
        return None

    return {
        "instruction": f"Write a SQL query for: {question}\n\nDatabase: {db_id}",
        "output": f"```sql\n{query}\n```"
    }

def format_conala(item):
    """Python code generation from natural language"""
    intent = item.get("intent", "")
    snippet = item.get("snippet", "")

    if not intent or not snippet:
        return None

    return {
        "instruction": f"Write Python code to: {intent}",
        "output": f"```python\n{snippet}\n```"
    }

# Main
def main():
    print(f"""
{Colors.BOLD}{"="*80}
  CLAUDE PROGRAMMING ASSISTANT DATASETS
  Code generation, debugging, explanation, system design
{"="*80}{Colors.END}
""")

    datasets = [
        {
            "name": "Code Search Net Python (Full)",
            "hf_path": "code_search_net",
            "config": "python",
            "split": "train",
            "max_samples": None,
            "output": "code_search_net_python.jsonl",
            "formatter": format_code_search_net,
            "description": "Python function documentation and explanations"
        },
        {
            "name": "CoNaLa (Full)",
            "hf_path": "neulab/conala",
            "config": None,
            "split": "train",
            "max_samples": None,
            "output": "conala_python.jsonl",
            "formatter": format_conala,
            "description": "Natural language → Python code"
        },
        {
            "name": "Spider SQL (Full)",
            "hf_path": "spider",
            "config": None,
            "split": "train",
            "max_samples": None,
            "output": "spider_sql.jsonl",
            "formatter": format_spider,
            "description": "Text-to-SQL generation"
        },
        {
            "name": "Stack Exchange Code (50K)",
            "hf_path": "HuggingFaceH4/stack-exchange-preferences",
            "config": None,
            "split": "train",
            "max_samples": 50000,
            "output": "stack_exchange_code_50k.jsonl",
            "formatter": format_stack_exchange,
            "description": "Programming Q&A from StackOverflow"
        },
    ]

    print_status("Starting programming dataset downloads...\n")

    total = 0
    for ds_config in datasets:
        print(f"\n{Colors.BOLD}{'─'*80}{Colors.END}")
        print(f"{Colors.BOLD}{ds_config['name']}{Colors.END}")
        print(f"  {Colors.BLUE}Description:{Colors.END} {ds_config['description']}")
        print(f"{'─'*80}\n")

        count = download_dataset(
            name=ds_config['name'],
            hf_path=ds_config['hf_path'],
            split=ds_config['split'],
            max_samples=ds_config['max_samples'],
            output_file=ds_config['output'],
            format_func=ds_config['formatter']
        )
        total += count

    print(f"\n{Colors.BOLD}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}  PROGRAMMING DATASETS COMPLETE{Colors.END}")
    print(f"{Colors.BOLD}{'='*80}{Colors.END}\n")

    print_success(f"Total programming samples: {total:,}")

    print(f"\n{Colors.YELLOW}To create ULTIMATE Claude coding assistant:{Colors.END}\n")
    print(f"{Colors.GREEN}cat code_alpaca_full.jsonl code_search_net_python.jsonl conala_python.jsonl spider_sql.jsonl stack_exchange_code_50k.jsonl wizardlm_70k.jsonl alpaca_full.jsonl > claude_coding_full.jsonl{Colors.END}\n")

if __name__ == "__main__":
    # Try simplified version first
    try:
        main()
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")
        print(f"\n{Colors.YELLOW}Downloading simplified programming datasets...{Colors.END}\n")

        # Fallback to Code Alpaca + WizardCoder if main datasets fail
        print_status("Getting WizardCoder (simplified)")
        try:
            ds = load_dataset("WizardLM/WizardCoder-Python-34K-V1.0", split="train")
            count = 0
            with open("wizardcoder_34k.jsonl", "w") as f:
                for item in ds:
                    instruction = item.get("instruction", "")
                    output = item.get("output", "")
                    if instruction and output:
                        f.write(json.dumps({"instruction": instruction, "output": output}) + "\n")
                        count += 1
            print_success(f"WizardCoder: {count:,} samples")
        except Exception as e2:
            print(f"{Colors.RED}Failed: {e2}{Colors.END}")
