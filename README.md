# GovAssist AI

AI-powered Government Scheme Assistant built using Python,
LangChain, RAG and Streamlit.

## Problem Statement

Citizens often find it difficult to discover government schemes,
understand eligibility criteria, required documents and application
procedures.

## Features

- AI-based Government Scheme Assistant
- Government document-based RAG
- Scheme information retrieval
- Eligibility assistance
- Source-backed answers
- Streamlit interface

## Tech Stack

- Python
- LangChain
- Streamlit
- FAISS
- Ollama / Gemini
- RAG

## Project Architecture

Government Documents
        ↓
Document Loader
        ↓
Text Splitter
        ↓
Embeddings
        ↓
Vector Database
        ↓
Retriever
        ↓
LLM
        ↓
Answer

