import sys
from langchain_ollama import OllamaEmbeddings

try:
    from backend.ai.text_splitter import split_documents
except ImportError:
    from text_splitter import split_documents

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def get_embeddings():
    embedder = OllamaEmbeddings(
        model="qwen3-embedding:0.6b"
    )
    return embedder

if __name__ == "__main__":
    print("Program Started...")
    print("Loading and splitting documents...")
    chunks = split_documents()
    print(f"Loaded {len(chunks)} chunks")

    print("Generating embeddings using OllamaEmbeddings...")
    embedder = get_embeddings()

    # Embed sample chunks
    sample_chunks = [chunk.page_content for chunk in chunks[:5]]
    embeddings = embedder.embed_documents(sample_chunks)

    print("Done!")
    print(f"Sample Embeddings Count: {len(embeddings)}")
    print(f"Embedding Vector Dimension: {len(embeddings[0])}")
