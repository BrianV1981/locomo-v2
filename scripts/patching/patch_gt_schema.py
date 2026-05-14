import json
import glob

files = [
    "/home/kingb/locomo-v2/data/locomo_v2_llava.json",
    "/home/kingb/locomo-v2/data/locomo_v2_local.json",
    "/home/kingb/locomo-v2/data/locomo_v2_web.json"
]

total_fixed = 0

for file_path in files:
    with open(file_path, "r") as f:
        dataset = json.load(f)
        
    fixed = 0
    for row in dataset:
        for qa in row.get("qa", []):
            if "adversarial_answer" in qa and ("answer" not in qa or str(qa["answer"]).strip() == ""):
                qa["answer"] = qa["adversarial_answer"]
                fixed += 1
                
    if fixed > 0:
        with open(file_path, "w") as f:
            json.dump(dataset, f, indent=2)
        print(f"Fixed {fixed} missing GTs in {file_path}")
        total_fixed += fixed
        
print(f"Total missing GTs standardized: {total_fixed}")
