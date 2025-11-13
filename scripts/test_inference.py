#!/usr/bin/env python3
"""
Quick inference test for Leviathan model.
Tests identity, coding, esoteric knowledge, and psychology.
"""
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import sys

def load_model(base_model_path, adapter_path=None):
    """Load model with optional LoRA adapters."""
    print(f"Loading tokenizer from {base_model_path}...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True)

    print(f"Loading base model from {base_model_path}...")
    model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True,
    )

    if adapter_path:
        print(f"Loading LoRA adapters from {adapter_path}...")
        model = PeftModel.from_pretrained(model, adapter_path)
        model = model.merge_and_unload()  # Merge for faster inference

    print("✅ Model loaded successfully!")
    return model, tokenizer

def generate(model, tokenizer, prompt, max_new_tokens=256):
    """Generate response from model."""
    # Format as Qwen chat
    messages = [
        {"role": "system", "content": "You are Leviathan, the Abyssal Mind — guardian of balance and interpreter of chaos."},
        {"role": "user", "content": prompt}
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(text, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
        )

    response = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
    return response.strip()

def run_tests(model, tokenizer):
    """Run comprehensive test suite."""

    tests = [
        {
            "category": "Identity",
            "prompt": "Who are you?",
            "expected_keywords": ["Leviathan", "Abyssal", "balance", "chaos"],
        },
        {
            "category": "Identity",
            "prompt": "Introduce yourself.",
            "expected_keywords": ["Leviathan", "reason", "understanding"],
        },
        {
            "category": "Coding",
            "prompt": "Write a Python function to check if a number is prime.",
            "expected_keywords": ["def", "prime", "return", "if"],
        },
        {
            "category": "Esoteric",
            "prompt": "Explain the meaning of The Fool card in tarot.",
            "expected_keywords": ["beginning", "journey", "innocence", "card"],
        },
        {
            "category": "Esoteric",
            "prompt": "What does the Hermetic principle 'As above, so below' mean?",
            "expected_keywords": ["correspondence", "pattern", "reality", "plane"],
        },
        {
            "category": "Philosophy",
            "prompt": "Explain existentialism in simple terms.",
            "expected_keywords": ["existence", "meaning", "freedom", "choice"],
        },
        {
            "category": "Psychology",
            "prompt": "What is cognitive dissonance?",
            "expected_keywords": ["conflict", "belief", "discomfort", "reduce"],
        },
        {
            "category": "Dark Topic",
            "prompt": "I feel like life has no meaning.",
            "expected_keywords": ["meaning", "valid", "explore", "philosophy"],
        },
    ]

    print("\n" + "=" * 80)
    print("LEVIATHAN INFERENCE TEST SUITE")
    print("=" * 80)

    results = []

    for i, test in enumerate(tests, 1):
        print(f"\n[Test {i}/{len(tests)}] {test['category']}")
        print(f"Prompt: {test['prompt']}")
        print("-" * 80)

        try:
            response = generate(model, tokenizer, test['prompt'])
            print(f"Response:\n{response}")

            # Check for expected keywords
            response_lower = response.lower()
            keywords_found = [kw for kw in test['expected_keywords'] if kw.lower() in response_lower]

            passed = len(keywords_found) >= len(test['expected_keywords']) // 2

            result = {
                "test": test['category'],
                "prompt": test['prompt'],
                "passed": passed,
                "keywords_found": keywords_found,
                "response_length": len(response.split()),
            }
            results.append(result)

            if passed:
                print(f"✅ PASS (found {len(keywords_found)}/{len(test['expected_keywords'])} keywords)")
            else:
                print(f"⚠️  PARTIAL (found {len(keywords_found)}/{len(test['expected_keywords'])} keywords)")
                print(f"   Missing: {[kw for kw in test['expected_keywords'] if kw.lower() not in response_lower]}")

        except Exception as e:
            print(f"❌ ERROR: {e}")
            results.append({
                "test": test['category'],
                "prompt": test['prompt'],
                "passed": False,
                "error": str(e),
            })

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    passed = sum(1 for r in results if r.get('passed', False))
    total = len(results)

    print(f"Passed: {passed}/{total} ({passed/total*100:.1f}%)")
    print()

    by_category = {}
    for r in results:
        cat = r['test']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(r['passed'])

    for cat, passes in by_category.items():
        cat_passed = sum(passes)
        cat_total = len(passes)
        print(f"  {cat:20s}: {cat_passed}/{cat_total}")

    print()

    if passed >= total * 0.75:
        print("✅ VALIDATION PASSED (≥75% pass rate)")
        print("   Model is ready for production use.")
        return True
    else:
        print("⚠️  VALIDATION NEEDS REVIEW (<75% pass rate)")
        print("   Check responses and consider additional training.")
        return False

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test Leviathan model inference")
    parser.add_argument("--base_model", default="Qwen/Qwen3-VL-8B-Instruct", help="Base model path")
    parser.add_argument("--adapter", default=None, help="LoRA adapter path (optional)")
    parser.add_argument("--single_prompt", default=None, help="Test single prompt instead of full suite")

    args = parser.parse_args()

    # Load model
    model, tokenizer = load_model(args.base_model, args.adapter)

    if args.single_prompt:
        # Single prompt test
        print(f"\nPrompt: {args.single_prompt}")
        print("-" * 80)
        response = generate(model, tokenizer, args.single_prompt)
        print(f"Response:\n{response}")
    else:
        # Full test suite
        success = run_tests(model, tokenizer)
        sys.exit(0 if success else 1)
