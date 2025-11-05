import json
import argparse
import sys

def parse_streamed_json(input_path, output_path):
    """
    Parses a file containing concatenated JSON objects by streaming it
    to avoid loading the entire file into memory.
    """
    decoder = json.JSONDecoder()
    buffer = ""
    
    try:
        with open(input_path, 'r', encoding='utf-8') as infile, \
             open(output_path, 'w', encoding='utf-8') as outfile:
            
            while True:
                chunk = infile.read(8192) # Read in 8KB chunks
                if not chunk:
                    break
                
                buffer += chunk
                
                while buffer:
                    buffer = buffer.lstrip() # Skip leading whitespace
                    if not buffer:
                        break
                        
                    try:
                        obj, end_idx = decoder.raw_decode(buffer)
                        outfile.write(json.dumps(obj) + '\n')
                        buffer = buffer[end_idx:]
                    except json.JSONDecodeError:
                        # Not enough data in buffer for a full JSON object,
                        # break the inner loop to read more from the file.
                        break

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse a file with concatenated JSON objects in a streaming fashion.")
    parser.add_argument("input_file", help="The path to the input file.")
    parser.add_argument("output_file", help="The path to the output file.")
    args = parser.parse_args()

    print(f"Parsing {args.input_file} in a streaming fashion...")
    parse_streamed_json(args.input_file, args.output_file)
    print(f"Successfully created {args.output_file}")
