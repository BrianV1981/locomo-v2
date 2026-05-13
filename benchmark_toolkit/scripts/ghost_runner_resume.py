import os
import json
import time
import subprocess
import glob
from datetime import datetime

PROJECT_ROOT = "/home/kingb/aim-locomo"
TMUX_SESSION = "17"
DATA_FILE = os.path.join(PROJECT_ROOT, "data/locomo_v2_minicpm.json")

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
        time.sleep(1)
    return None

def main():
    # 1. Load questions
    with open(DATA_FILE, 'r') as f:
        questions = json.load(f)
    
    # 2. Find latest prediction file
    predictions_dir = "/home/kingb/gemini-benchmarks/reports/locomo_v2/track_b/"
    list_of_files = glob.glob(os.path.join(predictions_dir, 'trackB_predictions_*.json'))
    latest_file = max(list_of_files, key=os.path.getctime)
    
    with open(latest_file, 'r') as f:
        predictions = json.load(f)
    
    progress = len(predictions)
    print(f"Resuming benchmark from question {progress + 1}")
    
    # 3. Find latest transcript
    transcript_files = glob.glob(os.path.expanduser("~/.gemini/tmp/aim-locomo/chats/*.jsonl"))
    latest_transcript = max(transcript_files, key=os.path.getctime)
    
    # 4. Resume loop
    for i in range(progress, len(questions)):
        q = questions[i]
        print(f"Sending Question {i+1}: {q['question']}")
        send_via_buffer(TMUX_SESSION, q['question'])
        
        response = wait_for_response(TMUX_SESSION, latest_transcript)
        
        if response:
            answer = response.split("[ANSWER]")[-1].strip()
            predictions.append({"id": q['id'], "question": q['question'], "answer": answer})
            with open(latest_file, 'w') as f:
                json.dump(predictions, f, indent=4)
        else:
            print(f"Timed out on question {i+1}")
            break

if __name__ == "__main__":
    main()
