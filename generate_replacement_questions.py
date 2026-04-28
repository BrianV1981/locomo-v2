import json
import sys
import os

# Add aim_core to path for reasoning utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
try:
    from aim_core.reasoning_utils import generate_reasoning
except ImportError:
    # For testing without aim_core
    generate_reasoning = lambda p, **kw: '{"question": "mock_q", "answer": "mock_a"}'

def build_image_turn_map(dataset):
    """Map image URL to its turn context (speaker, text, dia_id) and sample_id."""
    img_map = {}
    for row in dataset:
        sample_id = row.get("sample_id")
        conv = row.get("conversation", {})
        for i in range(1, 100):
            session_key = f'session_{i}'
            if session_key not in conv:
                break
            for turn in conv[session_key]:
                urls = turn.get("img_url", [])
                if urls and isinstance(urls, list) and urls[0]:
                    img_map[urls[0]] = {
                        "sample_id": sample_id,
                        "speaker": turn.get("speaker"),
                        "text": turn.get("text"),
                        "dia_id": turn.get("dia_id")
                    }
    return img_map

def generate_new_qa(category, speaker, text, llava_desc):
    """Prompt the LLM to generate a new QA pair."""
    system_instruction = "You are an expert AI benchmark dataset creator. Return ONLY raw JSON without markdown formatting."
    prompt = f"""
    Create a new evaluation question based on an image shared in a chat.
    The question must require understanding BOTH the image description and the conversation context.
    
    Category requested: {category} (1=Factual, 2=Temporal, 3=Reasoning, 4=Multi-hop/Reference)
    Speaker: {speaker}
    Utterance: {text}
    Image Description (OCR): {llava_desc}
    
    Output exactly this JSON format:
    {{
        "question": "The generated question text here",
        "answer": "The correct answer here"
    }}
    """
    
    response = generate_reasoning(prompt, system_instruction=system_instruction)
    try:
        if response.startswith("```json"):
            response = response[7:-3].strip()
        elif response.startswith("```"):
            response = response[3:-3].strip()
        parsed = json.loads(response)
        return parsed.get("question", "Fallback Question"), parsed.get("answer", "Fallback Answer")
    except json.JSONDecodeError:
        return "Failed to generate question", "Failed to generate answer"

def process_replacements(dataset, manifest, llava_cache, img_map, dry_run=False):
    """Modifies the dataset in-place using the manifest."""
    
    # Create a quick lookup for qa items by original_dialogue_id and old_evidence
    # This is a bit tricky because evidence is a list. We match by original_question text
    # to be safe, as it's unique enough within a dialogue.
    
    replaced_count = 0
    for item in manifest:
        dialogue_id = item["original_dialogue_id"]
        orig_q = item["original_question"]
        new_url = item["new_image_url"]
        category = item["category"]
        
        turn_context = img_map.get(new_url, {})
        new_dia_id = turn_context.get("dia_id")
        speaker = turn_context.get("speaker", "Unknown")
        text = turn_context.get("text", "")
        llava_desc = llava_cache.get(new_url, "A photo.")
        
        # Generate new QA
        if dry_run:
            new_q, new_a = "mock_q", "mock_a"
        else:
            new_q, new_a = generate_new_qa(category, speaker, text, llava_desc)
            
        # Find the original question in the dataset and replace it
        for row in dataset:
            if row.get("sample_id") == dialogue_id:
                for qa in row.get("qa", []):
                    q_text = qa.get("question", "")
                    if isinstance(q_text, dict):
                        q_text = q_text.get("text", "")
                        
                    if q_text == orig_q:
                        qa["question"] = new_q
                        qa["answer"] = new_a
                        qa["evidence"] = [new_dia_id] if new_dia_id else []
                        qa["v2_replacement"] = True
                        replaced_count += 1
                        item["status"] = "Generated"
                        break
    return replaced_count

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="locomo_v2_base.json")
    parser.add_argument("--manifest", default="replacement_manifest.json")
    parser.add_argument("--cache", default="../locomo-visual-ground-truth/llava_7b_cache.json")
    parser.add_argument("--output", default="locomo_v2_final.json")
    parser.add_argument("--dry-run", action="store_true", help="Do not call LLM, use mock data")
    args = parser.parse_args()
    
    with open(args.dataset, "r", encoding="utf-8") as f:
        dataset = json.load(f)
        
    with open(args.manifest, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    try:
        with open(args.cache, "r", encoding="utf-8") as f:
            llava_cache = json.load(f)
    except FileNotFoundError:
        print("Warning: LLaVA cache not found. Using fallback descriptions.")
        llava_cache = {}
        
    img_map = build_image_turn_map(dataset)
    print(f"Loaded {len(manifest)} replacement tasks.")
    
    count = process_replacements(dataset, manifest, llava_cache, img_map, dry_run=args.dry_run)
    
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
        
    with open(args.manifest, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4, ensure_ascii=False)
        
    print(f"✅ Successfully generated and replaced {count} questions.")
    print(f"Saved final V2 dataset to {args.output}")

if __name__ == "__main__":
    main()
