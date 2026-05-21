#!/usr/bin/env python3
"""
OpenCode Ghost Operator — Continuation Runner.
Loads an existing partial predictions file, identifies invalid/timeout answers,
re-asks those questions, then continues with remaining questions.
"""
import os, sys, json, time, subprocess, sqlite3
from datetime import datetime

PROJECT_ROOT = "/home/kingb/opencode-locomo"
OPECODE_BIN = "/home/kingb/.opencode/bin/opencode"
MODEL = "deepseek/deepseek-v4-flash"
OPECODE_DB = os.path.expanduser("~/.local/share/opencode/opencode.db")
DATA_FILE = "/home/kingb/locomo-v2/data/locomo_v2_final.json"

# --- DELAY & TIMEOUT LOGIC ---
PACING_DELAY_SECONDS = 30
COOLDOWN_DELAY_SECONDS = 180
THINKING_TIMEOUT_SECONDS = 300
BOOT_DELAY_SECONDS = 15

# ── Session Discovery ───────────────────────────────────────────────

def get_latest_session():
    if not os.path.exists(OPECODE_DB):
        return None, 0
    conn = sqlite3.connect(OPECODE_DB)
    row = conn.execute(
        "SELECT id FROM session ORDER BY time_created DESC LIMIT 1"
    ).fetchone()
    conn.close()
    if row:
        return row[0], get_part_count(row[0])
    return None, 0

def get_part_count(session_id):
    conn = sqlite3.connect(OPECODE_DB)
    count = conn.execute(
        "SELECT COUNT(*) FROM part WHERE session_id = ?", (session_id,)
    ).fetchone()[0]
    conn.close()
    return count

def poll_new_parts(session_id, last_count):
    conn = sqlite3.connect(OPECODE_DB)
    rows = conn.execute(
        "SELECT data FROM part WHERE session_id = ? ORDER BY time_created ASC",
        (session_id,)
    ).fetchall()
    conn.close()
    new_parts = rows[last_count:] if len(rows) > last_count else []
    return new_parts, len(rows)

# ── Answer Detection ─────────────────────────────────────────────────

def find_answer_in_parts(new_parts):
    raw_context = []
    for (part_data,) in new_parts:
        try:
            p = json.loads(part_data)
        except (json.JSONDecodeError, TypeError):
            continue
        raw_context.append(p)
        for field in ('text', 'reason', 'content'):
            content = p.get(field, '')
            if content and isinstance(content, str) and len(content.strip()) > 3:
                raw_context.append({"text": content})

    skipping_keywords = ["let me search", "let me look", "search for", "look for more"]

    for item in raw_context:
        text = item.get("text", "")
        if not text:
            continue
        text_lower = text.lower().strip()
        if any(kw in text_lower[:80] for kw in skipping_keywords) and "[ANSWER]" not in text.upper():
            continue
        if "[ANSWER]" in text.upper():
            idx = text.upper().find("[ANSWER]")
            ans = text[idx + len("[ANSWER]"):].strip()
            if ans and len(ans) >= 2:
                return ans, raw_context

        if "ANSWER " in text.upper() and "[ANSWER]" not in text.upper():
            idx = text.upper().find("ANSWER ")
            ans = text[idx + len("ANSWER "):].strip()
            if ans and len(ans) >= 2:
                return ans, raw_context
        if "i don't know" in text_lower and len(text) < 300:
            return text.strip(), raw_context

    # Fallback: if no [ANSWER] tag found, grab last substantial text block
    # (mirrors Gemini runner: any gemini msg without toolCalls = final answer)
    for item in reversed(raw_context):
        text = item.get("text", "")
        if not text or len(text.strip()) < 5:
            continue
        text_lower = text.lower().strip()
        if any(kw in text_lower[:80] for kw in skipping_keywords):
            continue
        if any(kw in text_lower[:50] for kw in ["tool_call", "tool call", "startcall", "ollama", "search for"]):
            continue
        return f"[ANSWER] {text.strip()}", raw_context

    return None, raw_context

# ── Response Monitor ─────────────────────────────────────────────────

def wait_for_response(session_id, last_part_count):
    print("Waiting for agent to generate answer...")
    start_time = time.time()
    last_activity = start_time
    raw_context_all = []

    while True:
        new_parts, current_count = poll_new_parts(session_id, last_part_count)
        if new_parts:
            last_part_count = current_count
            last_activity = time.time()
            ans, ctx = find_answer_in_parts(new_parts)
            raw_context_all.extend(ctx)
            if ans:
                return ans, raw_context_all, last_part_count

        idle_time = time.time() - last_activity
        if idle_time > 120:
            print(f"Timeout: agent idle for {int(idle_time)}s. Returning sentinel for retry.")
            return "TIMEOUT_NO_ANSWER", raw_context_all, last_part_count

        if time.time() - start_time > THINKING_TIMEOUT_SECONDS:
            print(f"Hard timeout after {THINKING_TIMEOUT_SECONDS}s. Returning sentinel for retry.")
            return "TIMEOUT_NO_ANSWER", raw_context_all, last_part_count

        time.sleep(2)

