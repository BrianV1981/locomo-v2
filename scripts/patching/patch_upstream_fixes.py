import json
import os

def patch_dataset():
    input_file = '/home/kingb/locomo-v2/locomo_v2_base.json'
    output_file = '/home/kingb/locomo-v2/locomo_v2_final.json'
    
    with open(input_file, 'r') as f:
        data = json.load(f)
        
    print("Patching dataset...")
    
    for session in data:
        if 'qa' in session:
            for qa in session['qa']:
                q = qa.get('question', '')
                ans = qa.get('answer', '')
                
                # Q57: Remove transgender symbol
                if 'symbols are important to Caroline' in q:
                    if 'transgender symbol' in ans.lower():
                        qa['answer'] = 'Rainbow flag, eagle (symbolizing freedom and pride)'
                        if '[V2_CORRECTION]' not in qa['question']:
                            qa['question'] = '[V2_CORRECTION] ' + qa['question']
                        print(f"Patched Q57: {q}")
                
                # Q95: Re-attribute bowl to Caroline
                if "Melanie's hand-painted bowl" in q:
                    if "Caroline's bowl, not Melanie's" not in ans:
                        qa['answer'] = 'art and self-expression (but this is Caroline\'s bowl, not Melanie\'s)'
                        if '[V2_CORRECTION]' not in qa['question']:
                            qa['question'] = '[V2_CORRECTION] ' + qa['question']
                        print(f"Patched Q95: {q}")
                
                # Sunrise/Sunset Conflict
                if "What has Melanie painted?" in q:
                    # Update ground truth to align with human dialogue
                    if "sunset" in ans.lower() and "sunrise" not in ans.lower():
                        qa['answer'] = qa['answer'].replace("sunset", "sunset, sunrise")
                        if '[V2_CORRECTION]' not in qa['question']:
                            qa['question'] = '[V2_CORRECTION] ' + qa['question']
                        print("Patched Sunrise/Sunset conflict.")

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
        
    print(f"Dataset patched and saved to {output_file}")

if __name__ == "__main__":
    patch_dataset()
