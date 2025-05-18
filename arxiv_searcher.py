import arxiv
import os
import json
from typing import List

def search_papers(topic: str, max_results: int = 5) -> List[str]:
    """
    Searches arXiv for papers related to a specific topic and stores their metadata locally.

    The function creates a directory named after the sanitized topic (lowercase, spaces
    replaced with underscores). Inside this directory, it saves paper metadata in a
    JSON file named `papers_info.json`.

    If `papers_info.json` already exists, the function loads the existing data.
    It then performs a new search on arXiv. For each paper found, it checks if the
    paper's `entry_id` is already present in the loaded data. If not, the new paper's
    metadata (title, authors, summary, PDF URL, published date, and entry_id) is
    appended to the list. This ensures that duplicates are not added if the search
    is run multiple times for the same topic.

    The updated list of metadata is then saved back to `papers_info.json`.
    The function prints the absolute path to this JSON file.

    Args:
        topic: The topic to search for on arXiv (e.g., "Quantum Computing").
        max_results: The maximum number of search results to fetch from arXiv.
                     Defaults to 5.

    Returns:
        A list of paper entry_ids (unique identifiers from arXiv) found in the
        *current* search. This list may include IDs already stored if they
        appeared in the current search results.
    """
    # Sanitize the topic string to create a valid directory name.
    # Example: "Quantum Computing" -> "quantum_computing"
    directory_name = topic.lower().replace(" ", "_")

    # Create the directory for the topic if it doesn't already exist.
    # `exist_ok=True` prevents an error if the directory already exists.
    os.makedirs(directory_name, exist_ok=True)

    # Construct the full path to the JSON file where paper metadata will be stored.
    filepath = os.path.join(directory_name, "papers_info.json")

    # Load existing paper metadata from the JSON file if it exists.
    all_papers_metadata = []
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                loaded_data = json.load(f)
                # Ensure the loaded data is a list, as expected.
                if isinstance(loaded_data, list):
                    all_papers_metadata = loaded_data
                else:
                    # Handle cases where the JSON file does not contain a list (e.g., corrupted or wrong format).
                    print(f"Warning: Data in {filepath} is not a list. Starting with an empty list of papers.")
        except json.JSONDecodeError:
            # Handle cases where the JSON file is corrupted or not valid JSON.
            print(f"Warning: Could not decode JSON from {filepath}. File might be corrupted. Starting with an empty list of papers.")
        except Exception as e:
            # Catch any other unexpected errors during file loading.
            print(f"Warning: An unexpected error occurred while loading {filepath}: {e}. Starting with an empty list of papers.")

    # This list will store the entry_ids of papers found in the *current* search.
    current_search_paper_ids = []
    # Create a set of entry_ids from already stored papers for efficient duplicate checking.
    existing_entry_ids = {p['entry_id'] for p in all_papers_metadata if 'entry_id' in p}

    # Initialize the arXiv client and perform the search.
    # `arxiv.Client()` is used to interact with the arXiv API.
    # `arxiv.Search()` configures the search query and parameters.
    client = arxiv.Client()
    search = arxiv.Search(query=topic, max_results=max_results)
    # `client.results(search)` executes the search and returns an iterable of Paper objects.
    # This usage addresses a DeprecationWarning from older versions of the arxiv library.
    results = list(client.results(search))

    # Process each paper found in the current search.
    for paper in results:
        paper_entry_id = paper.entry_id
        current_search_paper_ids.append(paper_entry_id) # Keep track of all IDs from this specific search

        # Add the paper to our stored list only if its entry_id is not already present.
        # This prevents duplicates if the same paper is fetched in multiple searches.
        if paper_entry_id not in existing_entry_ids:
            # If the paper is new, extract its metadata into a dictionary.
            metadata = {
                "title": paper.title,
                "authors": [author.name for author in paper.authors], # List comprehension to get author names
                "summary": paper.summary,
                "pdf_url": paper.pdf_url,
                "published_date": paper.published.strftime('%Y-%m-%d'), # Format date as YYYY-MM-DD
                "entry_id": paper_entry_id
            }
            all_papers_metadata.append(metadata) # Add new paper's metadata to our main list
            existing_entry_ids.add(paper_entry_id)  # Add its ID to the set to avoid duplicates from *this* search session

    # Save the potentially updated list of all paper metadata back to the JSON file.
    # `indent=4` makes the JSON file human-readable.
    with open(filepath, 'w') as f:
        json.dump(all_papers_metadata, f, indent=4)

    # Print the absolute path to the JSON file for user confirmation.
    print(f"Results saved to: {os.path.abspath(filepath)}")

    # Return the list of paper entry_ids found in the current search session.
    return current_search_paper_ids

if __name__ == "__main__":
    # Example usage
    topic_to_search = "Quantum Computing"
    number_of_results = 2
    print(f"Searching for '{topic_to_search}' on arXiv (max {number_of_results} results)...")
    paper_ids = search_papers(topic=topic_to_search, max_results=number_of_results)
    print(f"Search completed. Found {len(paper_ids)} paper IDs for the current search: {paper_ids}")

    # Example of a second search to demonstrate appending behavior
    print(f"\nSearching again for '{topic_to_search}' on arXiv (max {number_of_results} results) to show appending...")
    more_paper_ids = search_papers(topic=topic_to_search, max_results=number_of_results) # Should load existing and only add new if any
    print(f"Second search completed. Found {len(more_paper_ids)} paper IDs for the current search: {more_paper_ids}")

    # Example of searching for a different topic
    another_topic = "Machine Learning"
    print(f"\nSearching for '{another_topic}' on arXiv (max {number_of_results} results)...")
    ml_paper_ids = search_papers(topic=another_topic, max_results=number_of_results)
    print(f"Search for '{another_topic}' completed. Found {len(ml_paper_ids)} paper IDs: {ml_paper_ids}")
