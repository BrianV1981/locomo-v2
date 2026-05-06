import json

with open("locomo_v2_final.json", "r") as f:
    dataset = json.load(f)

for row in dataset:
    if row.get("sample_id") == "conv-26":
        for qa in row.get("qa", []):
            if "When did Melanie read the book \"nothing is impossible\"" in qa.get("question", "").lower() or "nothing is impossible" in qa.get("question", "").lower():
                if "[V2_CORRECTION]" not in qa["question"]:
                    qa["question"] = "[V2_CORRECTION] " + qa["question"]
                qa["answer"] = "2022"
                qa["v2_correction"] = True
                print("Patched Q27 in conv-26!")
                break

with open("locomo_v2_final.json", "w") as f:
    json.dump(dataset, f, indent=2)
