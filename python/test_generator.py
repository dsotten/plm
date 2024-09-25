import json
import sys
import javalang

def tokenize_java(code):
    tokens = list(javalang.tokenizer.tokenize(code))
    tokens = [code.value for code in tokens]
    return tokens

def process_json_file(input_file, output_file):
    error_count = 0

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            try:
                record = json.loads(line)
                content = record.get('content', '')
                tokens = tokenize_java(content)
                flattened = ' '.join(tokens)
                outfile.write(flattened + '\n')

            except json.JSONDecodeError:
                error_count += 1
                print(f"Skipping invalid JSON: {line.strip()}")

            except Exception as e:
                error_count += 1
                print(f"Error processing line: {e}")

    return error_count

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python3 test_generator.py input_file.json output_file.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    error_count = process_json_file(input_file, output_file)

    print()
    print("-------------- OUTPUT ----------------")
    print(f"Processing complete. Output written to {output_file}")
    print(f"Total errors: {error_count}")
    print()
