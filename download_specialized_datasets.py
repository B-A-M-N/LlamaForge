#!/usr/bin/env python3
"""
Download specialized datasets for advanced capabilities.
Focuses on: structured outputs, concise instructions, distillation, tool use, and preferences.
"""
import json
import os
from datasets import load_dataset
from tqdm import tqdm

def ensure_dir(path):
    """Ensure directory exists."""
    os.makedirs(path, exist_ok=True)

def convert_to_instruction_format(example, dataset_name, category):
    """Convert various formats to instruction format."""
    result = {
        '_source': dataset_name,
        '_category': category
    }

    # Handle different formats
    if 'question' in example and 'answer' in example:
        result['instruction'] = example['question']
        result['input'] = ''
        result['output'] = example['answer'] if isinstance(example['answer'], str) else str(example['answer'])
    elif 'prompt' in example and 'completion' in example:
        result['instruction'] = example['prompt']
        result['input'] = ''
        result['output'] = example['completion']
    elif 'instruction' in example and 'output' in example:
        result['instruction'] = example['instruction']
        result['input'] = example.get('input', '')
        result['output'] = example['output']
    elif 'text' in example:
        result['instruction'] = example['text']
        result['input'] = ''
        result['output'] = example.get('response', '')
    else:
        keys = list(example.keys())
        if len(keys) >= 2:
            result['instruction'] = str(example[keys[0]])
            result['input'] = ''
            result['output'] = str(example[keys[1]])

    return result

def download_structured_output_datasets():
    """Download datasets for structured output (JSON, XML, YAML, Markdown)."""
    print("\n" + "="*80)
    print("📋 DOWNLOADING STRUCTURED-OUTPUT DATASETS")
    print("="*80)

    base_path = '/home/joker/LlamaForge/examples/datasets/specialized/structured_output'
    ensure_dir(base_path)

    datasets_to_download = [
        {
            'name': 'b-mc2/sql-create-context',
            'split': 'train',
            'output': 'sql_create_context.jsonl',
            'category': 'sql',
            'limit': 78577  # Full dataset
        },
        {
            'name': 'json-schema-corpus',  # Placeholder - may need alternative
            'skip': True  # Skip if not found
        },
        {
            'name': 'xlangai/spider',
            'split': 'train',
            'output': 'spider_sql.jsonl',
            'category': 'sql',
            'limit': 8659
        },
        {
            'name': 'wikisql',
            'split': 'train',
            'output': 'wikisql.jsonl',
            'category': 'sql',
            'limit': 56355
        },
        {
            'name': 'TokenBender/code_instructions_122k_alpaca_style',
            'split': 'train',
            'output': 'code_instructions_structured.jsonl',
            'category': 'code_instruction_multilang',
            'limit': 100000  # Sample from 122k
        },
        {
            'name': 'HuggingFaceH4/instruction-dataset',
            'split': 'train',
            'output': 'instruction_dataset_structured.jsonl',
            'category': 'instruction',
            'limit': 50000
        },
    ]

    total_downloaded = 0

    for ds_info in datasets_to_download:
        if ds_info.get('skip'):
            continue

        try:
            print(f"\n📥 Downloading {ds_info['name']}...")
            dataset = load_dataset(ds_info['name'], split=ds_info['split'], trust_remote_code=True)

            if ds_info['limit'] and len(dataset) > ds_info['limit']:
                dataset = dataset.shuffle(seed=42).select(range(ds_info['limit']))

            output_path = os.path.join(base_path, ds_info['output'])
            count = 0

            with open(output_path, 'w') as f:
                for example in tqdm(dataset, desc=f"Processing {ds_info['name']}"):
                    try:
                        converted = convert_to_instruction_format(example, ds_info['name'], ds_info['category'])
                        f.write(json.dumps(converted) + '\n')
                        count += 1
                    except:
                        continue

            print(f"✓ Saved {count:,} examples to {ds_info['output']}")
            total_downloaded += count

        except Exception as e:
            print(f"⚠️  Error downloading {ds_info['name']}: {e}")

    print(f"\n✅ Total structured-output examples downloaded: {total_downloaded:,}")
    return total_downloaded

