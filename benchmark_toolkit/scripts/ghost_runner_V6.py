#!/usr/bin/env python3
import os
import json
import time
import subprocess
import glob
from datetime import datetime

# ==========================================
# V6 MARATHON BENCHMARK CONFIGURATION
# ==========================================

# The exact name of the tmux session the script will target and inject prompts into.
TARGET_TMUX_SESSION = "run_20260512_161607"

# The path to the dataset you want to run.
DATASET_FILE = "/home/kingb/gemini-benchmarks/data/locomo_v2/locomo_v2_session0.json"

# The path where predictions will be saved. The script will automatically resume if this file exists.
OUT_FILE = "/home/kingb/gemini-benchmarks/reports/locomo_v2/track_b/trackB_predictions_V6_SESSION_0.json"

# Pacing: How many seconds to wait AFTER a successful answer before sending the next question.
PACING_DELAY_SECONDS = 60

# Cooldown: How many seconds to wait AFTER hitting a timeout/429 error before retrying.
COOLDOWN_DELAY_SECONDS = 180

# Maximum amount of time (in seconds) to wait for the agent to finish "Thinking" before assuming a timeout.
THINKING_TIMEOUT_SECONDS = 300

# ==========================================

PROJECT_ROOT = "/home/kingb/aim-locomo"

def get_latest_transcript(session_name):
    search_dir = os.path.expanduser("~/.gemini/tmp/aim-locomo/chats/*.jsonl")
    files = glob.glob(search_dir)
    if not files: return None
    return sorted(files, key=os.path.getmtime)[-1]

def wait_for_response(transcript_path, question_text):
    print("Waiting for Gemini to finish generating answer...")
    start_time = time.time()
    q_target = question_text[-50:].strip()
    
    last_gemini_content = ""
    last_update_time = time.time()
    raw_context = []
    
    while time.time() - start_time < THINKING_TIMEOUT_SECONDS:
        if os.path.exists(transcript_path):
            with open(transcript_path, "r") as f:
                lines = f.readlines()
                
            messages = []
            for line in lines:
                try:
                    msg = json.loads(line)
                    if msg.get("type") in ("user", "gemini", "tool_call", "tool_response", "tool"):
                        messages.append(msg)
                except:
                    pass
            
            user_msg_idx = -1
            for idx, msg in enumerate(messages):
                if msg.get("type") == "user":
                    content = msg.get("content", [])
                    text = "".join([c.get("text", "") for c in content]) if isinstance(content, list) else str(content)
                    if q_target in text:
                        user_msg_idx = idx
                        
            if user_msg_idx == -1:
                time.sleep(2)
                continue
                
            raw_context = []
            current_content = ""
            for msg in messages[user_msg_idx+1:]:
                if msg.get("type") != "system":
                    raw_context.append(msg)
                    
                if msg.get("type") == "gemini":
                    c = msg.get("content", "").strip()
                    if c:
                        current_content = c
                    
            if current_content and current_content != last_gemini_content:
                last_gemini_content = current_content
                last_update_time = time.time()
                
        if last_gemini_content and (time.time() - last_update_time > 10):
            ans = last_gemini_content
            if "[ANSWER]" in ans.upper():
                idx = ans.upper().find("[ANSWER]")
                extracted = ans[idx + len("[ANSWER]"):].strip()
                if extracted:
                    ans = extracted
            return f"[ANSWER] {ans}", raw_context
            
        time.sleep(2)
        
    return "TIMEOUT_ERROR", raw_context

def send_via_buffer(session_name, text):
    tmp_file = "/tmp/locomo_benchmark_prompt.txt"
    with open(tmp_file, "w") as f:
        f.write(text)
    subprocess.run(["tmux", "load-buffer", tmp_file])
    subprocess.run(["tmux", "paste-buffer", "-t", session_name])
    time.sleep(0.5)
    subprocess.run(["tmux", "send-keys", "-t", session_name, "Enter"])

