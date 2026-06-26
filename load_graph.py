# load_graph.py
import os, json
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
)

def load_triples(triples):
    with driver.session() as session:
        for t in triples:
            session.run(
                f"""
                MERGE (s:{t['source_type']} {{name: $source}})
                MERGE (tg:{t['target_type']} {{name: $target}})
                MERGE (s)-[r:{t['relationship']}]->(tg)
                """,
                source=t["source"], target=t["target"]
            )

if __name__ == "__main__":
    with open("extracted_triples.json") as f:
        triples = json.load(f)
    load_triples(triples)
    print(f"Loaded {len(triples)} triples into Neo4j")
    driver.close()