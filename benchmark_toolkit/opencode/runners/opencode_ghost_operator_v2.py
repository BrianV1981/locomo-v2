#!/usr/bin/env python3
"""
OpenCode Ghost Operator — Track B benchmark for opencode-locomo (DeepSeek v4 Flash).

Mirrors the Gemini locomo_ghost_operator_v2.py pattern exactly, but polls the
OpenCode SQLite database (~/.local/share/opencode/opencode.db) for structured
session data instead of parsing Gemini CLI JSONL transcripts.

Protocol:
  1. Spawn OpenCode TUI in detached tmux
  2. Find the session ID from opencode.db
  3. Poll part table for [ANSWER] in text parts (same as Gemini JSONL polling)
  4. Retry on errors, timeout after 120s
  5. Save predictions incrementally
"""
import os, sys, json, time, subprocess, sqlite3
from datetime import datetime

PROJECT_ROOT = "/home/kingb/opencode-locomo"
OPECODE_BIN = "/home/kingb/.opencode/bin/opencode"
MODEL = "deepseek/deepseek-v4-flash"
OPECODE_DB = os.path.expanduser("~/.local/share/opencode/opencode.db")
DATA_FILE = "/home/kingb/locomo-v2/data/locomo_v2_minicpm.json"

# --- QUESTION BATCHING ---
START_QUESTION_INDEX = 0
END_QUESTION_INDEX = 50

# --- DELAY & TIMEOUT LOGIC ---
PACING_DELAY_SECONDS = 30
COOLDOWN_DELAY_SECONDS = 180
THINKING_TIMEOUT_SECONDS = 300
BOOT_DELAY_SECONDS = 15

# ── Session Discovery ───────────────────────────────────────────────

def get_latest_session():
    """Find the most recent OpenCode session ID from the SQLite database."""
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
    """Count existing parts for a session (baseline for polling)."""
    conn = sqlite3.connect(OPECODE_DB)
    count = conn.execute(
        "SELECT COUNT(*) FROM part WHERE session_id = ?", (session_id,)
    ).fetchone()[0]
    conn.close()
    return count

def poll_new_parts(session_id, last_count):
    """Poll the part table for new text parts. Returns (new_parts, new_count)."""
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
    """
    Scan new parts for [ANSWER] tags. Only inspects content-bearing parts
    (type=text, type=reasoning). Ignores structural parts (step-start,
    step-finish, patch, tool) whose metadata fields (e.g. 'reason') are
    NOT agent answers.
    Returns (answer_text, raw_context) if found, else (None, raw_context).
    """
    CONTENT_TYPES = {"text", "reasoning"}
    STRUCTURAL_TYPES = {"step-start", "step-finish", "patch", "tool"}

    raw_context = []
    for (part_data,) in new_parts:
        try:
            p = json.loads(part_data)
        except (json.JSONDecodeError, TypeError):
            continue

        ptype = p.get("type", "")
        raw_context.append(p)

        # Only extract text from content-bearing parts, not structural metadata
        if ptype in STRUCTURAL_TYPES:
            continue

        for field in ('text', 'reason', 'content'):
            content = p.get(field, '')
            if content and isinstance(content, str) and len(content.strip()) > 3:
                # For non-content types, only take 'text' field (skip 'reason' metadata)
                if ptype not in CONTENT_TYPES and field != 'text':
                    continue
                raw_context.append({"type": ptype, "text": content})

    for item in raw_context:
        text = item.get("text", "")
        if not text:
            continue

        text_lower = text.lower().strip()

        # Skip user-injected search mandate text (defense-in-depth against race)
        if "mandate: you must use the run_shell_command tool" in text_lower[:120]:
            continue

        if any(kw in text_lower[:180] for kw in SKIPPING_KEYWORDS) and "[ANSWER]" not in text.upper():
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

    # No eager fallback — return None so wait_for_response keeps polling
    # for a tagged answer. The fallback only triggers in wait_for_response
    # after the agent has gone idle (stopped producing new parts).
    return None, raw_context

# ── Idle Fallback ────────────────────────────────────────────────────

SKIPPING_KEYWORDS = ["let me search", "let me look", "search for", "look for more"]

