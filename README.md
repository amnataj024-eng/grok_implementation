# FastAPI Groq Chat & RAG Web Application

A lightweight, high-performance web service built with **FastAPI** and the **Groq API** that provides endpoints for both **Basic Conversational AI** and **Retrieval-Augmented Generation (RAG)** using custom local knowledge documents.

---

## 🚀 Features

* **FastAPI Backend:** Fully asynchronous, robust API framework with automatic interactive documentation (`/docs`).
* **Groq Integration:** Utilizes high-speed language models (such as `llama-3.3-70b-versatile`) for instant response generation.
* **Basic Chat Endpoint (`/api/chat`):** Supports conversational history and multi-turn messaging.
* **RAG Chat Endpoint (`/api/rag`):** Grounded document querying that references a structured local handbook (`knowledge.txt`).
* **CORS Enabled:** Ready for integration with frontend applications or static UI deployments.

---

## 📁 Project Structure

```text
fastapi-groq-rag/
├── sample_docs/
│   └── knowledge.txt     # Context document for RAG implementation
├── app.py                # Main FastAPI application
├── requirements.txt      # Python dependencies
├── .env                  # Local environment variables
└── README.md             # Project documentation