from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from backend.ai.retriever import get_retriever

# ── Prompt ─────────────────────────────────────────────────────────────────────
_PROMPT_TEMPLATE = """You are GovAssist AI, a helpful assistant for Indian government schemes.
Answer the user's question using ONLY the context provided below.
If the answer is not in the context, say: "I couldn't find that information in the loaded documents."
Be concise, factual, and helpful. Use bullet points when listing steps or requirements.

Context:
{context}

Question: {question}

Answer:"""

_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=_PROMPT_TEMPLATE,
)


# ── Helpers ────────────────────────────────────────────────────────────────────
def _format_docs(docs: list) -> str:
    """Concatenate retrieved document chunks into a single context string."""
    return "\n\n".join(doc.page_content for doc in docs)


def _extract_sources(docs: list) -> list[str]:
    """Return unique 'filename — page N' strings from retrieved doc metadata."""
    seen, sources = set(), []
    for doc in docs:
        meta = doc.metadata
        raw_source = meta.get("source", "Unknown")
        filename = raw_source.replace("\\", "/").split("/")[-1]
        page = meta.get("page", "?")
        entry = f"{filename} — page {int(page) + 1}" if page != "?" else filename
        if entry not in seen:
            seen.add(entry)
            sources.append(entry)
    return sources


# ── Chain builder ──────────────────────────────────────────────────────────────
def build_rag_chain() -> dict:
    """
    Build and return the LCEL RAG chain components as a dict:
      {
        "chain":     the answer-generation runnable,
        "retriever": the document retriever (needed to also fetch sources),
      }
    """
    llm = OllamaLLM(model="llama3.2:latest", temperature=0.8)
    retriever = get_retriever(k=4)

    # LCEL chain: question → retrieve → format → prompt → LLM → parse
    chain = (
        {"context": retriever | RunnableLambda(_format_docs), "question": RunnablePassthrough()}
        | _PROMPT
        | llm
        | StrOutputParser()
    )

    return {"chain": chain, "retriever": retriever}


# ── Public entry point ─────────────────────────────────────────────────────────
def ask(question: str, chain: dict = None) -> dict:
    """
    Ask a question and get an answer + source citations from the RAG pipeline.

    Args:
        question: The user's natural-language question.
        chain:    Pre-built chain dict from build_rag_chain() (avoids rebuilding).

    Returns:
        {
            "answer":  str,
            "sources": list[str],   # e.g. ["PM-KISAN.pdf — page 3", ...]
        }
    """
    if chain is None:
        chain = build_rag_chain()

    # Retrieve source docs separately so we can display citations
    source_docs = chain["retriever"].invoke(question)
    answer = chain["chain"].invoke(question)

    return {
        "answer": answer.strip(),
        "sources": _extract_sources(source_docs),
    }
