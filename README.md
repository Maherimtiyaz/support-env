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
curl -X GET "http://localhost:8000/reset?task=easy"
```

## 🧪 Running Tests Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the local server:
   ```bash
   uvicorn app:app --reload
   ```

3. In another terminal, run the test script:
   ```bash
   python test_space.py
   ```

Note: If you run the API on a different port, update `BASE_URL` in `test_space.py`.