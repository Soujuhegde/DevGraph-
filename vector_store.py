# vector_store.py
import os, chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

client = chromadb.PersistentClient(path="./chroma_db")
# Groq does not have embedding models, so we rely on ChromaDB's default local embedding model (all-MiniLM-L6-v2)
collection = client.get_or_create_collection(name="project_readmes")

def index_readmes(projects):
    collection.add(
        documents=[p["content"][:8000] for p in projects],
        ids=[p["project_name"] for p in projects],
        metadatas=[{"project_name": p["project_name"]} for p in projects]
    )

def semantic_search(query, n_results=3):
    results = collection.query(query_texts=[query], n_results=n_results)
    return results

if __name__ == "__main__":
    from ingest import load_readmes
    projects = load_readmes()
    index_readmes(projects)
    print(f"Indexed {len(projects)} READMEs into ChromaDB")

    test = semantic_search("which project reduces manual data entry in hospitals")
    print(test["ids"])