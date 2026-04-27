import json
import random

def create_replacement_manifest(dead_dataset, unused_urls, seed=42):
    """Maps dead questions to unused image URLs."""
    random.seed(seed)
    
    # Shuffle the unused urls
    available_urls = list(unused_urls)
    random.shuffle(available_urls)
    
    manifest = []
    
    for dialogue_idx, row in enumerate(dead_dataset):
        dialogue_id = row.get('sample_id', f'conv-unknown-{dialogue_idx}')
        for qa_idx, qa in enumerate(row.get('qa', [])):
            if not available_urls:
                raise ValueError("Not enough unused URLs to map all dead questions!")
            
            new_url = available_urls.pop()
            
            question_text = qa.get('question', '')
            if isinstance(question_text, dict):
                question_text = question_text.get('text', str(question_text))
                
            manifest.append({
                "original_dialogue_id": dialogue_id,
                "original_question": question_text,
                "category": qa.get('category'),
                "old_evidence": qa.get('evidence', []),
                "new_image_url": new_url,
                "status": "Pending Generation"
            })
            
    return manifest

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dead", default="../locomo-visual-ground-truth/locomo_dead_image.json", help="Path to dead dataset")
    parser.add_argument("--unused", default="../locomo-visual-ground-truth/unused_alive_urls.json", help="Path to unused URLs")
    parser.add_argument("--output", default="replacement_manifest.json", help="Output path")
    args = parser.parse_args()
    
    with open(args.dead, 'r', encoding='utf-8') as f:
        dead_data = json.load(f)
        
    with open(args.unused, 'r', encoding='utf-8') as f:
        unused_urls = json.load(f)
        
    manifest = create_replacement_manifest(dead_data, unused_urls)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=4)
        
    print(f"✅ Successfully mapped {len(manifest)} dead questions to new unused images.")
    print(f"Manifest saved to {args.output}")

if __name__ == "__main__":
    main()
