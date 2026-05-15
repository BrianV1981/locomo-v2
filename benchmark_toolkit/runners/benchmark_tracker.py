import json
import time
import glob
import os
import threading

def get_latest_transcript():
    search_dir = os.path.expanduser("~/.gemini/tmp/aim-locomo/chats/*.jsonl")
    files = glob.glob(search_dir)
    if not files: return None
    return max(files, key=os.path.getmtime)

def track_quota():
    transcript_path = get_latest_transcript()
    if not transcript_path:
        print("[Tracker] No transcript found. Waiting...")
        return
        
    print(f"[Tracker] Monitoring: {transcript_path}")
    
    total_tokens = 0
    total_input = 0
    total_output = 0
    turns = 0
    last_line_count = 0
    
    while True:
        try:
            with open(transcript_path, "r") as f:
                lines = f.readlines()
                
            if len(lines) > last_line_count:
                new_lines = lines[last_line_count:]
                last_line_count = len(lines)
                
                for line in new_lines:
                    try:
                        msg = json.loads(line)
                        if msg.get("type") == "gemini" and "tokens" in msg:
                            t = msg["tokens"]
                            total_input += t.get("input", 0)
                            total_output += t.get("output", 0)
                            total_tokens += t.get("total", 0)
                            turns += 1
                            
                            # Write to report
                            with open("/home/kingb/aim-locomo/QUOTA_REPORT.md", "w") as rf:
                                rf.write(f"# Benchmark Quota Tracker\n\n")
                                rf.write(f"**Total Turns:** {turns}\n")
                                rf.write(f"**Total Tokens:** {total_tokens:,}\n")
                                rf.write(f"**Input Tokens:** {total_input:,}\n")
                                rf.write(f"**Output Tokens:** {total_output:,}\n\n")
                                rf.write(f"**Average Tokens/Turn:** {total_tokens // turns if turns > 0 else 0:,}\n")
                    except Exception:
                        pass
        except Exception:
            pass
            
        time.sleep(2)

if __name__ == "__main__":
    print("Starting Quota Tracker in background...")
    track_quota()
