import json

with open("locomo_v2_base.json", "r") as f:
    dataset = json.load(f)

with open("replacement_manifest.json", "r") as f:
    manifest = json.load(f)

try:
    with open("../locomo-visual-ground-truth/llava_7b_cache.json", "r") as f:
        llava = json.load(f)
except:
    llava = {}

img_map = {}
for row in dataset:
    conv = row.get("conversation", {})
    for i in range(1, 100):
        sk = f'session_{i}'
        if sk not in conv: break
        for turn in conv[sk]:
            urls = turn.get("img_url", [])
            if urls and isinstance(urls, list) and urls[0]:
                img_map[urls[0]] = turn

batch_data = []
for item in manifest:
    url = item["new_image_url"]
    turn = img_map.get(url, {})
    desc = llava.get(url, "A photo.")
    batch_data.append({
        "id": item["original_dialogue_id"] + "_" + item["original_question"],
        "category": item["category"],
        "speaker": turn.get("speaker", "Unknown"),
        "text": turn.get("text", ""),
        "description": desc
    })

with open("batch_prompt.json", "w") as f:
    json.dump(batch_data, f, indent=2)
