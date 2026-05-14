import json
import sys
import os

sys.path.insert(0, "/home/kingb/aim")
try:
    from aim_core.reasoning_utils import generate_reasoning
except ImportError:
    generate_reasoning = lambda p, **kw: "{\"question\": \"mock_q\", \"answer\": \"mock_a\"}"

def build_image_turn_map(dataset):
    img_map = {}
    for row in dataset:
        sample_id = row.get("sample_id")
        conv = row.get("conversation", {})
        for i in range(1, 100):
            session_key = f"session_{i}"
            if session_key not in conv:
                break
                
            # Build the full transcript for this session
            session_transcript = ""
            for turn in conv[session_key]:
                session_transcript += f"{turn.get("speaker", "")}: {turn.get("text", "")}\n"
                
            for turn in conv[session_key]:
                urls = turn.get("img_url", [])
                if urls and isinstance(urls, list) and urls[0]:
                    img_map[urls[0]] = {
                        "sample_id": sample_id,
                        "session_transcript": session_transcript,
                        "dia_id": turn.get("dia_id")
                    }
    return img_map

def generate_new_qa(category, session_transcript, llava_desc):
    system_instruction = "You are an expert AI benchmark dataset creator. Return ONLY raw JSON without markdown formatting."
    prompt = f"""
    Create a new evaluation question based on an image shared during a conversation.
    
    CRITICAL REQUIREMENT: The question MUST NOT just be an odd, specific question about the image itself (e.g. "What breed is the dog?"). 
    It MUST be highly relevant to the BROADER CONVERSATION. It must require an AI agent to read the conversation text AND look at the image to synthesize the correct answer. 
    
    *** NEW REQUIREMENT ***
    The question MUST contain strong temporal or conversational anchors (e.g. "In the photo Caroline shared of the basketball game...", "Regarding the image Melanie sent on October 13...", or "When Melanie shared a picture of her ceramic plate, what color was it?"). 
    A search engine MUST be able to uniquely identify WHICH image is being asked about based on the text of the question alone. NEVER ask "What is depicted in the image shared by Melanie?" without specifying WHICH image you mean.
    
    Category requested: {category} (1=Factual, 2=Temporal, 3=Reasoning, 4=Multi-hop/Reference)
    
    === Full Session Transcript ===
    {session_transcript}
    
    === Image Description (OCR/Visuals attached to one of the turns) ===
    {llava_desc}
    
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
    replaced_count = 0
    for item in manifest:
        dialogue_id = item["original_dialogue_id"]
        orig_q = item["original_question"]
        new_url = item["new_image_url"]
        category = item["category"]
        
        turn_context = img_map.get(new_url, {})
        new_dia_id = turn_context.get("dia_id")
        session_transcript = turn_context.get("session_transcript", "")
        llava_desc = llava_cache.get(new_url, "A photo.")
        
        if dry_run:
            new_q, new_a = "mock_q", "mock_a"
        else:
            import time
            new_q, new_a = generate_new_qa(category, session_transcript, llava_desc)
            time.sleep(1)  # Pace to avoid rate limits
            
        for row in dataset:
            if row.get("sample_id") == dialogue_id:
                for qa in row.get("qa", []):
                    q_text = qa.get("question", "")
                    if isinstance(q_text, dict):
                        q_text = q_text.get("text", "")
                        
                    if orig_q in q_text:
                        qa["question"] = f"[V2_REPLACEMENT] {new_q}"
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
    parser.add_argument("--dataset", default="data/locomo_v2_base.json")
    parser.add_argument("--manifest", default="data/replacement_manifest.json")
    parser.add_argument("--cache", default="../locomo-visual-ground-truth/llava_7b_cache.json")
    parser.add_argument("--output", default="data/locomo_v2_final.json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    
    with open(args.dataset, "r", encoding="utf-8") as f:
        dataset = json.load(f)
        
    with open(args.manifest, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    try:
        with open(args.cache, "r", encoding="utf-8") as f:
            llava_cache = json.load(f)
    except FileNotFoundError:
        llava_cache = {}
        
    img_map = build_image_turn_map(dataset)
    
    count = process_replacements(dataset, manifest, llava_cache, img_map, dry_run=args.dry_run)
    
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4)
        
    with open(args.manifest, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)

if __name__ == "__main__":
    main()
