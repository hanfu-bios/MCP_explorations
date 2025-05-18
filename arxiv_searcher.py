import arxiv
import os
import json
from typing import List

# Global constant for the base directory where topic-specific paper subdirectories are stored.
PAPER_DIR = "."

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

def extract_info(paper_id: str) -> str:
    """
    Searches all saved paper metadata in topic folders under PAPER_DIR for a specific paper.

    Args:
        paper_id: The entry_id of the paper to search for.

    Returns:
        A string containing the paper's metadata as a pretty-printed JSON if found,
        otherwise a message indicating the paper was not found.
    """
    # Iterate through all items (files and directories) in the PAPER_DIR.
    # PAPER_DIR is expected to contain subdirectories, each named after a topic.
    for item_name in os.listdir(PAPER_DIR):
        # Construct the full path for the item.
        topic_dir_path = os.path.join(PAPER_DIR, item_name)

        # Check if the current item is a directory; topic folders are directories.
        if os.path.isdir(topic_dir_path):
            # Construct the path to the 'papers_info.json' file within this topic directory.
            json_path = os.path.join(topic_dir_path, "papers_info.json")

            # Check if the 'papers_info.json' file actually exists in this directory.
            if os.path.exists(json_path):
                try:
                    # Attempt to open and load the JSON data from the file.
                    with open(json_path, 'r') as f:
                        papers_data = json.load(f)

                    # The JSON file is expected to contain a list of paper metadata dictionaries.
                    # If it's not a list, print a warning and skip this file.
                    if not isinstance(papers_data, list):
                        print(f"Warning: Data in {json_path} is not a list. Skipping.")
                        continue # Move to the next item in PAPER_DIR

                    # Iterate through each paper's metadata in the loaded list.
                    for paper_metadata in papers_data:
                        # Safely access 'entry_id' using .get() to avoid KeyError if 'entry_id' is missing.
                        # Check if the current paper's 'entry_id' matches the requested 'paper_id'.
                        if paper_metadata.get('entry_id') == paper_id:
                            # Paper found. Convert the metadata dictionary to a pretty-printed JSON string.
                            # `indent=4` ensures the JSON string is formatted with an indent of 4 spaces for readability.
                            return json.dumps(paper_metadata, indent=4)
                except json.JSONDecodeError:
                    # Handle cases where the file is not valid JSON (e.g., corrupted).
                    print(f"Warning: Could not decode JSON from {json_path}. File may be corrupted. Skipping.")
                    continue # Move to the next item in PAPER_DIR
                except FileNotFoundError:
                    # This case should ideally be caught by `os.path.exists(json_path)` earlier.
                    # However, it's included for robustness against rare race conditions or unexpected filesystem behavior.
                    print(f"Warning: File not found {json_path} (unexpected as os.path.exists was true). Skipping.")
                    continue # Move to the next item in PAPER_DIR
                except Exception as e:
                    # Catch any other unexpected errors during file reading or JSON processing.
                    print(f"Warning: An unexpected error occurred while reading {json_path}: {e}. Skipping.")
                    continue # Move to the next item in PAPER_DIR

    # If the loop completes without returning, the paper_id was not found in any file.
    return f"There's no saved information related to paper {paper_id}."

if __name__ == "__main__":
    print("--- Testing search_papers ---")
    # Example for search_papers (can keep existing or modify)
    topic1 = "Quantum Computing"
    print(f"Searching for '{topic1}' papers (max 1)...")
    qc_paper_ids = search_papers(topic=topic1, max_results=1)
    print(f"Search for '{topic1}' completed. Found IDs: {qc_paper_ids}")

    topic2 = "Machine Learning"
    print(f"\nSearching for '{topic2}' papers (max 1)...")
    ml_paper_ids = search_papers(topic=topic2, max_results=1) # Example of appending
    print(f"Search for '{topic2}' completed. Found IDs: {ml_paper_ids}")

    print("\n--- Testing extract_info ---")
    # Test extract_info with a found paper ID
    if qc_paper_ids:
        first_qc_id = qc_paper_ids[0]
        print(f"\nExtracting info for paper ID: {first_qc_id}")
        info_found = extract_info(paper_id=first_qc_id)
        print(info_found)
    else:
        print(f"\nSkipping extract_info test for '{topic1}' as no papers were found in the initial search.")

    # Test extract_info with a non-existent paper ID
    non_existent_id = "this_id_should_not_exist_12345"
    print(f"\nExtracting info for non-existent paper ID: {non_existent_id}")
    info_not_found = extract_info(paper_id=non_existent_id)
    print(info_not_found)

    # Example: Searching again for Quantum Computing to show papers are appended
    # and old papers can still be extracted
    print(f"\nSearching again for '{topic1}' papers (max 1, new paper expected if available)...")
    # This search will likely find the same paper or a new one.
    # If it's the same paper, its entry_id will already exist, and it won't be added again to papers_info.json.
    # If it's a new paper (e.g., if a new paper matching the query became the top result),
    # its metadata would be appended to papers_info.json.
    search_papers(topic=topic1, max_results=1)

    if qc_paper_ids: # Try extracting the originally found paper again
        first_qc_id = qc_paper_ids[0] # Use the ID from the *first* search for consistency in this test
        print(f"\nRe-extracting info for original paper ID: {first_qc_id} (after potential append)")
        info_found_again = extract_info(paper_id=first_qc_id)
        print(info_found_again)
