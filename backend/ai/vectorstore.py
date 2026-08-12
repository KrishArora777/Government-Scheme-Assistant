from pathlib import Path
from langchain_chroma import Chroma
from backend.ai.embeddings import get_embeddings
from backend.ai.text_splitter import split_documents

# Persist ChromaDB inside gov_db/chromadb/
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHROMA_PATH = str(PROJECT_ROOT / "gov_db" / "chromadb")
COLLECTION_NAME = "gov_schemes"


def build_vectorstore() -> Chroma:
    """
    Load PDFs, split into chunks, embed and persist to ChromaDB.
    Call this once (or when you add new documents).
    """
    print("📄 Loading and splitting documents...")
    chunks = split_documents()
    print(f"   → {len(chunks)} chunks created")

    print("🔢 Embedding and storing in ChromaDB...")
    embedder = get_embeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedder,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PATH,
    )
    print(f"   → Vector store saved to {CHROMA_PATH}")
    return vectorstore


def load_vectorstore() -> Chroma:
    """
    Load an existing ChromaDB vector store from disk.
    Raises if the store hasn't been built yet.
    """
    embedder = get_embeddings()
    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PATH,
        embedding_function=embedder,
    )


def get_or_build_vectorstore() -> Chroma:
    """
    Return the vector store, building it from scratch if it doesn't exist yet.
    This is the recommended entry point.
    """
    chroma_dir = Path(CHROMA_PATH)
    # If the directory is empty or missing, build from PDFs
    if not chroma_dir.exists() or not any(chroma_dir.iterdir()):
        return build_vectorstore()
    return load_vectorstore()
