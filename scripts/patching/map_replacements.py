import json
import random
import os

def create_replacement_manifest(dataset, dead_dataset, unused_urls, seed=42):
    random.seed(seed)
    
    # 1. Map every image URL in the dataset to its sample_id
    url_to_sample = {}
    all_urls_by_sample = {}
    
    for row in dataset:
        sid = row.get("sample_id")
        if sid not in all_urls_by_sample:
            all_urls_by_sample[sid] = []
            
        conv = row.get("conversation", {})
        for i in range(1, 100):
            sk = f"session_{i}"
            if sk not in conv: break
            for turn in conv[sk]:
                urls = turn.get("img_url", [])
                if urls and isinstance(urls, list) and urls[0]:
                    url = urls[0]
                    url_to_sample[url] = sid
                    if url not in all_urls_by_sample[sid]:
                        all_urls_by_sample[sid].append(url)

    # 2. Group unused URLs by sample_id
    unused_by_sample = {}
    for url in unused_urls:
        sid = url_to_sample.get(url)
        if sid:
            if sid not in unused_by_sample:
                unused_by_sample[sid] = []
            unused_by_sample[sid].append(url)
            
    # Shuffle the pools
    for sid in unused_by_sample:
        random.shuffle(unused_by_sample[sid])

    manifest = []
    
    for row in dead_dataset:
        dialogue_id = row.get("sample_id")
        for qa in row.get("qa", []):
            # Try to pop an unused URL from the SAME sample_id
            pool = unused_by_sample.get(dialogue_id, [])
            if pool:
                new_url = pool.pop()
            else:
                # FALLBACK: If no unused images left, pick a random ALREADY USED image from this conversation
                fallback_pool = all_urls_by_sample.get(dialogue_id, [])
                if fallback_pool:
                    new_url = random.choice(fallback_pool)
                else:
                    print(f"CRITICAL ERROR: Conversation {dialogue_id} has absolutely NO images to use.")
                    continue
            
            question_text = qa.get("question", "")
            if isinstance(question_text, dict):
                question_text = question_text.get("text", str(question_text))
                
            manifest.append({
                "original_dialogue_id": dialogue_id,
                "original_question": question_text,
                "category": qa.get("category"),
                "old_evidence": qa.get("evidence", []),
                "new_image_url": new_url,
                "status": "Pending Generation"
            })
            
    return manifest

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="data/locomo_v2_base.json", help="Path to base dataset to map urls to conversations")
    parser.add_argument("--dead", default="../locomo-visual-ground-truth/data/locomo_dead_image.json", help="Path to dead dataset")
    parser.add_argument("--unused", default="../locomo-visual-ground-truth/maps/unused_alive_urls.json", help="Path to unused URLs")
    parser.add_argument("--output", default="data/source/replacement_manifest.json", help="Output path")
    args = parser.parse_args()
    
    with open(args.base, "r", encoding="utf-8") as f:
        base_data = json.load(f)
        
    with open(args.dead, "r", encoding="utf-8") as f:
        dead_data = json.load(f)
        
    with open(args.unused, "r", encoding="utf-8") as f:
        unused_urls = json.load(f)
        
    manifest = create_replacement_manifest(base_data, dead_data, unused_urls)
    
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)
        
    print(f"✅ Successfully mapped {len(manifest)} dead questions to CONVERSATION-LOCKED images (using fallback when necessary).")
    print(f"Manifest saved to {args.output}")

if __name__ == "__main__":
    main()
