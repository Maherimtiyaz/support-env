# app.py
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

app = FastAPI(title="SupportEnv API")

# Allow requests from any frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy environments for tasks
ENVIRONMENTS = {
    "easy": {"state": 0},
    "medium": {"state": 0},
    "hard": {"state": 0},
}

@app.get("/reset")
def reset(task: str = Query(..., description="Task to reset: easy/medium/hard")):
    if task not in ENVIRONMENTS:
        raise HTTPException(status_code=404, detail="Task not found")
    ENVIRONMENTS[task]["state"] = 0
    return {"observation": f"Task {task} reset.", "reward": 0, "done": False}

@app.post("/step")
def step(task: str = Query(..., description="Task name: easy/medium/hard"),
         action: Optional[str] = Query(None, description="Action to take")):
    if task not in ENVIRONMENTS:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Increment dummy state
    ENVIRONMENTS[task]["state"] += 1
    done = ENVIRONMENTS[task]["state"] >= 5
    reward = 1 if not done else 10

    return {
        "observation": f"Step {ENVIRONMENTS[task]['state']} in {task}",
        "reward": reward,
        "done": done
    }

@app.get("/")
def root():
    return {"message": "SupportEnv running. Use /reset?task=... or /step"}