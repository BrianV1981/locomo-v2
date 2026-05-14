import os
import json
import re
import glob

# Assumes it is run from the root of locomo-v2
def get_processor():
    mapping_path = os.path.join(os.path.dirname(__file__), 'decontamination_mapping.json')
    with open(mapping_path, 'r') as f:
        mapping = json.load(f)
    names = mapping['names']
    entities = mapping['entities']
    year_shift = mapping['temporal_shift']['years']
    replace_dict = {**names, **entities}
    sorted_replace_keys = sorted(replace_dict.keys(), key=len, reverse=True)

    def process_text(text):
        if not isinstance(text, str): return text
        if year_shift != 0:
            def year_replacer(match):
                return str(int(match.group(1)) + year_shift)
            text = re.sub(r'\b(199[0-9]|20[0-2][0-9])\b', year_replacer, text)
        for old_val in sorted_replace_keys:
            new_val = replace_dict[old_val]
            escaped_old = re.escape(old_val)
            prefix = r'\b' if old_val[0].isalnum() else ''
            suffix = r'\b' if old_val[-1].isalnum() else ''
            pattern = prefix + escaped_old + suffix
            text = re.sub(pattern, new_val, text)
        return text
    return process_text

processor = get_processor()

def traverse(obj, key=None):
    if key and ("url" in key.lower() or "caption" in key.lower() or key in ["id", "sample_id", "dia_id"]):
        return obj
    if isinstance(obj, dict):
        return {k: traverse(v, key=k) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [traverse(v) for v in obj]
    elif isinstance(obj, str):
        return processor(obj)
    else:
        return obj

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    
    web_file = os.path.join(data_dir, 'locomo_v2_web.json')
    regen_file = os.path.join(data_dir, 'regenerated_questions.json')
    
    print("Processing locomo_v2_web.json...")
    if os.path.exists(web_file):
        with open(web_file, 'r', encoding='utf-8') as f:
            web_dataset = json.load(f)
        new_web_dataset = traverse(web_dataset)
        with open(web_file, 'w', encoding='utf-8') as f:
            json.dump(new_web_dataset, f, indent=4)

    print("Processing regenerated_questions.json...")
    if os.path.exists(regen_file):
        with open(regen_file, 'r', encoding='utf-8') as f:
            regen_dataset = json.load(f)
        new_regen_dataset = traverse(regen_dataset)
        with open(regen_file, 'w', encoding='utf-8') as f:
            json.dump(new_regen_dataset, f, indent=4)

    print("Decontamination transformation complete.")

if __name__ == "__main__":
    main()
