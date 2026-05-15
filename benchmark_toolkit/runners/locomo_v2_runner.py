import os
import json
import time
import subprocess
import glob
from datetime import datetime

PROJECT_ROOT = "/home/kingb/aim-locomo"
DATA_FILE = "/home/kingb/locomo-v2/data/locomo_v2_qwen.json"

# --- QUESTION BATCHING ---
# The array slice of questions to run. 0 to 50 = Questions 1 through 50.
START_QUESTION_INDEX = 0
END_QUESTION_INDEX = 199

# --- DELAY & TIMEOUT LOGIC ---
# Pacing: Seconds to wait AFTER a successful answer before sending the next question.
PACING_DELAY_SECONDS = 60

# Cooldown: Seconds to wait AFTER hitting a timeout/429 error before retrying.
COOLDOWN_DELAY_SECONDS = 180

# Timeout: Maximum seconds to wait for the agent to finish "Thinking" before assuming a freeze.
THINKING_TIMEOUT_SECONDS = 300

# Boot Delay: Seconds to wait after spawning tmux to allow the Gemini CLI to authenticate.
BOOT_DELAY_SECONDS = 15


if not os.path.exists(DATA_FILE):
    DATA_FILE = "/home/kingb/gemini-benchmarks/data/locomo_v2/locomo_track1_qwen_q1_to_50.json"

def get_latest_transcript():
    # Gemini CLI saves transcripts for aim-locomo here
    search_dir = os.path.expanduser("~/.gemini/tmp/aim-locomo/chats/*.jsonl")
    files = glob.glob(search_dir)
    if not files: return None
    return max(files, key=os.path.getmtime)

def wait_for_response(transcript_path, question_text):
    print("Waiting for Gemini to finish generating answer...")
    start_time = time.time()
    q_target = question_text.strip()
    
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
                    if isinstance(content, list):
                        text = "".join([c.get("text", "") for c in content])
                    else:
                        text = str(content)
                    
                    if q_target in text:
                        user_msg_idx = idx
                        
            if user_msg_idx == -1:
                time.sleep(2)
                continue
                
            raw_context = []
            for msg in messages[user_msg_idx+1:]:
                if msg.get("type") == "gemini":
                    if not msg.get("toolCalls"):
                        content = msg.get("content", "").strip()
                        if "[ANSWER]" in content.upper():
                            idx = content.upper().find("[ANSWER]")
                            ans = content[idx + len("[ANSWER]"):].strip()
                            if not ans:
                                ans = content
                            return f"[ANSWER] {ans}", raw_context
                        else:
                            # If it forgot the tag, just return the raw text it provided
                            return f"[ANSWER] {content}", raw_context
                        
                elif msg.get("type") not in ("user", "system"):
                    raw_context.append(msg)
                    
        time.sleep(2)
        
    return "TIMEOUT_ERROR", []

def send_via_buffer(session_name, text):
    # Avoid escaping issues by using a temp file and load-buffer instead of set-buffer
    tmp_file = "/tmp/locomo_benchmark_prompt.txt"
    with open(tmp_file, "w") as f:
        f.write(text)
    
    subprocess.run(["tmux", "load-buffer", tmp_file])
    subprocess.run(["tmux", "paste-buffer", "-t", session_name])
    time.sleep(0.5)
    subprocess.run(["tmux", "send-keys", "-t", session_name, "Enter"])

