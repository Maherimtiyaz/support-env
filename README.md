# 🧠 SupportEnv: AI Customer Support Simulation Environment

## 🚀 Overview

SupportEnv is a realistic simulation environment designed to evaluate AI agents on customer support tasks.

Agents must:
- Understand user issues
- Classify intent
- Respond appropriately
- Handle emotional context
- Resolve efficiently

---

## 🌍 Real-World Motivation

Customer support automation is critical for:
- Reducing operational costs
- Improving response times
- Enhancing user satisfaction

This environment simulates real-world ticket workflows with multi-step reasoning.

---

## 🎯 Objective

Maximize ticket resolution quality while minimizing steps and handling user emotions correctly.

---

## 🔧 Action Space

| Action | Description |
|------|------------|
| classify | Identify user intent |
| respond | Provide solution |
| ask_clarification | Request more info |
| escalate | Transfer to human |

---

## 👁️ Observation Space

- Ticket text
- Conversation history
- User mood (neutral / angry)
- Current status (open / resolved / escalated)

---

## 🧠 Reward Design

Agents are rewarded for:
- Correct classification
- Providing valid solutions
- Efficient resolution
- Handling emotional users properly

Penalties for:
- Incorrect actions
- Excessive steps
- Poor response tone

---

## 🧪 Tasks

| Difficulty | Description |
|----------|------------|
| Easy | Simple intent detection |
| Medium | Requires reasoning |
| Hard | Multi-condition + emotional handling |

---

## ⚙️ Setup

```bash
pip install -r requirements.txt