# ── Buffer Injection ─────────────────────────────────────────────────

def send_via_buffer(session_name, text):
    tmp_file = "/tmp/oc_benchmark_prompt.txt"
    with open(tmp_file, "w") as f:
        f.write(text)
    subprocess.run(["tmux", "load-buffer", tmp_file], check=True)
    subprocess.run(["tmux", "paste-buffer", "-t", session_name], check=True)
    time.sleep(0.5)
    subprocess.run(["tmux", "send-keys", "-t", session_name, "Enter"], check=True)

# ── Load & Identify ──────────────────────────────────────────────────

def load_existing_predictions(filepath):
    with open(filepath) as f:
        return json.load(f)

def find_invalid_questions(predictions):
    """Return list of (0-based index, question_dict) for invalid answers."""
    invalid = []
    for i, p in enumerate(predictions):
        pred = str(p.get('prediction', '')).lower()
        if any(m in pred for m in ['timeout_no_answer', 'startcall:',
                                     'native cli exception', 'ollama error']):
            invalid.append((i, p))
        elif 'let me search' in pred[:60]:
            invalid.append((i, p))
        elif len(p.get('prediction', '').strip()) < 2:
            invalid.append((i, p))
    return invalid

def load_remaining_questions(predictions):
    """Load questions 147-199 from the original data file."""
    with open(DATA_FILE) as f:
        data = json.load(f)

    all_questions = []
    for sample in data:
        if "qa" in sample:
            for qa in sample["qa"]:
                qa["question"] = qa["question"].replace("[V2_CORRECTION] ", "").replace("[LOCOMO-AUDIT] ", "").replace("[LOCOMO-ISSUES] ", "").replace("[V2_REPLACEMENT] ", "")
                all_questions.append(qa)
        elif "question" in sample:
            all_questions.append(sample)

    all_questions = all_questions[:199]
    remaining = all_questions[len(predictions):]
    return remaining

# ── Main ─────────────────────────────────────────────────────────────

