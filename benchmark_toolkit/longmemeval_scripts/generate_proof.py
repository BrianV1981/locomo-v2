#!/usr/bin/env python3
"""
A.I.M. LongMemEval Benchmark - Proof Generator
Re-runs the benchmark and saves a transparent JSON log of all retrievals.
"""

import json
import time
import os
import sys
from pathlib import Path

# Add A.I.M. root to path
sys.path.insert(0, "/home/kingb/aim")
sys.path.insert(0, "/home/kingb/aim/aim_core")

from aim_core.lance_backend import VectorBackend
from aim_core.plugins.datajack.forensic_utils import get_embedding

DATA_DIR = Path("/home/kingb/aim-memeval/benchmarks/longmemeval/data")
TEST_FILE  = DATA_DIR / "longmemeval_s_cleaned.json"

def load_data():
    return json.loads(TEST_FILE.read_text())

def main():
    db_path = "/home/kingb/locomo-v2/benchmark_toolkit/database/longmemeval_lance_rag5.2/memory_lance"
    questions = load_data()
    backend = VectorBackend(path=db_path)

    total = len(questions)
    proof_log = []

    print("Generating transparent proof artifact for all 500 questions...")
    
    for i, item in enumerate(questions):
        time.sleep(2.0)
        haystack = set(item["haystack_session_ids"])
        query = item["question"]
        
        correct_ids = item.get("answer_session_ids", [])
        if not correct_ids and "ground_truth_session_id" in item:
            correct_ids = [item["ground_truth_session_id"]]

        query_vec = None
        for attempt in range(10):
            try:
                query_vec = get_embedding(query, task_type='RETRIEVAL_QUERY')
                if query_vec:
                    break
            except Exception as e:
                print(f"\nOllama Error on Q{i+1} (Attempt {attempt+1}): {e}. Retrying in 5 seconds...")
                time.sleep(5.0)
            
        results = backend.search(query_vec, query, top_k=500) if query_vec else []
        
        merged = {}
        for r in results:
            sid_match = r.get('session_id') or r.get('session_file', '').replace('.json', '')
            if sid_match not in haystack:
                continue
            score = r.get('score', 0)
            if sid_match not in merged or score > merged[sid_match]['score']:
                merged[sid_match] = r
                
        final_results = sorted(merged.values(), key=lambda x: x['score'], reverse=True)
        top10_results = []
        for rank, r in enumerate(final_results[:10]):
            sid = r.get("session_id") or r.get('session_file', '').replace('.json', '')
            top10_results.append({
                "rank": rank + 1,
                "session_id": sid,
                "score": float(r.get('score', 0)),
                "is_correct_target": sid in correct_ids
            })

        top5_ids = [r["session_id"] for r in top10_results[:5]]
        top10_ids = [r["session_id"] for r in top10_results[:10]]

        hit_at_5 = any(cid in top5_ids for cid in correct_ids)
        hit_at_10 = any(cid in top10_ids for cid in correct_ids)

        proof_log.append({
            "question_index": i + 1,
            "question": query,
            "ground_truth_targets": correct_ids,
            "hit_at_5": hit_at_5,
            "hit_at_10": hit_at_10,
            "top_10_retrievals": top10_results
        })
        print(f"Processed {i+1}/{total}...", end="\r")

    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = f"/home/kingb/locomo-v2/benchmark_toolkit/database/longmemeval_lance_rag5.2/A_I_M_LONGMEMEVAL_PROOF_LOG_{timestamp}.json"
    with open(out_file, "w") as f:
        json.dump({
            "benchmark": "LongMemEval (Cleaned S Dataset)",
            "architecture": "A.I.M. RAG 5.21 (Native LanceDB + Tantivy FTS + EntityIntersectionReranker)",
            "embedding_model": "nomic-embed-text (Ollama Local)",
            "total_questions": total,
            "recall_at_5_percentage": sum(1 for p in proof_log if p["hit_at_5"]) / total * 100,
            "recall_at_10_percentage": sum(1 for p in proof_log if p["hit_at_10"]) / total * 100,
            "detailed_results": proof_log
        }, f, indent=4)

    print(f"\n✅ Proof Artifact successfully saved to: {out_file}")

if __name__ == "__main__":
    main()