# retrieval.py
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
from vector_store import semantic_search

load_dotenv()
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
)

def graph_retrieve(entity_name, max_hops=2):
    """Pull everything connected to a given entity within N hops."""
    with driver.session() as session:
        result = session.run(
            f"""
            MATCH (n {{name: $name}})-[r*1..{max_hops}]-(connected)
            RETURN n.name AS source, connected.name AS target, [rel in r | type(rel)] AS relationships
            LIMIT 25
            """,
            name=entity_name
        )
        return [dict(record) for record in result]

def shared_stack_query(tech1, tech2):
    """Answers: which projects use BOTH tech1 AND tech2"""
    with driver.session() as session:
        result = session.run(
            """
            MATCH (p:Project)-[:USES]->(:Technology {name: $tech1})
            MATCH (p)-[:USES]->(:Technology {name: $tech2})
            RETURN p.name AS project
            """,
            tech1=tech1, tech2=tech2
        )
        return [record["project"] for record in result]

def hybrid_retrieve(query, entity_hint=None):
    """Combines semantic search with graph traversal for richer context."""
    vector_hits = semantic_search(query, n_results=3)
    graph_context = graph_retrieve(entity_hint) if entity_hint else []
    return {"vector_hits": vector_hits, "graph_context": graph_context}