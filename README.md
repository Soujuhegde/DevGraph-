# GraphRAG System🕷️

GraphRAG System is an advanced AI Architecture Assistant that combines **Knowledge Graphs (Neo4j)** with **Semantic Vector Search (ChromaDB)** to intelligently answer deep architectural and stack-related questions about your codebase. 

Instead of relying purely on standard semantic search, this system extracts entities and relationships (e.g., *Project -> USES -> Technology*) to build a relational graph. It uses a **LangGraph Agent** to dynamically decide whether a user's question requires navigating the graph connections, searching the semantic vector space, or using a robust **Hybrid Retrieval** method.

Includes a stunning, premium dark-mode chat interface built entirely in Vanilla HTML/CSS/JS and served directly via **FastAPI**.

---

## 🚀 Features

- **Hybrid Retrieval System**: Seamlessly merges exact-match graph relationships (Neo4j) with fuzzy semantic context (ChromaDB).
- **LangGraph Routing**: An intelligent agent classifies incoming questions as either `relational` or `semantic` and executes the appropriate retrieval strategy.
- **Automated Extraction**: Uses Groq (`llama-3.3-70b-versatile`) to parse raw Markdown READMEs and extract highly accurate knowledge graph triples.
- **Premium Web UI**: A gorgeous glassmorphism chat interface featuring micro-animations, a falling-code aesthetic, and dynamic routing badges.
- **Unified Server**: The FastAPI backend acts as both the robust API for LangGraph and the static file server for the web app—run everything with a single command!

---

## 🛠️ Tech Stack

### Core
- **Python 3.11**
- **LangGraph & LangChain**: For multi-agent orchestration and routing.
- **Groq API (`llama-3.3-70b-versatile`)**: Blazing fast inference for data extraction and conversational generation.

### Databases
- **Neo4j (AuraDB)**: Cloud graph database holding the entities and relationships.
- **ChromaDB**: Local vector store utilizing the `all-MiniLM-L6-v2` embedding model for semantic similarity search.

### Web Server & Frontend
- **FastAPI**: Asynchronous web framework.
- **Uvicorn**: Lightning-fast ASGI server.
- **Vanilla Web Stack**: HTML5, custom CSS3 (animations/flexbox), and Vanilla JS.
- **Marked.js**: For rendering rich markdown responses from the LLM.

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/graphrag-copilot.git
cd graphrag-copilot
```

### 2. Set up the Environment
Create a virtual environment and install the dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .\.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory and add your credentials:
```env
NEO4J_URI=neo4j+s://your-neo4j-uri.databases.neo4j.io
NEO4J_USERNAME=your_neo4j_username
NEO4J_PASSWORD=your_neo4j_password
GROQ_API_KEY=gsk_your_groq_api_key_here
```

---

## 🧠 Building the Knowledge Graph

If you want to re-build the knowledge graph and vector store from scratch, run the pipeline scripts in this order:

1. **`python ingest.py`** - Scans your repository and aggregates markdown data.
2. **`python extract.py`** - Uses Groq to extract (Source, Relationship, Target) triples and saves to `extracted_triples.json`.
3. **`python load_graph.py`** - Pushes the extracted triples up into your Neo4j database.
4. **`python vector_store.py`** - Embeds the markdown text and indexes it locally using ChromaDB.

---

## 🏃‍♂️ Running the Application

To start the GraphRAG Agent and the premium UI, run:

```bash
uvicorn main:app --reload
```

- **Chat Interface**: Open your browser to `http://localhost:8000/`
- **API Docs**: Open your browser to `http://localhost:8000/docs`

---

## 💡 Example Queries to Try

- *"Which of my projects use LangGraph and ChromaDB together?"* (Triggers Graph Retrieval)
- *"What is the full stack chain behind the AI News Automation Agent?"* (Triggers Hybrid Retrieval)
- *"Which project reduces manual data entry in hospitals?"* (Triggers Semantic Retrieval)

---

*Built with passion by the AI Architecture Assistant.*
