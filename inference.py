import os
from openai import OpenAI

from env.environment import SupportEnv
from env.models import Action
from utils.helpers import parse_action
from tasks.graders import grade_task

# Load tasks
from tasks.easy_ticket import TASK as EASY
from tasks.medium_ticket import TASK as MEDIUM
from tasks.hard_ticket import TASK as HARD


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("API_BASE_URL"),
)

if os.getenv("OPENAI_API_KEY") is None:
    action = Action(action_type="respond", content="Please reset your password using the link")
else:
    # normal model call
    MODEL = os.getenv("MODEL_NAME", "gpt-4o-mini")


def run_task(task_name, task):
    env = SupportEnv(task)
    obs = env.reset()

    print(f"\n--- Running {task_name.upper()} TASK ---")

    for step in range(10):
        try:
            prompt = f"""
You are an AI customer support agent.

Ticket:
{obs.ticket_text}

Conversation History:
{obs.conversation_history}

User Mood: {obs.user_mood}

Choose ONE action:
- classify
- respond
- ask_clarification
- escalate

Respond concisely.
"""

            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
            )

            action_text = response.choices[0].message.content
            action = parse_action(action_text)

        except Exception as e:
            print("Model error:", e)
            action = Action(action_type="respond", content="I'm here to help you.")

        obs, reward, done, info = env.step(action)

        print(f"Step {step+1}")
        print("Action:", action)
        print("Reward:", reward, "| Info:", info)

        if done:
            break

    score = grade_task(env.state)
    print(f"{task_name.upper()} SCORE:", score)

    return score


def main():
    scores = {
        "easy": run_task("easy", EASY),
        "medium": run_task("medium", MEDIUM),
        "hard": run_task("hard", HARD),
    }

    final_score = sum(scores.values()) / len(scores)

    print("\n==============================")
    print("FINAL SCORES:", scores)
    print("FINAL SCORE:", final_score)
    print("==============================")


if __name__ == "__main__":
    main()