def run_ghost_operator():
    print(f"Loading data from {DATA_FILE}")
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
        
    questions = []
    for sample in data:
        if "qa" in sample:
            for qa in sample["qa"]:
                questions.append(qa)
        elif "question" in sample:
            questions.append(sample)
                
    if not questions:
        print("No questions found.")
        return
        
    # The benchmark uses the first 199 questions for Track A
    questions = questions[START_QUESTION_INDEX:END_QUESTION_INDEX]
    print(f"Loaded total questions. Sliced to {len(questions)} (Indices {START_QUESTION_INDEX} to {END_QUESTION_INDEX}).")
    
    # Save to the benchmark_results folder with a timestamp to avoid overwriting RAG 5 / RAG 10 data
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    out_dir = "/home/kingb/gemini-benchmarks/reports/locomo_v2/track_a"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, f"trackA_predictions_{timestamp}.json")
    
    predictions = []
    chunks = [200]
    idx = 0
    tmux_session = f"ghost_aim_{int(time.time())}"
    
    print(f"Starting new tmux session '{tmux_session}'...")
    subprocess.run(["tmux", "kill-session", "-t", tmux_session], stderr=subprocess.DEVNULL)
    # Spin up a new detached tmux session, cd to aim-locomo, launch gemini --yolo
    subprocess.run(["tmux", "new-session", "-d", "-s", tmux_session, "-c", PROJECT_ROOT, "gemini", "--yolo", "-m", "gemini-3-flash-preview"])
    time.sleep(5)

    # --- PRIMER LOGIC ---
    old_transcript = get_latest_transcript()
    primer_msg = "MANDATE: You are about to be given a series of 105 questions. This is a strict benchmark testing your RAG v5.2 memory system. Before we begin, you MUST use your tools to read the AGENTS.md file in your root directory. Follow your AGENTS.md instructions precisely. Do not guess. Answer directly and concisely. Once you have read AGENTS.md and are ready, reply with '[ANSWER] YES'."
    print("Sending benchmark primer to agent...")
    send_via_buffer(tmux_session, primer_msg)

    print("Waiting for new Gemini transcript to be created by primer...")
    transcript_path = old_transcript
    for _ in range(20):
        time.sleep(2)
        current = get_latest_transcript()
        if current and current != old_transcript:
            transcript_path = current
            break
    if not transcript_path or transcript_path == old_transcript:
        print("Could not find new Gemini transcript for primer. Proceeding with the latest found.")

    # Wait for the primer response so it doesn't pollute the first question
    ans, _ = wait_for_response(transcript_path, "MANDATE:")
    print(f"Primer acknowledged: {ans[:50]}")
    # ---------------------

    for chunk_size in chunks:
        chunk_questions = questions[idx:idx+chunk_size]
        if not chunk_questions: break

        print(f"\\n--- STARTING BATCH OF {len(chunk_questions)} ---")

        for i, qa in enumerate(chunk_questions):
            q = qa["question"]
            print(f"Sending: {q}")

            old_transcript = transcript_path
            
            max_retries = 3
            ans = ""
            raw_context = []
            
            for attempt in range(max_retries):
                # Simulate human typing via tmux buffer
                # Hide taxonomy tags from the agent to prevent prompting bias, keeping it a blind test
                clean_q = q.replace("[V2_CORRECTION]", "").replace("[LOCOMO-AUDIT]", "").replace("[LOCOMO-ISSUES]", "").replace("[V2_REPLACEMENT]", "").replace("?", ".").replace("$", "").replace("!", "").strip()
                clean_q = f"MANDATE: You MUST use the run_shell_command tool to execute python3 aim_core/aim_cli.py search before answering. Question: {clean_q}"
                send_via_buffer(tmux_session, clean_q)
                
                ans, raw_context = wait_for_response(transcript_path, clean_q)
                print(f"Answer received: {ans[:50].replace(chr(10), ' ')}...")
                
                if "TIMEOUT_ERROR" in ans:
                    print(f"⚠️ Timeout detected. Sending Escape to stop thinking loop. Retrying ({attempt+1}/{max_retries})...")
                    subprocess.run(["tmux", "send-keys", "-t", tmux_session, "Escape"])
                    print(f"Cooling down for {COOLDOWN_DELAY_SECONDS} seconds before retry...")
                    time.sleep(COOLDOWN_DELAY_SECONDS)
                    continue
                    
                ans_lower = ans.lower()
                if "startcall:" in ans_lower or "native cli exception" in ans_lower or "ollama error" in ans_lower:
                    print(f"⚠️ Detected tool leak or error. Retrying ({attempt+1}/{max_retries})...")
                    print(f"Cooling down for {COOLDOWN_DELAY_SECONDS} seconds before retry...")
                    time.sleep(COOLDOWN_DELAY_SECONDS) # Pacing before retry
                    q = "You experienced a tool error or leaked raw JSON. Please use the aim-locomo search tool correctly and answer the question: " + qa["question"]
                    continue
                else:
                    break # Valid answer received
            
            pred = qa.copy()
            pred["prediction"] = ans
            pred["raw_rag_context"] = raw_context # Inject the raw tool calls and context into the output!
            predictions.append(pred)
            
            with open(out_file, "w") as f:
                json.dump(predictions, f, indent=4)
                
            print(f"Pacing: Sleeping for {PACING_DELAY_SECONDS} seconds before next question...")
            time.sleep(PACING_DELAY_SECONDS)
            
        idx += chunk_size
        print(f"Batch complete. Handled {chunk_size} questions.")
                
    print(f"All chunks completed. Results saved to {out_file}. Leaving tmux session open for manual review.")

if __name__ == "__main__":
    run_ghost_operator()
