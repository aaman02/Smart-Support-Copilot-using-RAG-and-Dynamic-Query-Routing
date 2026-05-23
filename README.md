# 🤖 Smart Support Copilot

An intelligent customer support application built using **Retrieval-Augmented Generation (RAG)**, **LangChain**, **FAISS**, and **Streamlit**. 

This Smart Support Copilot is designed to ingest technical manuals and provide grounded, highly accurate responses to user queries. It features intelligent query classification, dynamic response routing, and conversational memory to ensure a seamless and context-aware user experience.
---
# API LINK: 
https://smart-support-using-rag-and-dynamic-query-routing-aman.streamlit.app/

---

## ✨ Key Features

* **Intelligent Query Classification:** Automatically categorizes incoming user queries to determine the best response strategy.
* **Dynamic Response Routing:** Routes queries to the appropriate LLM chain or module based on the classification.
* **Retrieval-Augmented Generation (RAG):** Grounds responses in factual data extracted from provided technical manuals (e.g., `galaxy.txt`), minimizing hallucinations.
* **Conversational Memory:** Retains chat history to maintain context across multi-turn conversations.
* **Interactive UI:** A clean, user-friendly web interface powered by Streamlit.

---

## 🛠️ Tech Stack

* **LLM Provider:** Azure OpenAI GPT-4 (or preferred Azure OpenAI model)
* **Framework:** LangChain
* **Vector Store:** FAISS (Facebook AI Similarity Search)
* **Frontend:** Streamlit
* **Language:** Python 3.x

---

## 📂 Project Structure

```text
smart-support-copilot/
│
├── app.py                 # Main Streamlit application entry point
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API keys)
│
├── data/                  
│   └── galaxy.txt         # Sample technical manual/knowledge base
│
├── modules/
│   ├── rag_pipeline.py    # Logic for document loading, chunking, and retrieval
│   ├── classifier.py      # LLM-based query classification logic
│   ├── response_router.py # Routing logic based on query class
│   ├── prompts.py         # System prompts and templates
│   ├── memory.py          # Conversational memory management
│   └── utils.py           # Helper functions
│
├── vectorstore/
│   └── faiss_index/       # Persisted FAISS vector embeddings
│
└── README.md              # Project documentation