def download_short_context_datasets():
    """Download datasets for short-context instruction following."""
    print("\n" + "="*80)
    print("📝 DOWNLOADING SHORT-CONTEXT INSTRUCTION DATASETS")
    print("="*80)

    base_path = '/home/joker/LlamaForge/examples/datasets/specialized/short_context'
    ensure_dir(base_path)

    datasets_to_download = [
        {
            'name': 'Open-Orca/SlimOrca',
            'split': 'train',
            'output': 'slim_orca.jsonl',
            'category': 'instruction',
            'limit': 300000  # Sample from 518k
        },
        {
            'name': 'yahma/alpaca-cleaned',
            'split': 'train',
            'output': 'alpaca_cleaned.jsonl',
            'category': 'instruction',
            'limit': 51760
        },
        {
            'name': 'vicgalle/alpaca-gpt4',
            'split': 'train',
            'output': 'alpaca_gpt4_short.jsonl',
            'category': 'instruction',
            'limit': 52000
        },
        {
            'name': 'databricks/databricks-dolly-15k',
            'split': 'train',
            'output': 'dolly_15k_short.jsonl',
            'category': 'instruction',
            'limit': 15011
        },
        {
            'name': 'timdettmers/openassistant-guanaco',
            'split': 'train',
            'output': 'guanaco.jsonl',
            'category': 'multiturn_dialog',
            'limit': 9846
        },
        {
            'name': 'tatsu-lab/alpaca',
            'split': 'train',
            'output': 'alpaca_original.jsonl',
            'category': 'instruction',
            'limit': 52002
        },
        {
            'name': 'WizardLM/WizardLM_evol_instruct_V2_196k',
            'split': 'train',
            'output': 'wizardlm_v2.jsonl',
            'category': 'instruction',
            'limit': 150000  # Sample from 196k
        },
        {
            'name': 'teknium/GPT4-LLM-Cleaned',
            'split': 'train',
            'output': 'gpt4_llm_cleaned.jsonl',
            'category': 'instruction',
            'limit': 50000
        },
    ]

    total_downloaded = 0

    for ds_info in datasets_to_download:
        try:
            print(f"\n📥 Downloading {ds_info['name']}...")
            dataset = load_dataset(ds_info['name'], split=ds_info['split'], trust_remote_code=True)

            if ds_info['limit'] and len(dataset) > ds_info['limit']:
                dataset = dataset.shuffle(seed=42).select(range(ds_info['limit']))

            output_path = os.path.join(base_path, ds_info['output'])
            count = 0

            with open(output_path, 'w') as f:
                for example in tqdm(dataset, desc=f"Processing {ds_info['name']}"):
                    try:
                        converted = convert_to_instruction_format(example, ds_info['name'], ds_info['category'])
                        f.write(json.dumps(converted) + '\n')
                        count += 1
                    except:
                        continue

            print(f"✓ Saved {count:,} examples to {ds_info['output']}")
            total_downloaded += count

        except Exception as e:
            print(f"⚠️  Error downloading {ds_info['name']}: {e}")

    print(f"\n✅ Total short-context examples downloaded: {total_downloaded:,}")
    return total_downloaded

def download_tool_api_datasets():
    """Download datasets for tool/API reasoning."""
    print("\n" + "="*80)
    print("🔧 DOWNLOADING TOOL/API REASONING DATASETS")
    print("="*80)

    base_path = '/home/joker/LlamaForge/examples/datasets/specialized/tool_api'
    ensure_dir(base_path)

    datasets_to_download = [
        {
            'name': 'glaiveai/glaive-function-calling-v2',
            'split': 'train',
            'output': 'glaive_function_calling_v2.jsonl',
            'category': 'tool_api',
            'limit': 112960  # Full dataset
        },
        {
            'name': 'NousResearch/hermes-function-calling-v1',
            'split': 'train',
            'output': 'hermes_function_calling.jsonl',
            'category': 'tool_api',
            'limit': 50000
        },
    ]

    total_downloaded = 0

    for ds_info in datasets_to_download:
        try:
            print(f"\n📥 Downloading {ds_info['name']}...")
            dataset = load_dataset(ds_info['name'], split=ds_info['split'], trust_remote_code=True)

            if ds_info['limit'] and len(dataset) > ds_info['limit']:
                dataset = dataset.shuffle(seed=42).select(range(ds_info['limit']))

            output_path = os.path.join(base_path, ds_info['output'])
            count = 0

            with open(output_path, 'w') as f:
                for example in tqdm(dataset, desc=f"Processing {ds_info['name']}"):
                    try:
                        converted = convert_to_instruction_format(example, ds_info['name'], ds_info['category'])
                        f.write(json.dumps(converted) + '\n')
                        count += 1
                    except:
                        continue

            print(f"✓ Saved {count:,} examples to {ds_info['output']}")
            total_downloaded += count

        except Exception as e:
            print(f"⚠️  Error downloading {ds_info['name']}: {e}")

    print(f"\n✅ Total tool/API examples downloaded: {total_downloaded:,}")
    return total_downloaded

