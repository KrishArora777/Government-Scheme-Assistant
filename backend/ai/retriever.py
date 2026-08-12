from langchain_core.vectorstores import VectorStoreRetriever
from backend.ai.vectorstore import get_or_build_vectorstore


def get_retriever(k: int = 4) -> VectorStoreRetriever:
    """
    Return a LangChain retriever backed by the ChromaDB vector store.

    Args:
        k: Number of relevant document chunks to retrieve per query.
    """
    vectorstore = get_or_build_vectorstore()
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )
