import os
import json
import time
import subprocess
import glob
from datetime import datetime

# ==========================================
# CONFIGURATION
# ==========================================
PROJECT_ROOT = "/home/kingb/aim-locomo"
TMUX_SESSION = "17"

# Change this to locomo_v2_minicpm.json or locomo_v2_llava.json when testing flattened datasets
DATA_FILE = "/home/kingb/locomo-v2/data/locomo_v2_web.json"
PREDICTIONS_DIR = "/home/kingb/gemini-benchmarks/reports/locomo_v2/track_a/"
# ==========================================

def send_via_buffer(session, text):
    subprocess.run(["tmux", "set-buffer", text], check=True)
    subprocess.run(["tmux", "paste-buffer", "-t", session], check=True)
    subprocess.run(["tmux", "send-keys", "-t", session, "Enter"], check=True)

def wait_for_response(session, transcript_path, timeout=600):
    start_time = time.time()
    last_size = os.path.getsize(transcript_path)
    while time.time() - start_time < timeout:
        if os.path.getsize(transcript_path) > last_size:
            time.sleep(2) # Give it a moment to finish writing
            with open(transcript_path, 'r') as f:
                content = f.read()
                if "[ANSWER]" in content:
                    return content
            last_size = os.path.getsize(transcript_path)
        time.sleep(2)
    return None

def main():
    # 1. Load questions
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
        
    questions = []
    for sample in data:
        if "qa" in sample:
            for qa in sample["qa"]:
                questions.append(qa)
        elif "question" in sample:
            questions.append(sample)
            
    # The benchmark uses Track A Conv 26
    questions = questions[0:199]
    
    # 2. Find latest prediction file
    prediction_files = glob.glob(os.path.join(PREDICTIONS_DIR, "trackA_predictions_*.json"))
    if not prediction_files:
        print("No prediction files found to resume.")
        return
    latest_file = max(prediction_files, key=os.path.getctime)
    
    with open(latest_file, 'r') as f:
        predictions = json.load(f)
    
    progress = len(predictions)
    print(f"Resuming benchmark from question {progress + 1}")
    
    # 3. Find latest transcript
    transcript_files = glob.glob(os.path.expanduser("~/.gemini/tmp/aim-locomo/chats/*.jsonl"))
    if not transcript_files:
        print("No agent transcript found.")
        return
    latest_transcript = max(transcript_files, key=os.path.getctime)
    
    # 4. Resume loop
    for i in range(progress, len(questions)):
        q = questions[i]
        clean_q = q['question'].replace("[V2_CORRECTION]", "").replace("[LOCOMO-AUDIT]", "").replace("[LOCOMO-ISSUES]", "").replace("[V2_REPLACEMENT]", "").replace("?", ".").replace("$", "").replace("!", "").strip()
        print(f"Sending Question {i+1}: {clean_q}")
        send_via_buffer(TMUX_SESSION, clean_q)
        
        response = wait_for_response(TMUX_SESSION, latest_transcript)
        
        if response:
            answer = response.split("[ANSWER]")[-1].strip()
            # Preserve original question structure in predictions
            pred = q.copy()
            pred["prediction"] = answer
            predictions.append(pred)
            with open(latest_file, 'w') as f:
                json.dump(predictions, f, indent=4)
        else:
            print(f"Timed out on question {i+1}")
            break

if __name__ == "__main__":
    main()
