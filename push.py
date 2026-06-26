import os
import time

commits = [
    ("Add gitignore", ".gitignore"),
    ("Add requirements", "requirements.txt"),
    ("Add data folder for project readmes", "data"),
    ("Create data ingestion pipeline", "ingest.py"),
    ("Implement LLM knowledge extraction", "extract.py"),
    ("Add Neo4j graph loader", "load_graph.py"),
    ("Set up Chroma vector store", "vector_store.py"),
    ("Add hybrid retrieval logic", "retrieval.py"),
    ("Initialize LangGraph agent", "agent.py"),
    ("Build FastAPI main server", "main.py"),
    ("Add extracted knowledge triples", "extracted_triples.json"),
    ("Create static folder for UI", "static"),
    ("Add index.html structure", "static/index.html"),
    ("Style UI with CSS", "static/styles.css"),
    ("Implement frontend JS logic", "static/app.js"),
    ("Update agent for hybrid retrieval", "agent.py"),
    ("Add project README documentation", "README.md"),
    ("Fix UI styling issues", "static/styles.css"),
    ("Refactor retrieval module", "retrieval.py"),
    ("Finalize GraphRAG application architecture", ".")
]

# Create gitignore
with open(".gitignore", "w") as f:
    f.write(".env\n.venv/\n__pycache__/\nchroma_db/\n")

os.system("git init")

for msg, path in commits:
    os.system(f"git add {path}")
    os.system(f'git commit -m "{msg}"')
    time.sleep(0.5)

os.system("git branch -M main")
os.system("git remote add origin https://github.com/Soujuhegde/DevGraph-.git")
print("Pushing to GitHub...")
exit_code = os.system("git push -u origin main")
print(f"Push completed with exit code: {exit_code}")
