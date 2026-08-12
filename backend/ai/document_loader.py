from pathlib import Path
from langchain_community.document_loaders import PyPDFDirectoryLoader

# Resolve data/ relative to the project root (two levels up from this file)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

def load_documents():
    """Load all PDFs from the data/ directory."""
    loader = PyPDFDirectoryLoader(str(DATA_DIR))
    return loader.load()
