from env.state import SupportState
from env.reward import compute_reward
from env.models import Observation, Action


class SupportEnv:

    def __init__(self, task):
        self.task = task
        self.state = None
        self.max_steps = 10

    def reset(self):
        self.state = SupportState(self.task)
        return self._get_observation()

    def step(self, action: Action):
        done = False
        error = False

        try:
            self.state.apply_action(action)
        except Exception:
            error = True

        reward = compute_reward(self.state, action, error)

        # Termination conditions
        if self.state.status in ["resolved", "escalated"]:
            done = True

        if self.state.steps >= self.max_steps:
            done = True
            reward["value"] -= 0.5  # penalty for inefficiency

        obs = self._get_observation(error)

        return obs, reward["value"], done, {"reason": reward["reason"]}

    def state(self):
        return self.state

    def _get_observation(self, error=False):
        return Observation(
            ticket_text=self.state.ticket_text,
            conversation_history=self.state.history,
            last_action_error=error,
            status=self.state.status,
            user_mood=self.state.user_mood
        )