import os
from dotenv import load_dotenv

# Safe import of OpenAI
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

# Load env variables (safe)
load_dotenv()

# Safe config
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("API_BASE_URL")
MODEL = os.getenv("MODEL_NAME", "gpt-4o-mini")

# Initialize client safely
client = None
if OpenAI and api_key:
    try:
        client = OpenAI(api_key=api_key, base_url=base_url)
    except Exception:
        client = None


def safe_fallback_action():
    """Fallback action when model is unavailable"""
    return Action(
        action_type="respond",
        content="I'm here to help you. Could you please provide more details?"
    )


def run_task(task_name, task):
    try:
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

            except Exception as e:
                print("Model error:", e)
                action = safe_fallback_action()

            try:
                obs, reward, done, info = env.step(action)
            except Exception as e:
                print("Env step error:", e)
                break

            print(f"Step {step+1}")
            print("Action:", action)
            print("Reward:", reward, "| Info:", info)

            if done:
                break

        try:
            score = grade_task(env.state)
        except Exception:
            score = 0

        print(f"{task_name.upper()} SCORE:", score)

        return score

    except Exception as e:
        print(f"Task {task_name} failed:", e)
        return 0


def main():
    try:
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

    except Exception as e:
        print("Fatal error in main:", e)


if __name__ == "__main__":
    main()