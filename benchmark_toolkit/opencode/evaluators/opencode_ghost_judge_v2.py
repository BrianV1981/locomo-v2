#!/usr/bin/env python3
"""
OpenCode Ghost Judge — evaluates Track B predictions using DeepSeek API.
Matches ghost_judge.py logic: YES/NO per question, same forensic judge system prompt.
Uses A.I.M.'s generate_reasoning() for DeepSeek API access (no tmux needed).
"""
import sys, os, json, time, glob

sys.path.insert(0, "/home/kingb/aim-opencode")
sys.path.insert(0, "/home/kingb/aim-opencode/aim_core")
from aim_core.reasoning_utils import generate_reasoning

HUB_ROOT = "/home/kingb/opencode-benchmarks"

# Auto-find latest opencode predictions
pred_files = glob.glob(os.path.join(HUB_ROOT, "reports/locomo_v2/track_b/opencode_trackB_*.json"))
if not pred_files:
    pred_files = glob.glob(os.path.join(HUB_ROOT, "reports/locomo_v2/track_b/opencode_continuation_*.json"))
if not pred_files:
    pred_files = glob.glob(os.path.join(HUB_ROOT, "reports/locomo_v2/track_b/*trackB*.json"))
PREDS_FILE = max(pred_files, key=os.path.getmtime) if pred_files else os.path.join(HUB_ROOT, "reports/locomo_v2/track_b/trackB_predictions_conv1_FINAL.json")
print(f"Predictions: {os.path.basename(PREDS_FILE)}")

timestamp = time.strftime('%Y%m%d_%H%M%S')
OUT_FILE = os.path.join(HUB_ROOT, f"reports/locomo_v2/track_b/opencode_trackB_judged_{timestamp}.json")

with open(PREDS_FILE) as f:
    data = json.load(f)
print(f"Loaded {len(data)} predictions")

agents_md_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "opencode_AGENTS.md")
with open(agents_md_path, "r", encoding="utf-8") as f:
    SYSTEM_INSTRUCTION = f.read()

correct = 0
judged_results = []

for i, qa in enumerate(data):
    # Skip already-judged questions that were marked YES
    if "exact_match" in qa:
        if qa["exact_match"]:
            correct += 1
            continue
        # Re-evaluate NO answers with calibrated rules
        print(f"[{i+1}/{len(data)}] (re-eval) ", end="", flush=True)

    q = qa.get("question", "")
    gt = str(qa.get("answer", qa.get("ground_truth", "")))
    pred = str(qa.get("prediction", "")).strip()

    # Truncate massive predictions
    if len(pred) > 2000:
        pred = pred[:2000]

    prompt = f"Question: {q}\nGround Truth Answer: {gt}\nPredicted Answer: {pred}\n\nIs the Prediction CORRECT? Output ONLY YES or NO:"

    print(f"[{i+1}/{len(data)}] ", end="", flush=True)

    for attempt in range(3):
        try:
            result = generate_reasoning(
                prompt,
                system_instruction=SYSTEM_INSTRUCTION,
                brain_type="default_reasoning"
            ).strip().upper()
        except Exception as e:
            print(f"API error: {e}")
            time.sleep(10)
            continue

        # Clean response
        result = result.replace(".", "").replace('"', "").strip()
        if "YES" in result and "NO" not in result:
            is_match = True
            break
        elif "NO" in result:
            is_match = False
            break
        else:
            print(f"Bad format '{result[:30]}' retry {attempt+1}...")
            time.sleep(3)
    else:
        is_match = False
        result = "PARSE_ERROR"

    qa["exact_match"] = is_match
    qa["judge_raw"] = result

    if is_match:
        correct += 1
        print("YES")
    else:
        print("NO")

    # Save incrementally
    with open(OUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

    if (i + 1) % 20 == 0:
        print(f"  [{i+1}] Running accuracy: {correct}/{i+1} = {correct/(i+1)*100:.1f}%")

    time.sleep(0.3)  # API pacing

accuracy = (correct / len(data)) * 100
print("\n" + "=" * 60)
print("OPENCODE TRACK B RESULTS (DeepSeek V4 Flash Judge)")
print("=" * 60)
print(f"Total: {len(data)}")
print(f"Correct: {correct}")
print(f"Accuracy: {accuracy:.1f}%")
print("=" * 60)
print(f"Results: {OUT_FILE}")
