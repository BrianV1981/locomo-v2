#!/usr/bin/env python3
"""
Build LongMemEval LanceDB with speaker-boundary chunking (500-1500 chars) for RAG 5.2.
"""
import sys, os, json, re
from pathlib import Path

# Add A.I.M. memeval root to path
AIM_MEMEVAL_ROOT = "/home/kingb/aim-memeval"
sys.path.insert(0, AIM_MEMEVAL_ROOT)
sys.path.insert(0, os.path.join(AIM_MEMEVAL_ROOT, "aim_core"))

from aim_core.lance_backend import VectorBackend
from aim_core.plugins.datajack.forensic_utils import get_embedding

MD_DIR = Path(__file__).parent / "data" / "flight_recorders"
TARGET_LANCE = "/home/kingb/locomo-v2/benchmark_toolkit/database/longmemeval_lance_rag5.2/memory_lance"

backend = VectorBackend(path=TARGET_LANCE)
table = backend.get_table()

CHUNK_MIN = 500
CHUNK_MAX = 1500

completed_sessions = set()
rid = 0

# Check for existing table to enable resuming
if os.path.exists(TARGET_LANCE):
    try:
        import lancedb
        db = lancedb.connect(TARGET_LANCE)
        # Check if fragments table exists
        if "fragments" in db.table_names():
            df = table.to_pandas()
            if 'session_id' in df.columns:
                completed_sessions = set(df['session_id'].unique())
            if 'fragment_id' in df.columns and not df.empty:
                rid = int(df['fragment_id'].max()) + 1
            print(f"Resuming... found {len(completed_sessions)} completed sessions. Starting at fragment_id {rid}")
        else:
            print("No 'fragments' table found, but database directory exists. Starting fresh.")
    except Exception as e:
        print(f"Database access error, assuming fresh start: {e}")

all_files = list(MD_DIR.glob("*.md"))
print(f"Found {len(all_files)} total flight recorders.")

total_indexed = 0

for md_file in all_files:
    session_id = md_file.stem
    if session_id in completed_sessions:
        print(f"Skipping {session_id}, already embedded.")
        continue

    content = md_file.read_text(encoding="utf-8").strip()
    
    # Split by the specific LongMemEval format timestamp boundaries
    turns = re.split(r'\n(?=\[\d{4}/\d{2}/\d{2} )', '\n' + content)
    turns = [t.strip() for t in turns if t.strip()]

    records = []
    current_chunk = []
    current_len = 0

    for turn in turns:
        turn_len = len(turn)

        if current_len + turn_len > CHUNK_MAX and current_len >= CHUNK_MIN:
            chunk_content = "\n\n".join(current_chunk)
            try:
                vec = get_embedding(chunk_content[:8000], task_type='RETRIEVAL_DOCUMENT')
                if vec:
                    records.append({
                        "fragment_id": rid, "session_id": session_id,
                        "type": "longmemeval_session", "content": chunk_content[:16000],
                        "timestamp": "", "metadata": json.dumps({"dataset": "longmemeval"}),
                        "parent_id": 0, "source_db": "longmemeval_v1.1",
                        "vector": vec
                    })
                    rid += 1
            except Exception as e:
                print(f"Embedding error: {e}")
            current_chunk = []
            current_len = 0

        current_chunk.append(turn)
        current_len += turn_len

    if current_chunk:
        chunk_content = "\n\n".join(current_chunk)
        try:
            vec = get_embedding(chunk_content[:8000], task_type='RETRIEVAL_DOCUMENT')
            if vec:
                records.append({
                    "fragment_id": rid, "session_id": session_id,
                    "type": "longmemeval_session", "content": chunk_content[:16000],
                    "timestamp": "", "metadata": json.dumps({"dataset": "longmemeval"}),
                    "parent_id": 0, "source_db": "longmemeval_v1.1",
                    "vector": vec
                })
                rid += 1
        except Exception as e:
            print(f"Embedding error: {e}")

    print(f"  {session_id} → {len(records)} chunks")

    if records:
        table.add(records)
        total_indexed += len(records)

if total_indexed > 0 or rid > 0:
    try:
        table.create_fts_index("content", replace=True)
        print("  FTS index built/updated.")
    except Exception as e:
        print(f"  FTS index warning (non-fatal): {e}")

print(f"\nLanceDB sync complete. Target: {TARGET_LANCE}")
