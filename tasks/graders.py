def grade_task(state):
    score = 0.0

    # 1. Resolution
    if state.status == "resolved" and state.solution.lower() in " ".join(state.history).lower():
        score += 0.5

    # 2. Correct classification
    if state.classified:
        score += 0.2

    # 3. Efficiency
    if state.steps <= 5:
        score += 0.2
    elif state.steps <= 8:
        score += 0.1

    # 4. Avoid escalation
    if state.status == "escalated":
        score -= 0.2

    return max(0.0, min(1.0, score))