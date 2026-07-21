# Study Buddy 📚🤖

**Study Buddy** is an intelligent, retrieval-augmented study assistant and Model Context Protocol (MCP) server. It helps students query, summarize, and track progress over their study materials (like lecture notes, textbooks, and PDF documents) by leveraging vector embeddings and a conversational history database.

---

## 🚀 Key Features

* **Grounded Study Q&A**: Get precise answers based directly on your notes. If the answer isn't in your materials, Study Buddy lets you know to prevent hallucinations.
* **Conversational Memory**: Stores conversation history in a local SQLite database, allowing you to ask follow-up questions naturally in a multi-turn chat.
* **Document Summarization**: Summarizes documents by retrieving and synthesising content chunks directly from the vector store.
* **Study Progress Tracker**: Keeps an audit log of your study session, tracking the number of questions asked, documents summarized, and recent activities.
* **FastMCP Server Integration**: Exposes all functions as MCP tools, making it compatible with MCP-native AI clients (like Claude Desktop).

---

## 🛠️ Architecture Overview

The project is structured modularly:

```text
Study Buddy/
├── app/
│   ├── embedding/     # Configures HuggingFace embedding models (BGE-small)
│   ├── ingestion/     # PDF loading (PyMuPDF) and recursive text chunking
│   ├── memory/        # SQLite backend to log chats and student activity
│   ├── pipeline/      # Central StudyBuddyPipeline running the RAG logic
│   ├── prompts/       # Dynamic prompt templates injecting chat history
│   ├── retriever/     # Wraps vector database similarity queries
│   ├── utils/         # Custom logging and exception classes
│   └── vector_db/     # ChromaDB manager for document vector store
├── data/
│   └── raw/           # Place your PDF documents here (e.g. unit1.pdf)
├── database/
│   ├── chroma/        # Directory containing Chroma DB persistence files
│   └── SQL/           # Directory containing SQLite DB (study_buddy.db)
├── config.py          # Unified paths and constants configuration
├── main.py            # Local CLI testing execution script
├── server.py          # FastMCP server exposing assistant tools
└── requirements.txt   # Python dependency manifest
```

---

## 📦 Database Schema

A local SQLite database is stored at `database/SQL/study_buddy.db` with the following schema:

1. **`chat_history`**: Tracks multi-turn conversational turns.
   * `id` (INTEGER PRIMARY KEY)
   * `session_id` (TEXT)
   * `role` (TEXT: `user` or `assistant`)
   * `content` (TEXT)
   * `timestamp` (DATETIME)

2. **`study_progress`**: Logs user learning activities.
   * `id` (INTEGER PRIMARY KEY)
   * `session_id` (TEXT)
   * `action_type` (TEXT: e.g., `query`, `summarize`)
   * `target_name` (TEXT: e.g., question snippet or document name)
   * `details` (TEXT)
   * `timestamp` (DATETIME)

---

## ⚙️ Setup & Installation

### 1. Clone the repository and navigate inside:
```bash
cd "Study Buddy"
```

### 2. Create and activate a Virtual Environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables:
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## 🏃 Running the Project

### Local Test Execution
To run a test query directly from the terminal (which will automatically populate the SQLite database and retrieve responses based on `data/raw/unit1.pdf` context):
```bash
python main.py
```

### Run as an MCP Server
To host the RAG assistant as a Model Context Protocol server (useful for integrating with AI clients):
```bash
fastmcp run server.py
```

---

## 🛠️ MCP Tools Provided

Once connected, Study Buddy exposes the following tools to the client model:

1. **`ask_study_question(question, session_id)`**: Solves study questions using stored notes with conversation context support.
2. **`summarize_document(document_name, session_id)`**: Compiles a structured summary of document pages in the vector DB.
3. **`get_study_progress(session_id)`**: Outputs an overview of questions asked and documents summarized.
4. **`search_notes(query, k)`**: Returns raw text chunks matching a similarity search query.
5. **`get_sources(query, k)`**: Lists the source documents and page numbers utilized to back up a response.
