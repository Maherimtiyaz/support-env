from fastapi import FastAPI
from env.environment import SupportEnv
from env.models import Action
from tasks.easy_ticket import TASK

app = FastAPI()

env = SupportEnv(TASK)


@app.get("/reset")
def reset():
    obs = env.reset()
    return obs.dict()


@app.post("/step")
def step(action: dict):
    act = Action(**action)
    obs, reward, done, info = env.step(act)

    return {
        "observation": obs.dict(),
        "reward": reward,
        "done": done,
        "info": info
    }