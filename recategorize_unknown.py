#!/usr/bin/env python3
"""
Recategorize 'unknown' examples in the corpus based on content analysis.
"""
import json
import re
from collections import Counter

def detect_category(example):
    """
    Detect the appropriate category for an example based on content analysis.
    """
    instruction = example.get('instruction', '')
    output = example.get('output', '')
    input_text = example.get('input', '')
    source = example.get('_source', '')

    # Combine all text for analysis
    full_text = f"{instruction} {input_text} {output}".lower()

    # Function/Tool calling detection
    function_patterns = [
        'functioncall', 'function_call', '"name":', '"parameters":',
        'access to the following functions', 'use them if required',
        'external functions', 'function calling'
    ]
    if any(pattern in full_text for pattern in function_patterns):
        return 'tool_api'

    # Code detection
    code_patterns = [
        'def ', 'class ', 'import ', 'function ', '```python', '```javascript',
        '```java', '```cpp', '```c++', 'void ', 'int main', 'public class',
        'console.log', 'printf(', 'println('
    ]
    if any(pattern in full_text for pattern in code_patterns):
        if 'bug' in full_text or 'debug' in full_text or 'error' in full_text or 'fix' in full_text:
            return 'code_debugging'
        elif 'sql' in full_text or 'database' in full_text or 'select ' in full_text:
            return 'sql'
        else:
            return 'code_instruction_multilang'

    # Math/reasoning detection
    math_patterns = [
        r'\$.*\$',  # LaTeX math
        'theorem', 'proof', 'lemma', 'calculate', 'coefficient',
        'equation', 'formula', r'\bx\^', 'expansion of',
        'binomial', 'probability', 'derivative', 'integral'
    ]
    if any(re.search(pattern, full_text) for pattern in math_patterns):
        return 'reasoning_trace'

    # Multi-turn dialogue detection
    dialogue_indicators = [
        'user:', 'assistant:', 'human:', 'ai:',
        'you are a helpful assistant',
        'you are an ai assistant'
    ]
    turns_count = sum(full_text.count(ind) for ind in dialogue_indicators)
    if turns_count >= 2:
        return 'multiturn_dialog'

    # Q&A / Factual knowledge
    qa_patterns = [
        'what is', 'how is', 'why is', 'when is', 'where is',
        'what are', 'how are', 'explain', 'describe', 'define',
        'who is', 'who are', 'can you explain'
    ]
    if any(pattern in full_text[:500] for pattern in qa_patterns):
        if 'step' in full_text or 'first' in full_text or 'second' in full_text:
            return 'reasoning_trace'
        return 'factual_grounding'

    # Creative writing
    creative_patterns = [
        'write a story', 'create a story', 'creative writing',
        'narrative', 'once upon a time', 'story about'
    ]
    if any(pattern in full_text for pattern in creative_patterns):
        return 'creative_narrative'

    # Business/management
    business_patterns = [
        'business', 'company', 'market', 'strategy', 'management',
        'team', 'project', 'client', 'customer'
    ]
    business_count = sum(1 for pattern in business_patterns if pattern in full_text)
    if business_count >= 3:
        return 'instruction'

    # Legal/ethical
    legal_patterns = [
        'legal', 'law', 'court', 'regulation', 'statute',
        'liable', 'liability', 'contract', 'rights'
    ]
    if any(pattern in full_text for pattern in legal_patterns):
        return 'factual_grounding'

    # General instruction following
    instruction_patterns = [
        'provide', 'give', 'list', 'create', 'generate',
        'write', 'make', 'design', 'develop'
    ]
    if any(pattern in instruction[:50].lower() for pattern in instruction_patterns):
        return 'instruction'

    # Default to instruction if it has instruction format
    if instruction and output:
        return 'instruction'

    return 'general_instruction'


def recategorize_corpus(input_file, output_file):
    """
    Recategorize unknown examples in the corpus.
    """
    print("Starting recategorization process...")

    stats = {
        'total_processed': 0,
        'unknown_found': 0,
        'recategorized': 0,
        'new_categories': Counter()
    }

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line_num, line in enumerate(infile, 1):
            if line_num % 100000 == 0:
                print(f"Processed {line_num:,} lines...")

            try:
                data = json.loads(line)
                stats['total_processed'] += 1

                # Recategorize if unknown
                if data.get('_category') == 'unknown':
                    stats['unknown_found'] += 1
                    new_category = detect_category(data)
                    data['_category'] = new_category
                    stats['recategorized'] += 1
                    stats['new_categories'][new_category] += 1

                # Write back
                outfile.write(json.dumps(data) + '\n')

            except Exception as e:
                print(f"Error on line {line_num}: {e}")
                outfile.write(line)

    return stats


def main():
    input_file = '/home/joker/LlamaForge/examples/datasets/FINAL_MERGED_CORPUS_10M.jsonl'
    output_file = '/home/joker/LlamaForge/examples/datasets/RECATEGORIZED_CORPUS.jsonl'

    print("="*80)
    print("RECATEGORIZING UNKNOWN SAMPLES")
    print("="*80)

    stats = recategorize_corpus(input_file, output_file)

    print("\n" + "="*80)
    print("RECATEGORIZATION COMPLETE")
    print("="*80)
    print(f"Total lines processed: {stats['total_processed']:,}")
    print(f"Unknown examples found: {stats['unknown_found']:,}")
    print(f"Examples recategorized: {stats['recategorized']:,}")

    print("\n" + "="*80)
    print("NEW CATEGORY DISTRIBUTION:")
    print("="*80)
    for category, count in stats['new_categories'].most_common():
        pct = (count / stats['recategorized']) * 100 if stats['recategorized'] > 0 else 0
        print(f"{category:.<40} {count:>10,} ({pct:>5.1f}%)")

    print(f"\nOutput written to: {output_file}")


if __name__ == '__main__':
    main()