def download_preference_dpo_datasets():
    """Download additional preference/DPO datasets."""
    print("\n" + "="*80)
    print("🎯 DOWNLOADING ADDITIONAL PREFERENCE/DPO DATASETS")
    print("="*80)

    base_path = '/home/joker/LlamaForge/examples/datasets/specialized/preference_dpo'
    ensure_dir(base_path)

    datasets_to_download = [
        {
            'name': 'Intel/orca_dpo_pairs',
            'split': 'train',
            'output': 'orca_dpo_pairs.jsonl',
            'category': 'instruction',
            'limit': 100000  # Sample from 130k
        },
        {
            'name': 'argilla/ultrafeedback-binarized-preferences',
            'split': 'train',
            'output': 'ultrafeedback_preferences.jsonl',
            'category': 'instruction',
            'limit': 60000
        },
    ]

    total_downloaded = 0

    for ds_info in datasets_to_download:
        try:
            print(f"\n📥 Downloading {ds_info['name']}...")
            dataset = load_dataset(ds_info['name'], split=ds_info['split'], trust_remote_code=True)

            if ds_info['limit'] and len(dataset) > ds_info['limit']:
                dataset = dataset.shuffle(seed=42).select(range(ds_info['limit']))

            output_path = os.path.join(base_path, ds_info['output'])
            count = 0

            with open(output_path, 'w') as f:
                for example in tqdm(dataset, desc=f"Processing {ds_info['name']}"):
                    try:
                        converted = convert_to_instruction_format(example, ds_info['name'], ds_info['category'])
                        converted['_is_dpo'] = True
                        f.write(json.dumps(converted) + '\n')
                        count += 1
                    except:
                        continue

            print(f"✓ Saved {count:,} examples to {ds_info['output']}")
            total_downloaded += count

        except Exception as e:
            print(f"⚠️  Error downloading {ds_info['name']}: {e}")

    print(f"\n✅ Total preference/DPO examples downloaded: {total_downloaded:,}")
    return total_downloaded

def download_reasoning_compression_datasets():
    """Download datasets for reasoning compression and CoT."""
    print("\n" + "="*80)
    print("🧠 DOWNLOADING REASONING COMPRESSION DATASETS")
    print("="*80)

    base_path = '/home/joker/LlamaForge/examples/datasets/specialized/reasoning_compression'
    ensure_dir(base_path)

    datasets_to_download = [
        {
            'name': 'kaist-ai/CoT-Collection',
            'split': 'train',
            'output': 'cot_collection.jsonl',
            'category': 'reasoning_trace',
            'limit': 100000  # Sample from full dataset
        },
        {
            'name': 'openai/summarize_from_feedback',
            'subset': 'axis',
            'split': 'train',
            'output': 'summarize_feedback.jsonl',
            'category': 'reasoning_trace',
            'limit': 50000
        },
    ]

    total_downloaded = 0

    for ds_info in datasets_to_download:
        try:
            print(f"\n📥 Downloading {ds_info['name']}...")

            if 'subset' in ds_info:
                dataset = load_dataset(ds_info['name'], ds_info['subset'], split=ds_info['split'], trust_remote_code=True)
            else:
                dataset = load_dataset(ds_info['name'], split=ds_info['split'], trust_remote_code=True)

            if ds_info['limit'] and len(dataset) > ds_info['limit']:
                dataset = dataset.shuffle(seed=42).select(range(ds_info['limit']))

            output_path = os.path.join(base_path, ds_info['output'])
            count = 0

            with open(output_path, 'w') as f:
                for example in tqdm(dataset, desc=f"Processing {ds_info['name']}"):
                    try:
                        converted = convert_to_instruction_format(example, ds_info['name'], ds_info['category'])
                        f.write(json.dumps(converted) + '\n')
                        count += 1
                    except:
                        continue

            print(f"✓ Saved {count:,} examples to {ds_info['output']}")
            total_downloaded += count

        except Exception as e:
            print(f"⚠️  Error downloading {ds_info['name']}: {e}")

    print(f"\n✅ Total reasoning compression examples downloaded: {total_downloaded:,}")
    return total_downloaded

def main():
    print("="*80)
    print("SPECIALIZED DATASETS DOWNLOADER")
    print("="*80)
    print("Downloading datasets for advanced capabilities...")

    stats = {}

    # Download all categories
    stats['structured_output'] = download_structured_output_datasets()
    stats['short_context'] = download_short_context_datasets()
    stats['tool_api'] = download_tool_api_datasets()
    stats['preference_dpo'] = download_preference_dpo_datasets()
    stats['reasoning_compression'] = download_reasoning_compression_datasets()

    print("\n" + "="*80)
    print("DOWNLOAD COMPLETE - SUMMARY")
    print("="*80)

    total = sum(stats.values())

    for category, count in stats.items():
        print(f"{category.replace('_', ' ').title():.<40} {count:>10,} examples")

    print("-"*80)
    print(f"{'TOTAL':.<40} {total:>10,} examples")

    print("\n✅ All specialized datasets downloaded successfully!")
    print(f"📁 Location: examples/datasets/specialized/")

if __name__ == '__main__':
    main()