def fallback_on_raw_context(raw_context_all):
    """
    If agent has stopped producing parts, grab the last substantial text
    block as a fallback answer. Only called when agent is idle, so this
    won't preempt a tagged answer arriving in a later batch.
    """
    for item in reversed(raw_context_all):
        text = item.get("text", "")
        if not text or len(text.strip()) < 5:
            continue
        text_lower = text.lower().strip()
        if "mandate: you must use the run_shell_command tool" in text_lower[:120]:
            continue
        if any(kw in text_lower[:180] for kw in SKIPPING_KEYWORDS):
            continue
        if any(kw in text_lower[:180] for kw in ["tool_call", "tool call", "startcall", "ollama", "search for"]):
            continue
        return f"[ANSWER] {text.strip()}"
    return None

# ── Response Monitor (mirrors Gemini wait_for_response) ──────────────

def wait_for_response(session_id, last_part_count):
    """
    Poll the OpenCode SQLite DB for new text parts with [ANSWER].
    Returns (answer, raw_context, new_part_count).
    Waits for tagged answer; uses idle fallback only after agent pauses.
    """
    print("Waiting for agent to generate answer...")
    start_time = time.time()
    last_activity = start_time
    raw_context_all = []

    while True:
        new_parts, current_count = poll_new_parts(session_id, last_part_count)

        if new_parts:
            last_part_count = current_count
            last_activity = time.time()  # agent is alive
            ans, ctx = find_answer_in_parts(new_parts)
            raw_context_all.extend(ctx)

            if ans:
                return ans, raw_context_all, last_part_count

        # Agent idle for 20s → try fallback on accumulated context.
        # This waits for a tagged answer before grabbing untagged text.
        idle_time = time.time() - last_activity
        if idle_time > 20:
            fb_ans = fallback_on_raw_context(raw_context_all)
            if fb_ans:
                print(f"  No tagged answer after {int(idle_time)}s idle — using fallback.")
                return fb_ans, raw_context_all, last_part_count

        # Dynamic timeout: only fail if agent has been idle for 120s
        # (no new parts written), regardless of total elapsed time.
        idle_time = time.time() - last_activity
        if idle_time > 120:
            print(f"Timeout: agent idle for {int(idle_time)}s. Returning sentinel for retry.")
            return "TIMEOUT_NO_ANSWER", raw_context_all, last_part_count

        # Safety net: hard cap at 300s (5 min) — matches Gemini runner
        if time.time() - start_time > THINKING_TIMEOUT_SECONDS:
            print(f"Hard timeout after {THINKING_TIMEOUT_SECONDS}s. Returning sentinel for retry.")
            return "TIMEOUT_NO_ANSWER", raw_context_all, last_part_count

        time.sleep(2)

# ── Buffer Injection ─────────────────────────────────────────────────

def send_via_buffer(session_name, text):
    """Inject a message into a tmux session via buffer paste (avoids escaping)."""
    tmp_file = "/tmp/oc_benchmark_prompt.txt"
    with open(tmp_file, "w") as f:
        f.write(text)
    subprocess.run(["tmux", "load-buffer", tmp_file], check=True)
    subprocess.run(["tmux", "paste-buffer", "-t", session_name], check=True)
    time.sleep(0.5)
    subprocess.run(["tmux", "send-keys", "-t", session_name, "Enter"], check=True)

# ── Main Ghost Operator ──────────────────────────────────────────────

