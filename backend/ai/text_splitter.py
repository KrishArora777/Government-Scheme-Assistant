from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.ai.document_loader import load_documents

def split_documents():
    documents = load_documents()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(documents)
    return chunks

if __name__ == "__main__":
    chunks = split_documents()
    print(f"Total chunks generated: {len(chunks)}")
