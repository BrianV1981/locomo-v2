#!/usr/bin/env python3
"""
Build LoCoMo V2 LanceDB with speaker-boundary chunking (500-1500 chars).
Fixes the coarse 4000-char chunk problem identified in forensic analysis.
"""
import sys, os, json, shutil, re
sys.path.insert(0, "/home/kingb/opencode-locomo")
sys.path.insert(0, "/home/kingb/opencode-locomo/aim_core")
from aim_core.lance_backend import VectorBackend
from aim_core.plugins.datajack.forensic_utils import get_embedding

ORACLE_FILE = "/home/kingb/locomo-v2/data/locomo_v2_minicpm.json"
TARGET_LANCE = "/home/kingb/opencode-locomo/memory_lance"
CAPTION_KEY = "minicpm_caption"  # Change to "llava_caption" or "blip_caption" as needed

with open(ORACLE_FILE) as f:
    conversations = json.load(f)

conv_names = ['conv-26', 'conv-30', 'conv-41', 'conv-42', 'conv-43',
              'conv-44', 'conv-47', 'conv-48', 'conv-49', 'conv-50']

# Wipe old
if os.path.exists(TARGET_LANCE):
    shutil.rmtree(TARGET_LANCE)

backend = VectorBackend(path=TARGET_LANCE)
table = backend.get_table()

records = []
rid = 0
CHUNK_MIN = 500
CHUNK_MAX = 1500

for ci, conv in enumerate(conversations):
    conv_data = conv["conversation"]
    speaker_a = conv_data.get("speaker_a", f"Speaker_A_{ci}")
    speaker_b = conv_data.get("speaker_b", f"Speaker_B_{ci}")

    # Build complete dialog with named characters
    lines = []
    for sk in sorted([k for k in conv_data if k.startswith("session_") and isinstance(conv_data[k], list)]):
        ts = conv_data.get(sk + "_date_time", "")
        for turn in conv_data[sk]:
            if not isinstance(turn, dict):
                continue
            speaker = turn.get("speaker", "Unknown")
            text = turn.get("text", "").strip()
            
            # Dynamically append Multimodal/Image Data
            if CAPTION_KEY in turn:
                text += f"\n[Image Description]: {turn[CAPTION_KEY]}"
            elif "img_url" in turn and isinstance(turn["img_url"], list) and turn["img_url"]:
                text += f"\n[Image Attachment]: {turn["img_url"][0]}"
                
            if text:
                lines.append((speaker, text, ts))

    # Chunk at speaker boundaries, respecting size limits
    current_chunk = []
    current_len = 0

    for speaker, text, ts in lines:
        turn_text = f"[{ts}] **{speaker}**: {text}" if ts else f"**{speaker}**: {text}"
        turn_len = len(turn_text)

        # If adding this turn exceeds max, flush current chunk
        if current_len + turn_len > CHUNK_MAX and current_len >= CHUNK_MIN:
            chunk_content = "\n".join(current_chunk)
            try:
                vec = get_embedding(chunk_content[:8000], task_type='RETRIEVAL_DOCUMENT')
                if vec:
                    records.append({
                        "fragment_id": rid, "session_id": conv_names[ci],
                        "type": "locomo_conversation", "content": chunk_content[:16000],
                        "timestamp": "", "metadata": json.dumps({"conversation": conv_names[ci]}),
                        "parent_id": 0, "source_db": "locomo_v2_fine",
                        "vector": vec
                    })
                    rid += 1
            except:
                pass
            current_chunk = []
            current_len = 0

        current_chunk.append(turn_text)
        current_len += turn_len

    # Flush remaining
    if current_chunk:
        chunk_content = "\n".join(current_chunk)
        try:
            vec = get_embedding(chunk_content[:8000], task_type='RETRIEVAL_DOCUMENT')
            if vec:
                records.append({
                    "fragment_id": rid, "session_id": conv_names[ci],
                    "type": "locomo_conversation", "content": chunk_content[:16000],
                    "timestamp": "", "metadata": json.dumps({"conversation": conv_names[ci]}),
                    "parent_id": 0, "source_db": "locomo_v2_fine",
                    "vector": vec
                })
                rid += 1
        except:
            pass

    print(f"  {conv_names[ci]}: {speaker_a} & {speaker_b} → {rid - (rid - sum(1 for r in records if r['session_id'] == conv_names[ci]))} chunks")

if records:
    table.add(records)
    # Build FTS index (new LanceDB API)
    try:
        table.create_fts_index("content", replace=True)
    except Exception as e:
        print(f"  FTS index warning (non-fatal): {e}")
    print(f"\nBuilt LanceDB: {len(records)} fragments across {len(conversations)} conversations")
    print(f"  Chunk size: {CHUNK_MIN}-{CHUNK_MAX} chars at speaker boundaries")
    print(f"  Target: {TARGET_LANCE}")
else:
    print("ERROR: No fragments indexed")
    sys.exit(1)