def run_ghost_operator():
    # Load questions
    with open(DATA_FILE) as f:
        data = json.load(f)

    questions = []
    for sample in data:
        if "qa" in sample:
            for qa in sample["qa"]:
                qa["question"] = qa["question"].replace("[V2_CORRECTION] ", "").replace("[LOCOMO-AUDIT] ", "").replace("[LOCOMO-ISSUES] ", "").replace("[V2_REPLACEMENT] ", "")
                questions.append(qa)
        elif "question" in sample:
            questions.append(sample)

    questions = questions[START_QUESTION_INDEX:END_QUESTION_INDEX]
    print(f"Loaded {len(questions)} questions (Indices {START_QUESTION_INDEX} to {END_QUESTION_INDEX}).")
    
    # Allow limiting questions via CLI arg for smoke testing
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])
        questions = questions[:limit]
        print(f"SMOKE TEST: limited to {limit} questions")

    # Output file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    out_dir = "/home/kingb/opencode-benchmarks/reports/locomo_v2/track_b"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, f"opencode_trackB_{timestamp}.json")

    tmux_session = f"ghost_oc_{int(time.time())}"
    predictions = []

    # ── SPAWN ──
    print(f"Starting tmux session '{tmux_session}'...")
    subprocess.run([
        "tmux", "new-session", "-d", "-s", tmux_session,
        "-c", PROJECT_ROOT,
        OPECODE_BIN, "-m", MODEL
    ], check=True)
    time.sleep(BOOT_DELAY_SECONDS)

    # ── FIND SESSION ──
    old_session_id, _ = get_latest_session()
    if not old_session_id:
        print("ERROR: Could not find OpenCode session in database.")
        return

    # ── PRIMER ──
    primer = (
        "MANDATE: You are about to receive 199 benchmark questions. "
        "Follow your AGENTS.md instructions precisely. "
        "Answer with [ANSWER] followed by a concise answer. "
        "Acknowledge: 'Primer acknowledged.'"
    )
    print("Sending primer...")
    send_via_buffer(tmux_session, primer)

    # Wait for new session to appear (primer response may create new session)
    print("Waiting for agent to process primer...")
    for _ in range(20):
        time.sleep(2)
        current_sid, _ = get_latest_session()
        if current_sid and current_sid != old_session_id:
            session_id = current_sid
            break
    else:
        session_id = old_session_id

    # Consume primer response — accept ANY text, not just [ANSWER]
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

    # ── QUESTION LOOP ──
    for i, qa in enumerate(questions):
        q = qa["question"]
        print(f"\n[{i+1}/{len(questions)}] {q[:80]}...")

        max_retries = 3
        ans = ""
        raw_context = []

        for attempt in range(max_retries):
            # Strip taxonomy tags and punctuation to prevent biasing the agent
            clean_q = q.replace("[V2_CORRECTION]", "").replace("[LOCOMO-AUDIT]", "").replace("[LOCOMO-ISSUES]", "").replace("[V2_REPLACEMENT]", "").replace("?", ".").replace("$", "").replace("!", "").strip()
            # Embed search mandate into every question
            clean_q = f"MANDATE: You MUST use the run_shell_command tool to execute python3 aim_core/aim_cli.py search before answering. Question: {clean_q}"
            send_via_buffer(tmux_session, clean_q)
            # Skip past the user message part(s) just written by the paste.
            # Only advance past mandate lines, NOT past agent response parts.
            time.sleep(0.2)
            new_parts, new_count = poll_new_parts(session_id, last_part_count)
            user_msg_parts = 0
            for (part_data,) in new_parts:
                if 'mandate: you must use' in str(part_data).lower():
                    user_msg_parts += 1
            last_part_count += user_msg_parts
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
            # Detect degraded search: Ollama embedding failure in context
            if "semantic engine offline" in ctx_str or "ollama embedding error" in ctx_str:
                print(f"  Ollama search degraded. Retry {attempt+1}/{max_retries}...")
                subprocess.run(["tmux", "send-keys", "-t", tmux_session, "Escape"])
                print(f"  Cooling down for {COOLDOWN_DELAY_SECONDS} seconds before retry...")
                time.sleep(COOLDOWN_DELAY_SECONDS)
                q = f"Retry: {qa['question']}"
                continue
            else:
                break

        pred = qa.copy()
        pred["prediction"] = ans
        pred["raw_rag_context"] = raw_context
        predictions.append(pred)

        with open(out_file, "w") as f:
            json.dump(predictions, f, indent=2)

        print(f"  Pacing: Sleeping for {PACING_DELAY_SECONDS} seconds before next question...")
        time.sleep(PACING_DELAY_SECONDS)

        # Drain SQLite pipe AFTER pacing sleep: consume any late-arriving
        # answers from the previous question so they don't bleed into the
        # next question's polling window as a false answer.
        new_parts, last_part_count = poll_new_parts(session_id, last_part_count)
        if new_parts:
            print(f"  Drained {len(new_parts)} stale parts after pacing.")

    print(f"\nAll {len(predictions)} predictions saved to {out_file}")


if __name__ == "__main__":
    run_ghost_operator()
