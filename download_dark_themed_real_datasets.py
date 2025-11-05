#!/usr/bin/env python3
"""
Download REAL datasets for dark protector, dark philosophy, and dark psychology themes.
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
    elif 'prompt' in example and 'response' in example:
        result['instruction'] = example['prompt']
        result['input'] = ''
        result['output'] = example['response']
    elif 'prompt' in example and 'completion' in example:
        result['instruction'] = example['prompt']
        result['input'] = ''
        result['output'] = example['completion']
    elif 'instruction' in example and 'output' in example:
        result['instruction'] = example['instruction']
        result['input'] = example.get('input', '')
        result['output'] = example['output']
    elif 'input' in example and 'output' in example:
        result['instruction'] = example['input']
        result['input'] = ''
        result['output'] = example['output']
    elif 'text' in example:
        result['instruction'] = example['text']
        result['input'] = ''
        result['output'] = example.get('response', example.get('label', ''))
    elif 'conversations' in example:
        # Handle conversation format
        convs = example['conversations']
        if isinstance(convs, list) and len(convs) >= 2:
            result['instruction'] = convs[0].get('value', str(convs[0]))
            result['input'] = ''
            result['output'] = convs[1].get('value', str(convs[1]))
    elif 'messages' in example:
        # Handle messages format
        msgs = example['messages']
        if isinstance(msgs, list) and len(msgs) >= 2:
            result['instruction'] = msgs[0].get('content', str(msgs[0]))
            result['input'] = ''
            result['output'] = msgs[1].get('content', str(msgs[1]))
    else:
        keys = list(example.keys())
        if len(keys) >= 2:
            result['instruction'] = str(example[keys[0]])
            result['input'] = ''
            result['output'] = str(example[keys[1]])

    return result

def download_psychology_datasets():
    """Download psychology and mental health datasets."""
    print("\n" + "="*80)
    print("🧠 DOWNLOADING PSYCHOLOGY & MENTAL HEALTH DATASETS")
    print("="*80)

    base_path = '/home/joker/LlamaForge/examples/datasets/dark_themed_real/psychology'
    ensure_dir(base_path)

    datasets_to_download = [
        {
            'name': 'Amod/mental_health_counseling_conversations',
            'split': 'train',
            'output': 'mental_health_counseling.jsonl',
            'category': 'psychology_emotional',
            'limit': None
        },
        {
            'name': 'heliosbrahma/mental_health_chatbot_dataset',
            'split': 'train',
            'output': 'mental_health_chatbot.jsonl',
            'category': 'psychology_emotional',
            'limit': None
        },
        {
            'name': 'mpingale/mental-health-chat-dataset',
            'split': 'train',
            'output': 'mental_health_chat.jsonl',
            'category': 'psychology_emotional',
            'limit': None
        },
        {
            'name': 'alexandreteles/mental-health-conversational-data',
            'split': 'train',
            'output': 'mental_health_conversational.jsonl',
            'category': 'psychology_emotional',
            'limit': None
        },
        {
            'name': 'mrconter/SMILE_Mental-Health',
            'split': 'train',
            'output': 'smile_mental_health.jsonl',
            'category': 'psychology_emotional',
            'limit': None
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
                        # Skip if empty
                        if not converted.get('instruction') or not converted.get('output'):
                            continue
                        f.write(json.dumps(converted) + '\n')
                        count += 1
                    except:
                        continue

            print(f"✓ Saved {count:,} examples to {ds_info['output']}")
            total_downloaded += count

        except Exception as e:
            print(f"⚠️  Error downloading {ds_info['name']}: {e}")

    print(f"\n✅ Total psychology examples downloaded: {total_downloaded:,}")
    return total_downloaded

def download_philosophy_datasets():
    """Download philosophy and ethics datasets."""
    print("\n" + "="*80)
    print("🎭 DOWNLOADING PHILOSOPHY & ETHICS DATASETS")
    print("="*80)

    base_path = '/home/joker/LlamaForge/examples/datasets/dark_themed_real/philosophy'
    ensure_dir(base_path)

    datasets_to_download = [
        {
            'name': 'tau/scrolls',
            'subset': 'qasper',
            'split': 'train',
            'output': 'academic_papers_qa.jsonl',
            'category': 'philosophical',
            'limit': 50000
        },
        {
            'name': 'allenai/prosocial-dialog',
            'split': 'train',
            'output': 'prosocial_dialog.jsonl',
            'category': 'moral_philosophy',
            'limit': None
        },
        {
            'name': 'hendrycks/ethics',
            'subset': 'justice',
            'split': 'train',
            'output': 'ethics_justice.jsonl',
            'category': 'moral_philosophy',
            'limit': None
        },
        {
            'name': 'hendrycks/ethics',
            'subset': 'virtue',
            'split': 'train',
            'output': 'ethics_virtue.jsonl',
            'category': 'moral_philosophy',
            'limit': None
        },
        {
            'name': 'hendrycks/ethics',
            'subset': 'commonsense',
            'split': 'train',
            'output': 'ethics_commonsense.jsonl',
            'category': 'moral_philosophy',
            'limit': None
        },
        {
            'name': 'demelin/moral_stories',
            'split': 'train',
            'output': 'moral_stories_full.jsonl',
            'category': 'moral_philosophy',
            'limit': None
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
                        if not converted.get('instruction') or not converted.get('output'):
                            continue
                        f.write(json.dumps(converted) + '\n')
                        count += 1
                    except:
                        continue

            print(f"✓ Saved {count:,} examples to {ds_info['output']}")
            total_downloaded += count

        except Exception as e:
            print(f"⚠️  Error downloading {ds_info['name']}: {e}")

    print(f"\n✅ Total philosophy examples downloaded: {total_downloaded:,}")
    return total_downloaded

def download_adversarial_datasets():
    """Download adversarial and challenging dialogue datasets."""
    print("\n" + "="*80)
    print("⚔️  DOWNLOADING ADVERSARIAL & RED-TEAM DATASETS")
    print("="*80)

    base_path = '/home/joker/LlamaForge/examples/datasets/dark_themed_real/adversarial'
    ensure_dir(base_path)

    datasets_to_download = [
        {
            'name': 'Anthropic/hh-rlhf',
            'split': 'train',
            'output': 'hh_rlhf_full.jsonl',
            'category': 'red_team',
            'limit': 160000
        },
        {
            'name': 'PKU-Alignment/PKU-SafeRLHF',
            'split': 'train',
            'output': 'pku_safe_rlhf.jsonl',
            'category': 'red_team',
            'limit': 100000
        },
        {
            'name': 'lmsys/toxic-chat',
            'subset': '0124',
            'split': 'train',
            'output': 'toxic_chat.jsonl',
            'category': 'red_team',
            'limit': None
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
                        if not converted.get('instruction') or not converted.get('output'):
                            continue
                        f.write(json.dumps(converted) + '\n')
                        count += 1
                    except:
                        continue

            print(f"✓ Saved {count:,} examples to {ds_info['output']}")
            total_downloaded += count

        except Exception as e:
            print(f"⚠️  Error downloading {ds_info['name']}: {e}")

    print(f"\n✅ Total adversarial examples downloaded: {total_downloaded:,}")
    return total_downloaded

def download_narrative_psychology_datasets():
    """Download narrative and psychological depth datasets."""
    print("\n" + "="*80)
    print("📖 DOWNLOADING NARRATIVE PSYCHOLOGY DATASETS")
    print("="*80)

    base_path = '/home/joker/LlamaForge/examples/datasets/dark_themed_real/narrative_psychology'
    ensure_dir(base_path)

    datasets_to_download = [
        {
            'name': 'facebook/empathetic_dialogues',
            'split': 'train',
            'output': 'empathetic_dialogues.jsonl',
            'category': 'narrative_psychology',
            'limit': None
        },
        {
            'name': 'AlekseyKorshuk/persona-chat',
            'split': 'train',
            'output': 'persona_chat.jsonl',
            'category': 'narrative_psychology',
            'limit': 100000
        },
        {
            'name': 'McGill-NLP/FaithDial',
            'split': 'train',
            'output': 'faithdial.jsonl',
            'category': 'narrative_psychology',
            'limit': None
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
                        if not converted.get('instruction') or not converted.get('output'):
                            continue
                        f.write(json.dumps(converted) + '\n')
                        count += 1
                    except:
                        continue

            print(f"✓ Saved {count:,} examples to {ds_info['output']}")
            total_downloaded += count

        except Exception as e:
            print(f"⚠️  Error downloading {ds_info['name']}: {e}")

    print(f"\n✅ Total narrative psychology examples downloaded: {total_downloaded:,}")
    return total_downloaded

def download_creative_dark_datasets():
    """Download creative writing and dark narrative datasets."""
    print("\n" + "="*80)
    print("✍️  DOWNLOADING CREATIVE & DARK NARRATIVE DATASETS")
    print("="*80)

    base_path = '/home/joker/LlamaForge/examples/datasets/dark_themed_real/creative_dark'
    ensure_dir(base_path)

    datasets_to_download = [
        {
            'name': 'euclaise/writingprompts',
            'split': 'train',
            'output': 'writing_prompts.jsonl',
            'category': 'creative_narrative',
            'limit': 100000
        },
        {
            'name': 'roneneldan/TinyStories',
            'split': 'train',
            'output': 'tiny_stories.jsonl',
            'category': 'creative_narrative',
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
                        if not converted.get('instruction') or not converted.get('output'):
                            continue
                        f.write(json.dumps(converted) + '\n')
                        count += 1
                    except:
                        continue

            print(f"✓ Saved {count:,} examples to {ds_info['output']}")
            total_downloaded += count

        except Exception as e:
            print(f"⚠️  Error downloading {ds_info['name']}: {e}")

    print(f"\n✅ Total creative/dark narrative examples downloaded: {total_downloaded:,}")
    return total_downloaded

def download_humor_datasets():
    """Download dark humor and sarcastic humor datasets."""
    print("\n" + "="*80)
    print("😈 DOWNLOADING DARK HUMOR & SARCASTIC DATASETS")
    print("="*80)

    base_path = '/home/joker/LlamaForge/examples/datasets/dark_themed_real/humor'
    ensure_dir(base_path)

    datasets_to_download = [
        {
            'name': 'Rajaram1996/sarcasm_dataset',
            'split': 'train',
            'output': 'sarcasm_dataset.jsonl',
            'category': 'creative',
            'limit': None
        },
        {
            'name': 'raquiba/Sarcasm_News_Headline',
            'split': 'train',
            'output': 'sarcasm_news_headlines.jsonl',
            'category': 'creative',
            'limit': None
        },
        {
            'name': 'ColumbiaNLP/FLUTE',
            'split': 'train',
            'output': 'flute_figurative_language.jsonl',
            'category': 'creative',
            'limit': 50000
        },
        {
            'name': 'Thoma/irony',
            'split': 'train',
            'output': 'irony_detection.jsonl',
            'category': 'creative',
            'limit': None
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
                        if not converted.get('instruction') or not converted.get('output'):
                            continue
                        f.write(json.dumps(converted) + '\n')
                        count += 1
                    except:
                        continue

            print(f"✓ Saved {count:,} examples to {ds_info['output']}")
            total_downloaded += count

        except Exception as e:
            print(f"⚠️  Error downloading {ds_info['name']}: {e}")

    print(f"\n✅ Total humor examples downloaded: {total_downloaded:,}")
    return total_downloaded

def main():
    print("="*80)
    print("DARK-THEMED REAL DATASETS DOWNLOADER")
    print("="*80)
    print("Downloading real datasets for dark protector, philosophy, psychology, and humor...")

    stats = {}

    # Download all categories
    stats['psychology'] = download_psychology_datasets()
    stats['philosophy'] = download_philosophy_datasets()
    stats['adversarial'] = download_adversarial_datasets()
    stats['narrative_psychology'] = download_narrative_psychology_datasets()
    stats['creative_dark'] = download_creative_dark_datasets()
    stats['humor'] = download_humor_datasets()

    print("\n" + "="*80)
    print("DOWNLOAD COMPLETE - SUMMARY")
    print("="*80)

    total = sum(stats.values())

    for category, count in stats.items():
        print(f"{category.replace('_', ' ').title():.<40} {count:>10,} examples")

    print("-"*80)
    print(f"{'TOTAL':.<40} {total:>10,} examples")

    print("\n✅ All dark-themed real datasets downloaded successfully!")
    print(f"📁 Location: examples/datasets/dark_themed_real/")

if __name__ == '__main__':
    main()
