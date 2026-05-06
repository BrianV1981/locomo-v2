import pytest
from map_replacements import create_replacement_manifest

def test_create_replacement_manifest():
    dead_dataset = [
        {
            "sample_id": "conv-1",
            "qa": [
                {
                    "question": "What is the red object?",
                    "category": 4,
                    "evidence": ["D1:2"]
                },
                {
                    "question": {"text": "When was it painted?"},
                    "category": 2,
                    "evidence": ["D1:3"]
                }
            ]
        }
    ]
    
    unused_urls = [
        "http://alive.com/1.jpg",
        "http://alive.com/2.jpg",
        "http://alive.com/3.jpg"
    ]
    
    manifest = create_replacement_manifest(dead_dataset, unused_urls, seed=42)
    
    assert len(manifest) == 2
    
    # Check first item
    assert manifest[0]["original_dialogue_id"] == "conv-1"
    assert manifest[0]["original_question"] == "What is the red object?"
    assert manifest[0]["category"] == 4
    assert manifest[0]["old_evidence"] == ["D1:2"]
    assert "http://alive.com" in manifest[0]["new_image_url"]
    assert manifest[0]["status"] == "Pending Generation"
    
    # Check second item
    assert manifest[1]["original_question"] == "When was it painted?"
    assert manifest[1]["category"] == 2
    assert manifest[1]["new_image_url"] != manifest[0]["new_image_url"]

def test_not_enough_urls():
    dead_dataset = [
        {
            "sample_id": "conv-1",
            "qa": [
                {"question": "Q1", "category": 1, "evidence": []},
                {"question": "Q2", "category": 1, "evidence": []}
            ]
        }
    ]
    unused_urls = ["http://alive.com/1.jpg"]
    
    with pytest.raises(ValueError, match="Not enough unused URLs to map all dead questions!"):
        create_replacement_manifest(dead_dataset, unused_urls)
