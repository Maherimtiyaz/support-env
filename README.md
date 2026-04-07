---
title: SupportEnv – AI Customer Support Simulator
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: '1.0'
app_file: app.py
pinned: false
---

# 🧠 SupportEnv: AI Customer Support Simulation Environment

## 🚀 Overview
SupportEnv is an AI-powered environment for simulating customer support tasks.  
It allows testing agents on **three difficulty levels**: `easy`, `medium`, and `hard`.  
Built with **FastAPI + Docker**, fully reproducible, and hackathon-ready.  

## ⚡ Endpoints

Your Space exposes the following endpoints:

### 1️⃣ Reset Environment

**Example:**  
```bash
curl -X GET "https://huggingface.co/spaces/madameM/support-env/resolve/reset?task=easy"