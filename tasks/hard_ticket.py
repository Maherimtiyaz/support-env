import json

with open("data/tickets.json") as f:
    TASKS = json.load(f)

TASK = TASKS[0]