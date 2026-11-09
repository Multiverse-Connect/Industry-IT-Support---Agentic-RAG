# Industry IT Support - Agentic RAG

A production-ready End-to-End Agentic RAG (Retrieval-Augmented Generation) implementation designed for automated IT support assistance, leveraging **LangGraph, LangChain, Pinecone, and OpenAI**.

---

## Architecture Overview

This project implements an agentic workflow to handle IT support queries intelligently. Instead of traditional static retrieval, it uses an iterative agent loop capable of reasoning, utilizing tools, and retrieving context from vector databases (Pinecone) and search engines (Tavily).

---

## Prerequisites & Environment Setup

If you are setting up the environment from scratch in WSL (Windows Subsystem for Linux), follow these steps.

### 1. Update and Install Python Dependencies

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

### 2. Navigate to Project Directory

```bash
cd ~/agentic_rag/Industry-IT-Support---Agentic-RAG
```

### 3. Create and Activate the Virtual Environment

```bash
python3 -m venv project
source project/bin/activate
```

---

## Dependencies (`requirements.txt`)

The project relies on the following core libraries for FastAPI backend serving, LangGraph orchestration, and vector storage:

| Library | Description |
|---|---|
| **fastapi** | Backend web framework for serving the application. |
| **uvicorn[standard]** | ASGI server for running FastAPI. |
| **jinja2** | Template engine for rendering HTML views. |
| **python-multipart** | Handling form data uploads. |
| **pydantic-settings** | Settings management using Pydantic. |
| **langgraph** | Orchestrating multi-agent state machines and cyclic workflows. |
| **langchain-core** | Base abstractions for the LangChain ecosystem. |
| **langchain-community** | Community-contributed third-party integrations. |
| **langchain-openai** | Integration for OpenAI LLMs and chat models. |
| **langchain-tavily** | Web search tool integration. |
| **langchain-pinecone** | Vector database retriever integration for Pinecone. |
| **langchain-text-splitters** | Document splitting utilities. |
| **pinecone** | Pinecone client library for vector search. |
| **openai** | Official OpenAI Python client. |
| **pypdf** | PDF document loading and parsing. |
| **python-docx** | Microsoft Word document parsing. |
| **python-dotenv** | Environment variable management. |

### Install Requirements

To install all requirements into your active virtual environment, run:

```bash
pip install -r requirements.txt
```

