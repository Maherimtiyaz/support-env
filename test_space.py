# test_space.py
import requests

# Set this to your HF Space URL
BASE_URL = "https://madameM-hf-space-support-env.hf.space"

TASKS = ["easy", "medium", "hard"]

def reset_env(task):
    url = f"{BASE_URL}/reset"
    params = {"task": task}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def step_env(task, action="default_action"):
    url = f"{BASE_URL}/step"
    params = {"task": task, "action": action}
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()

def run_task(task):
    print(f"\n--- Running {task} task ---")
    try:
        obs = reset_env(task)
        print("Initial observation:", obs)
    except requests.HTTPError as e:
        print(f"Error resetting {task} task:", e)
        return

    done = False
    step_num = 0
    while not done:
        step_num += 1
        try:
            step_resp = step_env(task)
            print(f"Step {step_num}:", step_resp)
            done = step_resp.get("done", False)
        except requests.HTTPError as e:
            print(f"Error stepping {task} task:", e)
            break

def main():
    for task in TASKS:
        run_task(task)

if __name__ == "__main__":
    main()