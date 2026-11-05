from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from classifier import classify_task
from agents.copy_agent import run as copy_run
from agents.research_agent import run as research_run
from agents.analysis_agent import run as analysis_run
import json, os

app = FastAPI(title="SZB Orquestradora", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskRequest(BaseModel):
    task: str
    client: str

class TaskResponse(BaseModel):
    result: str
    agent_used: str
    task_type: str
    client: str

def load_client_context(client: str) -> dict:
    path = f"clients/{client}.json"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"Cliente '{client}' não encontrado.")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/")
def root():
    return {"status": "ok", "service": "SZB Orquestradora"}

@app.post("/run", response_model=TaskResponse)
async def run_task(body: TaskRequest):
    context = load_client_context(body.client)
    task_type = await classify_task(body.task)

    if task_type == "copy":
        result = await copy_run(body.task, context)
        agent_used = "copy_agent (GPT-4o)"
    elif task_type == "research":
        result = await research_run(body.task, context)
        agent_used = "research_agent (Gemini 1.5)"
    elif task_type == "analysis":
        result = await analysis_run(body.task, context)
        agent_used = "analysis_agent (Claude Sonnet)"
    else:
        raise HTTPException(status_code=422, detail=f"Tipo de tarefa desconhecido: {task_type}")

    return TaskResponse(
        result=result,
        agent_used=agent_used,
        task_type=task_type,
        client=body.client,
    )
