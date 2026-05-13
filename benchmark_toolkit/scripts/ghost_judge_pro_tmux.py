import os
import json
import time
import subprocess
import glob
from datetime import datetime

JUDGE_ROOT = "/home/kingb/gemini-benchmarks/evaluators"
TMUX_SESSION = f"pro_judge_{int(time.time())}"
INPUT_FILE = "/home/kingb/gemini-benchmarks/reports/locomo_v2/track_b/trackB_predictions_20260511_203738.json"
OUTPUT_FILE = f"/home/kingb/gemini-benchmarks/reports/locomo_v2/track_b/trackB_FINAL_PRO_TMUX_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
AGENTS_POLICY = "/home/kingb/gemini-benchmarks/evaluators/AGENTS.md"

def get_latest_transcript(session_name):
    # Search in all potential chat directories
    search_dir = os.path.expanduser("~/.gemini/tmp/evaluators/chats/*.jsonl")
    files = glob.glob(search_dir)
    if not files: return None
    return sorted(files)[-1]

# 1. Start the judge session
old_transcript = get_latest_transcript(TMUX_SESSION)
subprocess.run(["tmux", "new-session", "-d", "-s", TMUX_SESSION, "-c", JUDGE_ROOT, "gemini", "--yolo", "-m", "gemini-3.1-pro-preview", "--policy", AGENTS_POLICY])

print(f"Waiting for new transcript... Old was {old_transcript}")
transcript_path = old_transcript
for _ in range(20):
    time.sleep(2)
    current = get_latest_transcript(TMUX_SESSION)
    if current and current != old_transcript:
        transcript_path = current
        break

print(f"Using transcript: {transcript_path}")
last_line_count = 0
if transcript_path:
    with open(transcript_path, "r") as f:
        last_line_count = len(f.readlines())

def wait_for_response(transcript_path, last_line_count):
    start_time = time.time()
    while time.time() - start_time < 300:
        if os.path.exists(transcript_path):
            with open(transcript_path, "r") as f:
                lines = f.readlines()
                if len(lines) > last_line_count:
                    # Parse the new lines
                    for line in lines[last_line_count:]:
                        try:
                            msg = json.loads(line)
                            if msg.get("type") == "gemini":
                                content = msg.get("content", "").strip().upper()
                                import re
                                match = re.search(r"\b(YES|NO)\b", content)
                                if match:
                                    return match.group(1), len(lines)
                        except: continue
        time.sleep(1)
    return "TIMEOUT", last_line_count

# 2. Process questions
with open(INPUT_FILE, "r") as f:
    data = json.load(f)

results = []
for i, qa in enumerate(data):
    gt = qa.get('answer', qa.get('adversarial_answer', qa.get('ground_truth', '')))
    prompt = f"Question: {qa['question']} GT: {gt} Prediction: {qa['prediction']} Is the Prediction CORRECT. Output ONLY YES or NO:".replace("\n", " ").replace("$", "").replace("!", "").replace("?", ".")
    
    with open("/tmp/prompt.txt", "w") as f: f.write(prompt)
    subprocess.run(["tmux", "load-buffer", "/tmp/prompt.txt"])
    subprocess.run(["tmux", "paste-buffer", "-t", TMUX_SESSION])
    subprocess.run(["tmux", "send-keys", "-t", TMUX_SESSION, "Enter"])
    import time; time.sleep(0.5)
    subprocess.run(["tmux", "send-keys", "-t", TMUX_SESSION, "Enter"])
    
    response, last_line_count = wait_for_response(transcript_path, last_line_count)
    qa["is_correct"] = response
    results.append(qa)
    with open(OUTPUT_FILE, "w") as f: json.dump(results, f)
    print(f"Judged {i+1}/{len(data)}: {response}", flush=True)
    time.sleep(5)

