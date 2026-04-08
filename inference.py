import os
from dotenv import load_dotenv

# Safe import
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

from env.environment import SupportEnv
from env.models import Action
from utils.helpers import parse_action
from tasks.graders import grade_task

# Load tasks
from tasks.easy_ticket import TASK as EASY
from tasks.medium_ticket import TASK as MEDIUM
from tasks.hard_ticket import TASK as HARD

# Load environment variables
load_dotenv()

api_key = os.getenv("API_KEY")
base_url = os.getenv("API_BASE_URL")
MODEL = os.getenv("MODEL_NAME", "gpt-4o-mini")

# Safe client initialization
client = None
if OpenAI and api_key:
    try:
        client = OpenAI(api_key=api_key, base_url=base_url)
    except Exception:
        client = None


def safe_fallback_action():
    return Action(
        action_type="respond",
        content="I'm here to help you. Could you please provide more details?"
    )


def run_task(task_name, task):
    try:
        env = SupportEnv(task)
        obs = env.reset()

        print(f"[START] task={task_name}", flush=True)

        steps_taken = 0

        for step in range(10):
            steps_taken += 1

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

                if client is None:
                    action = safe_fallback_action()
                else:
                    response = client.chat.completions.create(
                        model=MODEL,
                        messages=[{"role": "user", "content": prompt}],
                    )

                    action_text = response.choices[0].message.content

                    try:
                        action = parse_action(action_text)
                    except Exception:
                        action = safe_fallback_action()

            except Exception:
                action = safe_fallback_action()

            try:
                obs, reward, done, info = env.step(action)
            except Exception:
                break

            # REQUIRED structured output
            print(f"[STEP] step={steps_taken} reward={reward}", flush=True)

            if done:
                break

        try:
            score = grade_task(env.state)
        except Exception:
            score = 0

        print(f"[END] task={task_name} score={score} steps={steps_taken}", flush=True)

        return score

    except Exception:
        print(f"[END] task={task_name} score=0 steps=0", flush=True)
        return 0


def main():
    try:
        scores = {
            "easy": run_task("easy", EASY),
            "medium": run_task("medium", MEDIUM),
            "hard": run_task("hard", HARD),
        }

        final_score = sum(scores.values()) / len(scores)

        print(f"[FINAL] score={final_score}", flush=True)

    except Exception:
        print("[FINAL] score=0", flush=True)


if __name__ == "__main__":
    main()