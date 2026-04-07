class SupportState:

    def __init__(self, task):
        # Core ticket info
        self.ticket_text = task["ticket"]
        self.expected_intent = task["intent"]
        self.solution = task["solution"]

        # Conversation tracking
        self.history = []

        # Status tracking
        self.status = "open"  # open / resolved / escalated
        self.steps = 0

        # Decision tracking
        self.classified = False

        # Extra realism (important for scoring)
        self.user_mood = task.get("user_mood", "neutral")

    def apply_action(self, action):
        self.steps += 1

        if action.action_type == "classify":
            if action.content == self.expected_intent:
                self.classified = True

        elif action.action_type == "respond":
            if action.content:
                self.history.append(action.content)

                # Check if solution is given
                if self.solution.lower() in action.content.lower():
                    self.status = "resolved"

        elif action.action_type == "ask_clarification":
            self.history.append("Agent asked for clarification")

        elif action.action_type == "escalate":
            self.status = "escalated"

        else:
            raise ValueError("Invalid action type")