# RAG Application Boilerplate

A minimal, ready-to-use boilerplate for building **Retrieval-Augmented Generation (RAG)** applications using Streamlit, Langchain, and OpenAI.

This boilerplate allows you to upload various documents (PDF, TXT, DOCX, CSV), splits the documents into chunks, generates embeddings, stores them in a FAISS vector database, and lets you chat with your documents using an LLM.

---

## Features

- **Multi-Format Document Upload**: Easy upload of PDF, TXT, DOCX, and CSV files via Streamlit interface.
- **Interactive Controls**: Sidebar sliders to dynamically adjust chunk size and retrieval parameters (top K).
- **Text Splitting**: Uses `RecursiveCharacterTextSplitter` for chunking documents.
- **Embeddings & Vector Store**: Uses OpenAI Embeddings and a local FAISS vector store.
- **Interactive Chat**: A Streamlit chat interface for interacting with the documents.
- **Configurable Settings**: Tweak model settings and default parameters in `config.py`.

---

## Prerequisites

- Python 3.8+
- An OpenAI API Key

---

## Installation

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Create a Virtual Environment**

   **Windows**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Copy the `.env_example` file to `.env`:
   ```bash
   cp .env_example .env
   ```
   Add your OpenAI API key in `.env` or input it directly through the UI.

---

## Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

1. Enter your **OpenAI API Key** in the sidebar.
2. Adjust document processing settings using the sidebar sliders if needed.
3. Upload a **supported document**.
4. Wait for the processing to finish and the vector store to be created.
5. **Start asking questions** about the content of your document in the chat interface!
6. Use the **Clear & Re-upload** button to start over with a new document.

---

## Configuration

You can adjust default RAG settings in `config.py`:
- `LLM_MODEL`: The LLM to use (default: gpt-3.5-turbo)
- `CHUNK_SIZE`: Default size of document chunks (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)
- `TOP_K`: Default number of documents retrieved for each query (default: 5)
- `LLM_TEMPERATURE`: Creativity parameter for the LLM (default: 0.2)