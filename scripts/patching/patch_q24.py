import json

with open("locomo_v2_final.json", "r") as f:
    dataset = json.load(f)

for row in dataset:
    if row.get("sample_id") == "conv-26":
        for qa in row.get("qa", []):
            if "What books has Melanie read?" in qa.get("question", ""):
                qa["question"] = "[V2_CORRECTION] " + qa["question"]
                qa["answer"] = "Charlotte's Web and Nothing is Impossible"
                qa["v2_correction"] = True
                print("Patched Q24 in conv-26!")
                break

with open("locomo_v2_final.json", "w") as f:
    json.dump(dataset, f, indent=2)
