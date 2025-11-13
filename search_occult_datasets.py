#!/usr/bin/env python3
"""
Search HuggingFace for esoteric, occult, demonology, and angelology datasets.
These are rare topics, so we'll search creatively.
"""
import json
from datasets import load_dataset, list_datasets
from pathlib import Path
from tqdm import tqdm
from huggingface_hub import HfApi

output_dir = Path("examples/datasets/occult_esoteric")
output_dir.mkdir(parents=True, exist_ok=True)

def save_dataset(dataset, filename, category, source, max_examples=None):
    """Save dataset in LlamaForge format."""
    examples = []
    skipped = 0

    print(f"  Processing {filename}...")

    for item in tqdm(dataset, desc=f"  {filename}"):
        if max_examples and len(examples) >= max_examples:
            break

        try:
            entry = {}

            # Auto-detect format
            if 'text' in item:
                entry['text'] = str(item['text'])
            elif 'instruction' in item and 'output' in item:
                entry['instruction'] = str(item['instruction'])
                entry['output'] = str(item['output'])
            elif 'question' in item and 'answer' in item:
                entry['instruction'] = str(item['question'])
                entry['output'] = str(item['answer'])
            elif 'content' in item:
                entry['text'] = str(item['content'])
            else:
                skipped += 1
                continue

            # Skip if too short
            full_text = ' '.join(str(v) for v in entry.values())
            if len(full_text) < 100:
                skipped += 1
                continue

            entry['_category'] = category
            entry['_source'] = source
            examples.append(entry)

        except Exception as e:
            skipped += 1
            continue

    if examples:
        output_path = output_dir / filename
        with open(output_path, 'w') as f:
            for ex in examples:
                f.write(json.dumps(ex) + '\n')
        print(f"  ✅ Saved {len(examples):,} examples ({skipped:,} skipped)")
        return len(examples)
    else:
        print(f"  ⚠️  No examples saved (all skipped)")
        return 0

print("\n" + "="*80)
print("SEARCHING HUGGINGFACE FOR OCCULT/ESOTERIC DATASETS")
print("="*80)

occult_count = 0

# Search keywords
occult_keywords = [
    'occult', 'esoteric', 'demonology', 'angelology', 'mysticism',
    'tarot', 'astrology', 'alchemy', 'hermetic', 'kabbalah',
    'mythology', 'religious', 'spiritual', 'metaphysical'
]

print("\n🔍 Searching HuggingFace Hub for relevant datasets...")
print(f"   Keywords: {', '.join(occult_keywords)}")

# Try specific datasets that might contain occult content

# 1. Religious texts
try:
    print("\n📖 Trying religious/spiritual text datasets...")

    # Bible dataset
    try:
        print("  Checking bible datasets...")
        ds = load_dataset("agomberto/biblija", split="train")
        occult_count += save_dataset(ds, "bible_texts.jsonl",
                                    "esoteric", "agomberto/biblija",
                                    max_examples=10000)
    except Exception as e:
        print(f"    ⚠️  agomberto/biblija: {e}")

    # Religious Q&A
    try:
        print("  Checking religious Q&A...")
        ds = load_dataset("sablo/religious_questions", split="train")
        occult_count += save_dataset(ds, "religious_qa.jsonl",
                                    "esoteric", "sablo/religious_questions")
    except Exception as e:
        print(f"    ⚠️  religious_questions: {e}")

except Exception as e:
    print(f"  ⚠️  Error with religious datasets: {e}")

# 2. Mythology datasets
try:
    print("\n🏺 Checking mythology datasets...")

    ds = load_dataset("monsoon-nlp/hindi_wikipedia", split="train")
    # Filter for mythology content
    myth_examples = []
    for item in tqdm(ds, desc="  Filtering mythology"):
        if len(myth_examples) >= 5000:
            break
        text = str(item.get('text', ''))
        if any(kw in text.lower() for kw in ['demon', 'angel', 'deity', 'god', 'goddess',
                                               'spirit', 'ritual', 'mythology']):
            if len(text) > 200:
                myth_examples.append({
                    'text': text,
                    '_category': 'esoteric',
                    '_source': 'monsoon-nlp/hindi_wikipedia'
                })

    if myth_examples:
        with open(output_dir / "mythology_wikipedia.jsonl", 'w') as f:
            for ex in myth_examples:
                f.write(json.dumps(ex) + '\n')
        print(f"  ✅ Saved {len(myth_examples):,} mythology examples")
        occult_count += len(myth_examples)

except Exception as e:
    print(f"  ⚠️  Error with mythology: {e}")

