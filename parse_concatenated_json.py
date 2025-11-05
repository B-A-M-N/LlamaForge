import json
import argparse
import sys

def parse_concatenated_json(input_path, output_path):
    """
    Parses a file containing concatenated JSON objects on a single line
    and writes them to a new file in JSON Lines format.
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)

    decoder = json.JSONDecoder()
    idx = 0
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            while idx < len(content):
                # Skip whitespace
                while idx < len(content) and content[idx].isspace():
                    idx += 1
                if idx == len(content):
                    break
                    
                try:
                    obj, end_idx = decoder.raw_decode(content, idx)
                    f.write(json.dumps(obj) + '\n')
                    idx = end_idx
                except json.JSONDecodeError as e:
                    print(f"JSON decoding error at index {idx}: {e}", file=sys.stderr)
                    # Attempt to find the next potential start of a JSON object
                    next_brace = content.find('{', idx + 1)
                    if next_brace == -1:
                        break # No more objects
                    idx = next_brace

    except Exception as e:
        print(f"Error writing to output file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse a file with concatenated JSON objects.")
    parser.add_argument("input_file", help="The path to the input file.")
    parser.add_argument("output_file", help="The path to the output file.")
    args = parser.parse_args()

    print(f"Parsing {args.input_file}...")
    parse_concatenated_json(args.input_file, args.output_file)
    print(f"Successfully created {args.output_file}")
