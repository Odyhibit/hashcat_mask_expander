import argparse
import itertools
import string
import sys
from tqdm import tqdm

# Define HashCat wildcards
WILDCARDS = {
    '?a': string.ascii_letters + string.digits + " " + string.punctuation,
    '?d': string.digits,
    '?l': string.ascii_lowercase,
    '?u': string.ascii_uppercase,
    '?h': "0123456789abcdef",
    '?H': "0123456789ABCDEF",
    '?s': " " + string.punctuation
}


# Parse pattern into segments (fixed strings or wildcard lists)
def parse_pattern(pattern):
    result = []
    i = 0
    buffer = ""
    while i < len(pattern):
        if pattern[i] == '?' and i + 1 < len(pattern):
            token = pattern[i:i + 2]
            if token in WILDCARDS:
                if buffer:
                    result.append([buffer])
                    buffer = ""
                result.append(list(WILDCARDS[token]))
                i += 2
                continue
        buffer += pattern[i]
        i += 1
    if buffer:
        result.append([buffer])
    return result


# Estimate output size in bytes
def estimate_size(combos, avg_length):
    return combos * (avg_length + 1)  # +1 for newline


def confirm_large_file(size_bytes):
    size_mb = size_bytes / (1024 * 1024)
    if size_mb > 100:
        confirm = input(
            f"[\\033[91m!\\033[0m] Estimated file size is {size_mb:.2f} MB. Continue? [y/N] ").strip().lower()
        if confirm != 'y':
            print("Aborted.")
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Generate wordlist from HashCat-style pattern.")
    parser.add_argument("pattern", help="Pattern string using HashCat-style wildcards (e.g. NCL-?u?u?u?u-?d?d?d?d)")
    parser.add_argument("-o", "--output", help="Output filename (default: wordlist.txt)")
    args = parser.parse_args()

    output_file = args.output
    if not output_file:
        output_file = input("Enter output filename [wordlist.txt]: ").strip() or "wordlist.txt"

    print("[\\033[92m+\\033[0m] Parsing pattern...")
    parsed = parse_pattern(args.pattern)
    total_combos = 1
    for item in parsed:
        total_combos *= len(item)

    avg_len = sum(len(str(x[0])) if len(x) == 1 else 1 for x in parsed)
    size_bytes = estimate_size(total_combos, avg_len)
    confirm_large_file(size_bytes)

    print(f"[\\033[92m+\\033[0m] Generating {total_combos:,} combinations...")
    combos = itertools.product(*parsed)
    # print(parsed)

    with open(output_file, 'w', encoding='utf-8') as f:
        for combo in tqdm(combos, total=total_combos, unit="words"):
            f.write(''.join(combo) + '\n')

    print(f"[\\033[92m+\\033[0m] Done. Wordlist saved to {output_file}")


if __name__ == "__main__":
    main()