# 3. Wikipedia subset for occult topics
try:
    print("\n📚 Searching Wikipedia for occult topics...")

    # Try English Wikipedia subset
    ds = load_dataset("wikipedia", "20220301.en", split="train", streaming=True)

    occult_wiki = []
    count = 0
    for item in ds:
        if count >= 100000:  # Check first 100k articles
            break
        count += 1

        if len(occult_wiki) >= 5000:
            break

        text = item.get('text', '')
        title = item.get('title', '').lower()

        # Check if article is about occult topics
        if any(kw in title for kw in ['occult', 'esoteric', 'demon', 'angel',
                                       'tarot', 'astrology', 'alchemy', 'mysticism',
                                       'magic', 'ritual', 'supernatural']):
            if len(text) > 500:
                # Create Q&A format
                occult_wiki.append({
                    'instruction': f"Explain the concept of {item.get('title', 'Unknown')} in occult and esoteric traditions.",
                    'output': text[:2000],  # Limit length
                    '_category': 'esoteric',
                    '_source': 'wikipedia_occult'
                })

    if occult_wiki:
        with open(output_dir / "wikipedia_occult.jsonl", 'w') as f:
            for ex in occult_wiki:
                f.write(json.dumps(ex) + '\n')
        print(f"  ✅ Saved {len(occult_wiki):,} Wikipedia occult articles")
        occult_count += len(occult_wiki)
    else:
        print("  ⚠️  No occult articles found in sample")

except Exception as e:
    print(f"  ⚠️  Error with Wikipedia: {e}")

# 4. Books/Literature that might contain occult content
try:
    print("\n📚 Checking literature datasets for occult content...")

    # Project Gutenberg
    try:
        ds = load_dataset("sedthh/gutenberg_english", split="train", streaming=True)

        occult_books = []
        for i, item in enumerate(ds):
            if i >= 10000:  # Check first 10k books
                break
            if len(occult_books) >= 1000:
                break

            text = str(item.get('TEXT', ''))
            title = str(item.get('TITLE', '')).lower()

            if any(kw in title for kw in ['occult', 'magic', 'demon', 'angel',
                                          'mysticism', 'supernatural', 'esoteric']):
                if len(text) > 1000:
                    # Extract meaningful passages
                    occult_books.append({
                        'text': text[:3000],
                        '_category': 'esoteric',
                        '_source': 'gutenberg_occult'
                    })

        if occult_books:
            with open(output_dir / "gutenberg_occult.jsonl", 'w') as f:
                for ex in occult_books:
                    f.write(json.dumps(ex) + '\n')
            print(f"  ✅ Saved {len(occult_books):,} occult literature examples")
            occult_count += len(occult_books)

    except Exception as e:
        print(f"    ⚠️  Gutenberg: {e}")

except Exception as e:
    print(f"  ⚠️  Error with literature: {e}")

# 5. Try any datasets with "tarot", "astrology", etc in name
try:
    print("\n🔮 Searching for datasets with occult terms in name...")

    api = HfApi()

    for keyword in ['tarot', 'astrology', 'occult', 'mysticism']:
        print(f"  Searching for '{keyword}'...")
        try:
            datasets = list(api.list_datasets(search=keyword, limit=10))
            for ds_info in datasets:
                print(f"    Found: {ds_info.id}")
                try:
                    ds = load_dataset(ds_info.id, split="train")
                    occult_count += save_dataset(ds, f"{keyword}_{ds_info.id.replace('/', '_')}.jsonl",
                                                "esoteric", ds_info.id,
                                                max_examples=5000)
                except Exception as e:
                    print(f"      ⚠️  Could not load {ds_info.id}: {e}")
        except Exception as e:
            print(f"    ⚠️  Search failed for {keyword}: {e}")

except Exception as e:
    print(f"  ⚠️  Error with Hub API search: {e}")

# 6. Fallback: Use curated content
print("\n📝 Note: Esoteric datasets are extremely rare on HuggingFace")
print("   Recommendation: Supplement with curated tarot/astrology/occult content")
print("   (See download_real_esoteric_datasets.py output)")

print("\n" + "="*80)
print("SEARCH COMPLETE")
print("="*80)
print(f"📊 Total occult/esoteric examples found: {occult_count:,}")
print(f"📁 Output: {output_dir}")
print()
if occult_count == 0:
    print("⚠️  NO DATASETS FOUND - Occult content is extremely rare on HuggingFace")
    print("   Will need to rely on curated content or external sources")
print("="*80)
