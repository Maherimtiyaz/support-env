def compute_reward(state, action, error):

    if error:
        return {"value": -0.3, "reason": "invalid_action"}

    reward = 0.0
    reason = []

    # discourage repeated responses
    if len(state.history) >= 2 and action.action_type == "respond":
        if action.content in state.history:
            reward -= 0.2
            reason.append("repeated_response")

    # classification reward
    if action.action_type == "classify":
        if state.classified:
            reward += 0.4
            reason.append("correct_classification")
        else:
            reward -= 0.1
            reason.append("wrong_classification")

    # response quality
    if action.action_type == "respond":
        if action.content and len(action.content.split()) > 5:
            reward += 0.15
        else:
            reward -= 0.1
            reason.append("low_quality_response")

        if state.status == "resolved":
            reward += 0.7
            reason.append("resolved")

    # escalation penalty
    if action.action_type == "escalate":
        reward -= 0.25
        reason.append("unnecessary_escalation")

    # emotional intelligence (killer feature 🔥)
    if action.action_type == "respond" and state.user_mood == "angry":
        if state.user_mood == "angry" and action.action_type == "respond":
            if any(word in action.content.lower() for word in ["sorry", "apologize", "understand"]):
               reward += 0.2
               reason.append("handled_angry_user_well")
        else:
            reward -= 0.2
            reason.append("no_empathy")

    # step penalty (efficiency)
    reward -= 0.02 * state.steps

    return {"value": reward, "reason": ",".join(reason)}