def run_ghost_operator():
    # 1. Verify tmux session exists
    try:
        output = subprocess.check_output(['tmux', 'ls']).decode()
        if TARGET_TMUX_SESSION not in output:
            print(f"CRITICAL ERROR: Tmux session '{TARGET_TMUX_SESSION}' not found!")
            print("Please manually start the agent first using:")
            print(f"  tmux new-session -s {TARGET_TMUX_SESSION} -c {PROJECT_ROOT} 'aim gemini --yolo -m gemini-3-flash-preview'")
            return
    except subprocess.CalledProcessError:
         print("CRITICAL ERROR: No tmux server running.")
         return

    # 2. Load dataset
    with open(DATASET_FILE, "r") as f:
        data = json.load(f)
        
    all_questions = []
    for sample in data:
        all_questions.extend(sample.get("qa", []))
        
    # 3. Resume Logic
    predictions = []
    start_idx = 0
    if os.path.exists(OUT_FILE):
        try:
            with open(OUT_FILE, "r") as f:
                predictions = json.load(f)
            start_idx = len(predictions)
            print(f"CRASH RECOVERY: Found existing predictions file.")
            print(f"Resuming at Question {start_idx + 1}")
        except:
            print("Failed to load previous predictions. Starting fresh.")
    else:
        print("Starting fresh benchmark run.")
        
    if start_idx >= len(all_questions):
        print("All questions already completed.")
        return

    # Give the user a moment to cancel if they want
    print("Hooking into tmux session in 3 seconds...")
    time.sleep(3)

    # We need to find the transcript file associated with this tmux session.
    # We assume the most recently modified transcript is the correct one.
    transcript_path = get_latest_transcript(TARGET_TMUX_SESSION)
    if not transcript_path:
        print("ERROR: Could not find a transcript file. Did you send a message in the agent yet?")
        return
        
    print(f"Using transcript: {transcript_path}")

    for i in range(start_idx, len(all_questions)):
        qa = all_questions[i]
        q = qa["question"]
        print(f"\n--- QUESTION {i+1} ---")
        
        clean_q = q.replace("[V2_CORRECTION]", "").replace("[LOCOMO-AUDIT]", "").replace("[LOCOMO-ISSUES]", "").replace("[V2_REPLACEMENT]", "").replace("?", ".").replace("$", "").replace("!", "").strip()
        
        prompt = f"MANDATE: You MUST use the run_shell_command tool to execute python3 aim_core/aim_cli.py search before answering. Question: {clean_q}"
        
        max_retries = 3
        for attempt in range(max_retries):
            print(f"Sending: {prompt}")
            send_via_buffer(TARGET_TMUX_SESSION, prompt)
            
            ans, raw_context = wait_for_response(transcript_path, prompt)
            print(f"Answer received: {ans[:50].replace(chr(10), ' ')}...")
            
            if "TIMEOUT_ERROR" in ans:
                print(f"⚠️ Timeout/429 detected. Sending Escape to stop thinking loop.")
                subprocess.run(["tmux", "send-keys", "-t", TARGET_TMUX_SESSION, "Escape"])
                print(f"Cooling down for {COOLDOWN_DELAY_SECONDS} seconds before retry ({attempt+1}/{max_retries})...")
                time.sleep(COOLDOWN_DELAY_SECONDS)
                continue
                
            ans_lower = ans.lower()
            if "startcall:" in ans_lower or "native cli exception" in ans_lower or "ollama error" in ans_lower:
                print(f"⚠️ Tool error detected. Sending Escape to stop loop.")
                subprocess.run(["tmux", "send-keys", "-t", TARGET_TMUX_SESSION, "Escape"])
                print(f"Cooling down for {COOLDOWN_DELAY_SECONDS} seconds before retry ({attempt+1}/{max_retries})...")
                time.sleep(COOLDOWN_DELAY_SECONDS)
                continue
                
            break
            
        pred = qa.copy()
        pred["prediction"] = ans
        pred["raw_rag_context"] = raw_context
        predictions.append(pred)
        
        with open(OUT_FILE, "w") as f:
            json.dump(predictions, f, indent=4)
            
        print(f"Sleeping {PACING_DELAY_SECONDS}s...")
        time.sleep(PACING_DELAY_SECONDS)

if __name__ == "__main__":
    run_ghost_operator()
