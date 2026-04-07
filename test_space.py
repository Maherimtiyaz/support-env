import requests

# Your HF Space URL (replace with your actual HF Space link)
BASE_URL = "https://huggingface.co/spaces/madameM/support-env/reset"

# List of tasks
TASKS = ["easy", "medium", "hard"]

def reset_env(task_name):
    """
    Resets the environment for a given task.
    """
    url = f"{BASE_URL}/reset?task={task_name}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Reset failed for {task_name}: {response.text}")
    return response.json()


def step_env(action_type, content):
    """
    Sends a step/action to the environment.
    """
    url = f"{BASE_URL}/step"
    payload = {"action_type": action_type, "content": content}
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise Exception(f"Step failed: {response.text}")
    return response.json()


def run_task(task_name):
    """
    Run a full task loop for testing purposes.
    """
    print(f"\n--- Running {task_name} task ---")
    obs = reset_env(task_name)
    print("Initial Observation:", obs)

    total_reward = 0.0
    done = False
    step_count = 0

    # Simulated actions for testing (modify if you want smarter logic)
    while not done and step_count < 10:
        step_count += 1
        if "password" in obs["ticket_text"].lower():
            action = step_env("classify", "password_reset")
        elif "charge" in obs["ticket_text"].lower():
            action = step_env("classify", "billing_issue")
        else:
            action = step_env("classify", "technical_bug")

        # Simulate a response action
        response_text = "Simulated response for testing"
        action = step_env("respond", response_text)
        total_reward += action.get("reward", 0.0)
        done = action.get("done", False)
        obs = action.get("observation", obs)

    print(f"Final Observation: {obs}")
    print(f"Total Reward for {task_name}: {total_reward:.2f}")


def main():
    for task in TASKS:
        run_task(task)
    print("\n✅ All tasks tested successfully!")


if __name__ == "__main__":
    main()