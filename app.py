# app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

# --- App Setup ---
app = FastAPI(title="SupportEnv Hackathon Space")

# Allow all CORS (HF front-end or test script)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Structures for Tasks ---
class StepRequest(BaseModel):
    task: str
    action: str

# Initial observations for each task
TASKS: Dict[str, Dict] = {
    "easy": {"obs": "initial_easy", "done": False},
    "medium": {"obs": "initial_medium", "done": False},
    "hard": {"obs": "initial_hard", "done": False},
}

# --- Root Endpoint ---
@app.get("/")
def root():
    return {"message": "SupportEnv running. Use /reset?task=<task> or POST /step"}

# --- Reset Endpoint ---
@app.get("/reset")
def reset(task: str):
    if task not in TASKS:
        raise HTTPException(status_code=400, detail=f"Unknown task: {task}")
    TASKS[task]["done"] = False
    return {"obs": TASKS[task]["obs"], "task": task}

# --- Step Endpoint ---
@app.post("/step")
def step(req: StepRequest):
    task = req.task
    action = req.action

    if task not in TASKS:
        raise HTTPException(status_code=400, detail=f"Unknown task: {task}")

    if TASKS[task]["done"]:
        return {"obs": TASKS[task]["obs"], "reward": 0, "done": True}

    # Simple mock step logic for scoring
    TASKS[task]["obs"] += f" -> {action}"
    reward = 1  # mock reward
    TASKS[task]["done"] = True
    done = True

    return {"obs": TASKS[task]["obs"], "reward": reward, "done": done}