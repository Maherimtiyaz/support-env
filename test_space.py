import requests

# ✅ Replace this with your actual Space API host
BASE_URL = "https://huggingface.co/spaces/madameM/support-env"



# The three tasks
TASKS = ["easy", "medium", "hard"]

def reset_env(task_name):
    """Call the /reset endpoint for a task"""
    url = f"{BASE_URL}/reset?task={task_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Error resetting {task_name} task: {e}")
        return None

def step_env(action):
    """Call the /step endpoint with an action"""
    url = f"{BASE_URL}/step"
    try:
        response = requests.post(url, json={"action": action})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Error during step: {e}")
        return None

def run_task(task_name):
    print(f"\n--- Running {task_name} task ---")
    obs = reset_env(task_name)
    if obs is None:
        print(f"Skipping {task_name} due to reset error.")
        return

    # Dummy random action loop (you can replace with your agent)
    total_reward = 0
    for i in range(3):  # run 3 steps for testing
        action = "default_action"  # replace with real action if needed
        result = step_env(action)
        if result is None:
            break
        print(f"Step {i+1}: {result}")
        total_reward += result.get("reward", 0)

    print(f"Total reward for {task_name}: {total_reward}")

def main():
    for task in TASKS:
        run_task(task)

if __name__ == "__main__":
    main()