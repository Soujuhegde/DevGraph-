# extract.py
import os, json, time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

EXTRACTION_PROMPT = """You are extracting a knowledge graph from a project README.

Extract triples using ONLY these entity types: Project, Technology, Problem, Person.
Extract triples using ONLY these relationship types: USES, SOLVES, DEPENDS_ON, BUILT_BY.

Rules:
- "Technology" means a specific library, framework, model, or tool (e.g. LangGraph, ChromaDB, FastAPI, Llama 3.3). Do NOT use generic terms like "LLM", "Custom Math Tool", or "Generative AI".
- "Problem" means the actual real-world issue the project solves (e.g. "manual hospital data entry", "inaccurate product information"). Do NOT use features or goals like "enhancing customer experience", "handling inquiries", or "streamlining operations".
- Normalize technology names exactly (e.g. always "Groq" not "Groq Cloud" or "Groq Cloud LLMs"; always "Sarvam AI" not "SarvamAI").
- Deduplication: Do not create duplicate or overlapping relationships between the same source and target. If a project USES a technology, do NOT also add a DEPENDS_ON relationship for the same technology. Choose either USES or DEPENDS_ON, not both.
- Return ONLY valid JSON, no markdown formatting, no explanation.

Output format:
{{
  "triples": [
    {{"source": "string", "source_type": "Project|Technology|Problem|Person", "relationship": "USES|SOLVES|DEPENDS_ON|BUILT_BY", "target": "string", "target_type": "Project|Technology|Problem|Person"}}
  ]
}}
OUTPUT ONLY THE JSON OBJECT. NO REASONING, NO THINKING, NO EXPLANATION.

Project name: {project_name}
README content:
{content}
"""

def extract_triples(project_name, content):
    prompt = EXTRACTION_PROMPT.format(project_name=project_name, content=content[:6000])
    client = Groq(api_key=GROQ_API_KEY)
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.0
        )
        text = response.choices[0].message.content.strip()
        data = json.loads(text)
        return data.get("triples", [])
    except Exception as e:
        print(f"API/JSON Error for {project_name}: {str(e)}")
        return []

if __name__ == "__main__":
    from ingest import load_readmes
    projects = load_readmes()
    all_triples = []
    for p in projects:
        print(f"Extracting from: {p['project_name']}")
        triples = extract_triples(p["project_name"], p["content"])
        print(f"  -> got {len(triples)} triples")
        all_triples.extend(triples)
        time.sleep(10)

    with open("extracted_triples.json", "w") as f:
        json.dump(all_triples, f, indent=2)
    print(f"\nTotal: {len(all_triples)} triples saved to extracted_triples.json")