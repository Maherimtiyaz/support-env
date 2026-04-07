import requests

BASE_URL = "https://huggingface.co/spaces/madameM/support-env/api"
TASKS = ["easy", "medium", "hard"]

def reset_env(task_name):
    url = f"{BASE_URL}/reset?task={task_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error resetting {task_name} task: {e}")
        return None

def step_env(task_name, action):
    url = f"{BASE_URL}/step"
    payload = {"task": task_name, "action": action}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error stepping {task_name} task: {e}")
        return None

def run_task(task_name):
    print(f"\n--- Running {task_name} task ---")
    obs = reset_env(task_name)
    if not obs:
        print(f"Skipping {task_name} due to reset error.")
        return

    print(f"Initial observation: {obs}")

    # Example loop of 3 steps
    for i in range(3):
        action = f"action_{i+1}"
        result = step_env(task_name, action)
        if not result:
            print(f"Step {i+1} failed.")
            break
        print(f"Step {i+1} result: {result}")

def main():
    for task in TASKS:
        run_task(task)

if __name__ == "__main__":
    main()