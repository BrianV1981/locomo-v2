import json
import re
import os
import copy

base_path = "/home/kingb/locomo-v2/data/locomo_v2_base.json"
mapping_path = "/home/kingb/locomo-v2/scripts/pipeline/decontamination_mapping.json"
image_map_path = "/home/kingb/locomo-visual-ground-truth/maps/image_map.json"

local_output = "/home/kingb/locomo-v2/data/locomo_v2_local.json"
web_output = "/home/kingb/locomo-v2/data/locomo_v2_web.json"

GITHUB_RAW_PREFIX = "https://raw.githubusercontent.com/BrianV1981/locomo-visual-ground-truth/main/images/"
DEAD_STUB = "[LOCOMO-V2-DEAD-URL]"

# 1. Load Data
with open(base_path, "r") as f:
    data = json.load(f)

with open(mapping_path, "r") as f:
    mapping = json.load(f)

# 2. Prepare Decontamination Regex
replacements = {}
for k, v in mapping.get("names", {}).items():
    replacements[k] = v
for k, v in mapping.get("entities", {}).items():
    replacements[k] = v

sorted_keys = sorted(replacements.keys(), key=len, reverse=True)
pattern = re.compile(r'\b(' + '|'.join(map(re.escape, sorted_keys)) + r')\b')

def replace_text(text):
    if not isinstance(text, str):
        return text
    return pattern.sub(lambda match: replacements[match.group(1)], text)

def process_dict(d):
    for key, value in d.items():
        if key == "img_url":
            continue # Protect URLs
        if isinstance(value, str):
            d[key] = replace_text(value)
        elif isinstance(value, list):
            d[key] = [replace_text(v) if isinstance(v, str) else v for v in value]
            for item in d[key]:
                if isinstance(item, dict):
                    process_dict(item)
        elif isinstance(value, dict):
            process_dict(value)

# 3. Apply Decontamination to Base Data
for sample in data:
    process_dict(sample)

with open(base_path, "w") as f:
    json.dump(data, f, indent=2)

print(f"--- 1. Base Dataset Decontaminated & Overwritten ---")

# 4. Generate Local and Web variants using the decontaminated data
with open(image_map_path, "r") as f:
    image_map = json.load(f)

local_data = copy.deepcopy(data)
web_data = copy.deepcopy(data)

def swap_urls(data_copy, is_web):
    swapped = 0
    missing = set()
    for sample in data_copy:
        conv = sample.get("conversation", {})
        for key, turns in conv.items():
            if isinstance(turns, list):
                for turn in turns:
                    img_url = turn.get("img_url")
                    if not img_url: continue
                    
                    if isinstance(img_url, list):
                        new_img_url = []
                        for url in img_url:
                            if url == DEAD_STUB:
                                new_img_url.append(url)
                            elif url in image_map:
                                filename = image_map[url]
                                new_img_url.append(f"{GITHUB_RAW_PREFIX}{filename}" if is_web else f"../images/{filename}")
                                swapped += 1
                            else:
                                new_img_url.append(url)
                                missing.add(url)
                        turn["img_url"] = new_img_url
                    elif isinstance(img_url, str):
                        if img_url == DEAD_STUB:
                            pass
                        elif img_url in image_map:
                            filename = image_map[img_url]
                            turn["img_url"] = f"{GITHUB_RAW_PREFIX}{filename}" if is_web else f"../images/{filename}"
                            swapped += 1
                        else:
                            missing.add(img_url)
    return swapped, missing

local_swapped, local_missing = swap_urls(local_data, is_web=False)
web_swapped, web_missing = swap_urls(web_data, is_web=True)

with open(local_output, "w") as f:
    json.dump(local_data, f, indent=2)

with open(web_output, "w") as f:
    json.dump(web_data, f, indent=2)

print(f"--- 2. Local & Web Datasets Regenerated ---")
print(f"Local swapped: {local_swapped}")
print(f"Web swapped: {web_swapped}")
print("Done.")
