import pytest
from generate_replacement_questions import build_image_turn_map, process_replacements

def test_build_image_turn_map():
    dataset = [
        {
            "sample_id": "conv-1",
            "conversation": {
                "session_1": [
                    {"dia_id": "D1:1", "speaker": "Alice", "text": "Look", "img_url": ["http://img1.jpg"]}
                ]
            }
        }
    ]
    img_map = build_image_turn_map(dataset)
    assert "http://img1.jpg" in img_map
    assert img_map["http://img1.jpg"]["dia_id"] == "D1:1"
    assert img_map["http://img1.jpg"]["speaker"] == "Alice"
    assert img_map["http://img1.jpg"]["text"] == "Look"

def test_process_replacements():
    dataset = [
        {
            "sample_id": "conv-1",
            "qa": [
                {
                    "question": "Old Question",
                    "answer": "Old Answer",
                    "evidence": ["D0:0"]
                }
            ],
            "conversation": {
                "session_1": [
                    {"dia_id": "D1:1", "speaker": "Alice", "text": "Look", "img_url": ["http://new.jpg"]}
                ]
            }
        }
    ]
    
    manifest = [
        {
            "original_dialogue_id": "conv-1",
            "original_question": "Old Question",
            "category": 1,
            "new_image_url": "http://new.jpg",
            "status": "Pending"
        }
    ]
    
    llava_cache = {"http://new.jpg": "A beautiful new image."}
    img_map = build_image_turn_map(dataset)
    
    count = process_replacements(dataset, manifest, llava_cache, img_map, dry_run=True)
    
    assert count == 1
    assert manifest[0]["status"] == "Generated"
    
    qa = dataset[0]["qa"][0]
    assert qa["question"] == "mock_q"
    assert qa["answer"] == "mock_a"
    assert qa["evidence"] == ["D1:1"]
    assert qa["v2_replacement"] is True
