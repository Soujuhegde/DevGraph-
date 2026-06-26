# agent.py
import os
from groq import Groq
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict
from retrieval import graph_retrieve, shared_stack_query, hybrid_retrieve
from vector_store import semantic_search

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def ask_groq(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    return response.choices[0].message.content.strip()

class AgentState(TypedDict):
    question: str
    route: str
    context: str
    answer: str

def classify_question(state: AgentState) -> AgentState:
    prompt = f"""Classify this question into exactly one category:
- "relational" if it asks about connections, shared technologies, or chains between entities (e.g. "which projects use X and Y", "what's the stack behind Z")
- "semantic" if it's a general topic or similarity question (e.g. "which project is about automation")

Question: {state['question']}
Reply with only one word: relational or semantic"""
    route = ask_groq(prompt).lower()
    state["route"] = "relational" if "relational" in route else "semantic"
    return state

def relational_retrieval(state: AgentState) -> AgentState:
    # naive entity extraction for the demo — ask LLM to pull the tech/project names out
    prompt = f"""Extract up to 2 technology or project names mentioned in this question, comma separated, nothing else: {state['question']}"""
    names = ask_groq(prompt).split(",")
    names = [n.strip() for n in names if n.strip()]

    if len(names) >= 2:
        projects = shared_stack_query(names[0], names[1])
        # fallback to semantic search to provide richer context
        semantic = semantic_search(state["question"], n_results=3)
        state["context"] = f"Graph Projects using both {names[0]} and {names[1]}: {projects}\nSemantic Docs: {semantic['documents']}"
    elif len(names) == 1:
        results = hybrid_retrieve(state["question"], entity_hint=names[0])
        state["context"] = f"Graph Context: {results['graph_context']}\nSemantic Docs: {results['vector_hits']['documents']}"
    else:
        results = hybrid_retrieve(state["question"])
        state["context"] = f"Semantic Docs: {results['vector_hits']['documents']}"
    return state

def semantic_retrieval(state: AgentState) -> AgentState:
    results = semantic_search(state["question"])
    state["context"] = str(results["documents"])
    return state

def generate_answer(state: AgentState) -> AgentState:
    prompt = f"""Answer the question using only the context below. Be specific and cite project/technology names from the context.

Context: {state['context']}
Question: {state['question']}
Answer:"""
    state["answer"] = ask_groq(prompt)
    return state

def route_decision(state: AgentState) -> str:
    return state["route"]

graph = StateGraph(AgentState)
graph.add_node("classify", classify_question)
graph.add_node("relational_retrieval", relational_retrieval)
graph.add_node("semantic_retrieval", semantic_retrieval)
graph.add_node("generate", generate_answer)

graph.set_entry_point("classify")
graph.add_conditional_edges("classify", route_decision, {
    "relational": "relational_retrieval",
    "semantic": "semantic_retrieval"
})
graph.add_edge("relational_retrieval", "generate")
graph.add_edge("semantic_retrieval", "generate")
graph.add_edge("generate", END)

app = graph.compile()

if __name__ == "__main__":
    result = app.invoke({"question": "Which of my projects use LangGraph and ChromaDB together?"})
    print(result["answer"])