def run_continuation(existing_file, output_file=None):
    # Load existing results
    print(f"Loading existing predictions from {existing_file}")
    predictions = load_existing_predictions(existing_file)
    print(f"  Existing predictions: {len(predictions)}")

    # Find invalid answers
    invalid = find_invalid_questions(predictions)
    print(f"  Invalid answers needing retry: {len(invalid)}")
    for idx, p in invalid:
        q = p.get('question', '')[:60]
        pred = str(p.get('prediction', ''))[:60]
        print(f"    Q{idx+1}: {q} -> [{pred}]")

    # Load remaining questions (147-199)
    remaining = load_remaining_questions(predictions)
    print(f"  Remaining questions: {len(remaining)} (Q{len(predictions)+1}-Q199)")

    # Build the work queue: invalid retries first, then remaining
    work_queue = [(idx, p) for idx, p in invalid]  # 0-based index to overwrite
    work_queue += [(len(predictions) + i, q) for i, q in enumerate(remaining)]

    if not work_queue:
        print("Nothing to do — all 199 predictions are valid!")
        return

    print(f"\nTotal questions to ask: {len(work_queue)}")

    # Output file
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        out_dir = "/home/kingb/benchmark_results/reports/locomo_v2/track_b"
        os.makedirs(out_dir, exist_ok=True)
        output_file = os.path.join(out_dir, f"opencode_continuation_{timestamp}.json")
    print(f"Output: {output_file}")

    tmux_session = f"ghost_oc_{int(time.time())}"

    # ── SPAWN ──
    print(f"\nStarting tmux session '{tmux_session}'...")
    subprocess.run([
        "tmux", "new-session", "-d", "-s", tmux_session,
        "-c", PROJECT_ROOT,
        OPECODE_BIN, "-m", MODEL
    ], check=True)
    time.sleep(BOOT_DELAY_SECONDS)

    # ── FIND SESSION ──
    old_session_id, _ = get_latest_session()
    if not old_session_id:
        print("ERROR: Could not find OpenCode session.")
        return

    # ── PRIMER ──
    primer = (
        "MANDATE: You are continuing a benchmark. "
        "Follow your AGENTS.md instructions precisely. "
        "Answer with [ANSWER] followed by a concise answer. "
        "Acknowledge: 'Ready for continuation.'"
    )
    print("Sending primer...")
    send_via_buffer(tmux_session, primer)

    print("Waiting for new session...")
    for _ in range(20):
        time.sleep(2)
        current_sid, _ = get_latest_session()
        if current_sid and current_sid != old_session_id:
            session_id = current_sid
            break
    else:
        session_id = old_session_id

    last_part_count = get_part_count(session_id)
    print("Waiting for primer acknowledgement...")
    start = time.time()
    while time.time() - start < 60:
        new_parts, current_count = poll_new_parts(session_id, last_part_count)
        if new_parts:
            last_part_count = current_count
            for (part_data,) in new_parts:
                try:
                    p = json.loads(part_data)
                except:
                    continue
                for field in ('text', 'reason', 'content'):
                    content = p.get(field, '')
                    if content and isinstance(content, str) and len(content.strip()) > 10:
                        print(f"Primer acknowledged: {str(content)[:80]}")
                        break
                else:
                    continue
                break
            else:
                continue
            break
        time.sleep(2)
    else:
        print("Primer timeout (60s) — proceeding.")

    # ── WORK LOOP ──
    for idx, qa in work_queue:
        q = qa["question"]
        total = len(work_queue)
        current = work_queue.index((idx, qa)) + 1

        # Determine display index
        if idx < len(predictions):
            display = f"RETRY Q{idx+1}/{len(predictions)}"
        else:
            display = f"Q{idx+1}/199"
        print(f"\n[{current}/{total}] {display}: {q[:80]}...")

        max_retries = 3
        ans = ""
        raw_context = []

        for attempt in range(max_retries):
            # Strip taxonomy tags and punctuation to prevent biasing the agent
            clean_q = q.replace("[V2_CORRECTION]", "").replace("[LOCOMO-AUDIT]", "").replace("[LOCOMO-ISSUES]", "").replace("[V2_REPLACEMENT]", "").replace("?", ".").replace("$", "").replace("!", "").strip()
            # Embed search mandate into every question
            clean_q = f"MANDATE: You MUST use the run_shell_command tool to execute python3 aim_core/aim_cli.py search before answering. Question: {clean_q}"
            send_via_buffer(tmux_session, clean_q)
            ans, raw_context, last_part_count = wait_for_response(
                session_id, last_part_count
            )
            ans_str = str(ans)[:100].replace("\n", " ")
            print(f"  Answer: {ans_str}...")

            ans_lower = str(ans).lower()
            ctx_str = str(raw_context).lower()
            if any(err in ans_lower or err in ctx_str for err in [
                "startcall:", "native cli exception", "ollama error",
                "traceback", "error:", "timeout_no_answer"
            ]):
                print(f"  Error/timeout. Sending Escape. Retry {attempt+1}/{max_retries}...")
                subprocess.run(["tmux", "send-keys", "-t", tmux_session, "Escape"])
                print(f"  Cooling down for {COOLDOWN_DELAY_SECONDS} seconds before retry...")
                time.sleep(COOLDOWN_DELAY_SECONDS)
                q = f"Retry: {qa['question']}"
                continue
            if "semantic engine offline" in ctx_str or "ollama embedding error" in ctx_str:
                print(f"  Ollama search degraded. Retry {attempt+1}/{max_retries}...")
                subprocess.run(["tmux", "send-keys", "-t", tmux_session, "Escape"])
                print(f"  Cooling down for {COOLDOWN_DELAY_SECONDS} seconds before retry...")
                time.sleep(COOLDOWN_DELAY_SECONDS)
                q = f"Retry: {qa['question']}"
                continue
            else:
                break

        # Update or append prediction
        if idx < len(predictions):
            predictions[idx]["prediction"] = ans
            predictions[idx]["raw_rag_context"] = raw_context
        else:
            pred = qa.copy()
            pred["prediction"] = ans
            pred["raw_rag_context"] = raw_context
            predictions.append(pred)

        with open(output_file, "w") as f:
            json.dump(predictions, f, indent=2)

        # Drain SQLite pipe: advance past all pending parts so stale
        # retry answers don't bleed into the next question's polling window
        new_parts, last_part_count = poll_new_parts(session_id, last_part_count)
        if new_parts:
            print(f"  Drained {len(new_parts)} stale parts before next question.")

        print(f"  Pacing: Sleeping for {PACING_DELAY_SECONDS} seconds before next question...")
        time.sleep(PACING_DELAY_SECONDS)

    print(f"\nAll done! {len(predictions)} predictions saved to {output_file}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("existing_file", help="Path to existing predictions JSON")
    parser.add_argument("--output", "-o", help="Output file path", default=None)
    args = parser.parse_args()
    run_continuation(args.existing_file, args.output)
