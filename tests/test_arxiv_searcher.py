import os
import json
import pytest
from arxiv_searcher import search_papers, extract_info

def test_search_papers_creates_files(tmp_path):
    """
    Tests if search_papers creates the correct directory and JSON file.
    """
    test_topic = "electron"  # A simple, common topic
    max_results = 1

    # Run the search, directing output to the temporary directory
    paper_ids = search_papers(topic=test_topic, max_results=max_results, base_dir=str(tmp_path))

    # Check if the paper_ids list is returned (might be empty, but should be a list)
    assert isinstance(paper_ids, list)
    if paper_ids:
        assert isinstance(paper_ids[0], str)

    # Check if the topic directory was created
    topic_dir = tmp_path / test_topic
    assert topic_dir.is_dir()

    # Check if the JSON file was created
    json_file = topic_dir / "papers_info.json"
    assert json_file.is_file()

    # Check the content of the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)

    assert isinstance(data, list)
    # If the search returned results, check the structure of the first result
    if len(data) > 0:
        paper_info = data[0]
        assert "title" in paper_info
        assert "authors" in paper_info
        assert "summary" in paper_info
        assert "entry_id" in paper_info
        assert paper_info["entry_id"] in paper_ids

def test_extract_info_retrieves_data(tmp_path):
    """
    Tests if extract_info can correctly find paper metadata from a dummy file
    and handle cases where the paper is not found.
    """
    # Create a dummy directory structure and a papers_info.json file
    test_topic = "test_topic"
    topic_dir = tmp_path / test_topic
    os.makedirs(topic_dir)

    dummy_paper_id = "1234.5678v1"
    dummy_paper_info = {
        "title": "A Test Paper",
        "authors": ["Test Author"],
        "summary": "This is a test.",
        "entry_id": dummy_paper_id
    }

    json_file = topic_dir / "papers_info.json"
    with open(json_file, 'w') as f:
        json.dump([dummy_paper_info], f)

    # Test 1: Successfully extract the dummy paper's info
    extracted_data_str = extract_info(paper_id=dummy_paper_id, base_dir=str(tmp_path))
    assert extracted_data_str is not None
    extracted_data = json.loads(extracted_data_str)
    assert extracted_data["title"] == "A Test Paper"
    assert extracted_data["entry_id"] == dummy_paper_id

    # Test 2: Attempt to extract info for a non-existent paper
    non_existent_id = "0000.0000v0"
    not_found_message = extract_info(paper_id=non_existent_id, base_dir=str(tmp_path))
    assert "no saved information" in not_found_message
