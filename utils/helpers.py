from env.models import Action


def parse_action(text: str) -> Action:
    text = text.lower()

    if "classify" in text:
        if "password" in text:
            return Action(action_type="classify", content="password_reset")
        elif "charge" in text or "billing" in text:
            return Action(action_type="classify", content="billing_issue")
        elif "bug" in text or "crash" in text:
            return Action(action_type="classify", content="technical_bug")

    elif "escalate" in text:
        return Action(action_type="escalate")

    elif "clarification" in text:
        return Action(action_type="ask_clarification")

    else:
        return Action(action_type="respond", content=text)