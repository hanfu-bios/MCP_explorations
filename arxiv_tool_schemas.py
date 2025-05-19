# This file will store the tool schemas for the functions found in arxiv_searcher.py

search_papers_schema = {
    "name": "search_papers",
    "description": "Searches arXiv for papers related to a specific topic and stores their metadata.",
    "parameters": {
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "description": "The topic to search for on arXiv (e.g., 'Quantum Computing')."
            },
            "max_results": {
                "type": "integer",
                "description": "The maximum number of search results to fetch from arXiv. Defaults to 5."
            }
        },
        "required": ["topic"]
    },
    "returns": {
        "type": "array",
        "items": {"type": "string"},
        "description": "A list of paper entry_ids (unique identifiers from arXiv) found in the current search."
    }
}

extract_info_schema = {
    "name": "extract_info",
    "description": "Extracts and returns the metadata of a specific paper if it has been previously saved.",
    "parameters": {
        "type": "object",
        "properties": {
            "paper_id": {
                "type": "string",
                "description": "The entry_id of the paper to search for."
            }
        },
        "required": ["paper_id"]
    },
    "returns": {
        "type": "string",
        "description": "A JSON string containing the paper's metadata if found, otherwise a message indicating the paper was not found."
    }
}
