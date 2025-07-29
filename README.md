# ArXiv Paper Searcher

This project provides a set of Python scripts to search for academic papers on [arXiv](https://arxiv.org/) and manage their metadata locally. It allows users to search for papers on specific topics, save the results, and retrieve detailed information about any saved paper.

## Features

- **Search Papers**: Find papers on arXiv by topic.
- **Save Metadata**: Automatically save the metadata of searched papers (title, authors, summary, PDF link, etc.) to a local JSON file.
- **Avoid Duplicates**: Prevents duplicate entries by checking if a paper has already been saved.
- **Extract Information**: Retrieve and display the full metadata for any specific paper you have saved.
- **Dynamic Tool Dispatcher**: A flexible system for calling functions dynamically.

## File Structure

- `arxiv_searcher.py`: Contains the core logic for searching arXiv and managing paper data.
- `arxiv_tool_schemas.py`: Defines the data schemas for the tool functions, making them easy to integrate with other systems.
- `tool_dispatcher.py`: A simple but powerful dispatcher for executing tools by name.
- `machine_learning/papers_info.json`: Example of a saved papers file for the "Machine Learning" topic.
- `quantum_computing/papers_info.json`: Example of a saved papers file for the "Quantum Computing" topic.

## How to Use

1.  **Install Dependencies**:
    You will need the `arxiv` library.
    ```bash
    pip install arxiv
    ```

2.  **Run the Searcher**:
    You can run `arxiv_searcher.py` directly to see an example of how to use the functions.
    ```bash
    python arxiv_searcher.py
    ```
    This will search for papers on "Quantum Computing" and "Machine Learning" and save them in their respective directories.

3.  **Using the Tool Dispatcher**:
    The `tool_dispatcher.py` can be used to call the search and extract functions. Here is an example of how you might use it in another script:

    ```python
    from tool_dispatcher import execute_tool

    # Search for papers on a new topic
    search_args = {"topic": "Astrophysics", "max_results": 3}
    paper_ids = execute_tool("search_papers", search_args)
    print(f"Found paper IDs: {paper_ids}")

    # Extract info for one of the papers
    if paper_ids:
        paper_id_to_find = paper_ids.split(', ')[0]
        info = execute_tool("extract_info", {"paper_id": paper_id_to_find})
        print(info)
    ```

## Functions

### `search_papers(topic: str, max_results: int = 5)`

Searches arXiv for papers on a given `topic`. It creates a directory named after the topic (e.g., `quantum_computing`) and saves the paper metadata in a `papers_info.json` file inside it.

### `extract_info(paper_id: str)`

Searches all saved `papers_info.json` files for a paper with the given `paper_id` (this is the arXiv entry ID) and returns its full metadata.
