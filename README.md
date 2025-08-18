# ArXiv Paper Searcher

This is a Python tool for searching for academic papers on [arXiv.org](https://arxiv.org) and managing their metadata locally.

## Features

- Search for papers by topic.
- Save paper metadata (title, authors, summary, etc.) to local JSON files.
- Avoids creating duplicate entries for the same paper.
- Retrieve saved metadata for a specific paper by its arXiv ID.

## Setup

1. **Install Dependencies:**
   This project's dependencies are listed in the `requirements.txt` file. You can install them using pip:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the script and see an example of it in action, execute the following command:

```bash
python3 arxiv_searcher.py
```

This will:
1. Create a directory named `papers_db` in your current location.
2. Search for papers on "Quantum Computing" and "Machine Learning".
3. Save the paper metadata inside `papers_db`.
4. Run a few example extractions.

## Testing

This project uses `pytest` for testing. To run the test suite, first make sure you have `pytest` installed (`pip install pytest`), and then run the following command from the root of the repository:

```bash
PYTHONPATH=. pytest
```
