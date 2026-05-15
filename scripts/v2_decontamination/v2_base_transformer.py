import json
import re
import os

base_path = "/home/kingb/locomo-v2/data/locomo_v2_base.json"
mapping_path = "/home/kingb/locomo-v2/scripts/pipeline/decontamination_mapping.json"
output_path = "/home/kingb/locomo-v2/data/locomo_v2_base_decontaminated_dryrun.json"

with open(base_path, "r") as f:
    data = json.load(f)

with open(mapping_path, "r") as f:
    mapping = json.load(f)

# Combine names and entities into one dictionary
replacements = {}
for k, v in mapping.get("names", {}).items():
    replacements[k] = v
for k, v in mapping.get("entities", {}).items():
    replacements[k] = v

# Sort keys by length descending to prevent partial replacements (e.g., "Melanie" before "Mel")
sorted_keys = sorted(replacements.keys(), key=len, reverse=True)

# Build a single regex pattern for efficiency, using word boundaries
pattern = re.compile(r'\b(' + '|'.join(map(re.escape, sorted_keys)) + r')\b')

def replace_text(text):
    if not isinstance(text, str):
        return text
    return pattern.sub(lambda match: replacements[match.group(1)], text)

def process_dict(d):
    for key, value in d.items():
        if key == "img_url":
            continue # Strictly firewall image URLs and Base64 stubs
        if isinstance(value, str):
            d[key] = replace_text(value)
        elif isinstance(value, list):
            # Process strings in lists (e.g., evidence or answer arrays)
            d[key] = [replace_text(v) if isinstance(v, str) else v for v in value]
            # Recursively process dicts in lists
            for item in d[key]:
                if isinstance(item, dict):
                    process_dict(item)
        elif isinstance(value, dict):
            process_dict(value)

# Run the recursive transformer over every sample
for sample in data:
    process_dict(sample)

os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w") as f:
    json.dump(data, f, indent=2)

print(f"--- Dry Run Completed ---")
print(f"Output saved to {output_path}")

print("\n--- Example QA Pairs After Decontamination ---")
count = 0
for sample in data:
    for qa in sample.get("qa", []):
        print(f"Q: {qa.get('question')}")
        print(f"A: {qa.get('answer')}")
        print("-" * 40)
        count += 1
        if count >= 5:
            break
    if count >= 5:
        break
