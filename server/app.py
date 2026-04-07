from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
import gradio as gr
from inference import run_task

def main():
    iface = gr.Interface(fn=run_task, inputs="text", outputs="text")
    iface.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    main()
    
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ENVIRONMENTS = {
    "easy": {"state": 0},
    "medium": {"state": 0},
    "hard": {"state": 0},
}

@app.get("/")
def root():
    return {"message": "SupportEnv running"}

@app.get("/reset")
@app.post("/reset")
def reset(task: str = "easy"):
    if task not in ENVIRONMENTS:
        raise HTTPException(status_code=404, detail="Task not found")

    ENVIRONMENTS[task]["state"] = 0

    return {
        "observation": f"Task {task} reset.",
        "reward": 0,
        "done": False
    }

@app.post("/step")
def step(data: dict = Body(...)):
    task = data.get("task", "easy")
    action = data.get("action", "")

    if task not in ENVIRONMENTS:
        raise HTTPException(status_code=404, detail="Task not found")

    ENVIRONMENTS[task]["state"] += 1

    done = ENVIRONMENTS[task]["state"] >= 5
    reward = 1 if not done else 10

    return {
        "observation": f"Step {ENVIRONMENTS[task]['state']} in {task}",
        "reward": reward,
        "done": done
    }