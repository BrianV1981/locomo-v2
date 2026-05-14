#!/usr/bin/env python3
"""
Extract full context for all 82 replacement question slots.

For each slot, pull:
  - The replacement image URL (from manifest)
  - 4 model descriptions (from caches)
  - The conversation turn where the image was placed
  - 3 turns before and 3 turns after that image
  - Speaker names and conversation topic

Output: regeneration_context.json — ready for an agent to generate new questions.
"""
import json
import hashlib
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_PATH = os.path.join(BASE, "data", "locomo_v2_web.json")
MANIFEST_PATH = os.path.join(BASE, "data", "replacement_manifest.json")
CACHE_DIR = os.path.join(BASE, "..", "locomo-visual-ground-truth", "caches")
OUT_PATH = os.path.join(BASE, "data", "regeneration_context.json")

CACHE_FILES = {
    "llava_7b": "llava_7b_cache.json",
    "minicpm": "minicpm_cache.json",
    "moondream": "moondream_cache.json",
    "qwen25vl": "qwen25vl_3b_cache.json",
}


def load_caches():
    caches = {}
    for name, fname in CACHE_FILES.items():
        with open(os.path.join(CACHE_DIR, fname)) as f:
            caches[name] = json.load(f)
    return caches


def find_image_turn(conv, img_url):
    """Find which conversation turn contains a given img_url."""
    for skey, session in conv.get("conversation", {}).items():
        if not isinstance(session, list):
            continue
        for i, turn in enumerate(session):
            urls = turn.get("img_url", [])
            if urls and img_url in urls[0]:
                return skey, i, session
    return None, None, None


def extract_context(session, turn_idx, window=3):
    """Get N turns before and after a given turn index."""
    before = []
    after = []
    for i in range(max(0, turn_idx - window), turn_idx):
        before.append(session[i])
    for i in range(turn_idx + 1, min(len(session), turn_idx + window + 1)):
        after.append(session[i])
    return before, after


def main():
    with open(WEB_PATH) as f:
        web = json.load(f)
    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)

    caches = load_caches()

    # Group manifest by conversation
    manifest_by_conv = {}
    for entry in manifest:
        cid = entry["original_dialogue_id"]
        manifest_by_conv.setdefault(cid, []).append(entry)

    # Also load base dataset for original evidence chains
    BASE_PATH = os.path.join(BASE, "data", "locomo_v2_base.json")
    with open(BASE_PATH) as f:
        base = json.load(f)

    results = []

    for conv in web:
        cid = conv["sample_id"]
        entries = manifest_by_conv.get(cid, [])
        if not entries:
            continue

        sp_a = conv["conversation"].get("speaker_a", "")
        sp_b = conv["conversation"].get("speaker_b", "")

        # Get base conversation (same CID, has original questions with evidence)
        base_conv = next((c for c in base if c["sample_id"] == cid), None)

        # Get replacement questions for this conversation
        repl_qs = [qa for qa in conv.get("qa", []) if "[V2_REPLACEMENT]" in qa["question"]]

        for i, (entry, qa) in enumerate(zip(entries, repl_qs)):
            img_url = entry["new_image_url"]
            original_q = entry["original_question"]
            current_q = qa["question"].replace("[V2_REPLACEMENT]", "").strip()
            current_a = qa.get("answer", "")

            # Find the original question's evidence chain from base dataset
            original_evidence = entry.get("old_evidence", [])
            original_answer = ""
            if base_conv:
                for base_qa in base_conv.get("qa", []):
                    if base_qa["question"].replace("[V2_CORRECTION]", "").strip() == original_q:
                        original_evidence = base_qa.get("evidence", [])
                        original_answer = base_qa.get("answer", "")
                        break

            # Use the FIRST evidence citation to locate the conversation turn
            before, after = [], []
            image_turn = None
            session_key = None
            found_turn_idx = None

            if original_evidence:
                first_ev = original_evidence[0]
                parts = first_ev.split(":")
                if len(parts) == 2:
                    d_num = parts[0].replace("D", "")
                    s_key = f"session_{d_num}"
                    t_idx = int(parts[1]) - 1
                    session = conv["conversation"].get(s_key)
                    if session and isinstance(session, list) and t_idx < len(session):
                        before, after = extract_context(session, t_idx)
                        image_turn = session[t_idx]
                        session_key = s_key
                        found_turn_idx = t_idx

            # Get model descriptions for the NEW image
            descriptions = {}
            for model_name, cache in caches.items():
                desc = cache.get(img_url, "")
                descriptions[model_name] = desc if desc else "(NO DESCRIPTION)"

            results.append({
                "dialogue_id": cid,
                "slot_index": i,
                "speaker_a": sp_a,
                "speaker_b": sp_b,
                "image_url": img_url,
                "image_turn": {
                    "session": session_key,
                    "turn_index": found_turn_idx,
                    "speaker": image_turn.get("speaker", "") if image_turn else "",
                    "text": image_turn.get("text", "") if image_turn else "",
                } if image_turn else None,
                "context_before": [
                    {"speaker": t.get("speaker", ""), "text": t.get("text", "")}
                    for t in before
                ],
                "context_after": [
                    {"speaker": t.get("speaker", ""), "text": t.get("text", "")}
                    for t in after
                ],
                "model_descriptions": descriptions,
                "original_dropped_question": original_q,
                "original_dropped_answer": original_answer,
                "original_evidence_chain": original_evidence,
                "current_replacement_question": current_q,
                "current_replacement_answer": current_a,
            })

    with open(OUT_PATH, "w") as f:
        json.dump(results, f, indent=2)

    # Stats
    with_image = sum(1 for r in results if r["image_turn"])
    with_context = sum(1 for r in results if r["context_before"] or r["context_after"])
    print(f"Slots extracted:  {len(results)}")
    print(f"Image found:      {with_image}")
    print(f"Context found:    {with_context}")
    print(f"Saved:            {OUT_PATH}")


if __name__ == "__main__":
    main()
