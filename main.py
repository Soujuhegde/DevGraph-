# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agent import app as agent_graph

app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_index():
    return FileResponse("static/index.html")

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask(q: Question):
    result = agent_graph.invoke({"question": q.question})
    return {"answer": result["answer"], "route_used": result["route"]}