from pydantic import BaseModel
from typing import List, Optional


class Observation(BaseModel):
    ticket_text: str
    conversation_history: List[str]
    last_action_error: bool
    status: str  # open / resolved / escalated
    user_mood: str  # neutral / angry


class Action(BaseModel):
    action_type: str  
    # classify / respond / ask_clarification / escalate

    content: Optional[str] = None


class Reward(BaseModel):
    value: float
    reason: str