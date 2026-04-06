# DocSense AI — Setup Guide

## Prerequisites
- Python 3.10+ installed
- Node.js 18+ installed
- Free Gemini API key from aistudio.google.com

---

## STEP 1 — Get Free Gemini API Key
1. Go to → https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

---

## STEP 2 — Add API Key
Open `backend/.env` → replace:
```
GEMINI_API_KEY=paste_your_free_key_here
```
With your actual key.

---

## STEP 3 — Backend Setup
Open Terminal 1:
```bash
cd docsense-ai/backend
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
pip install google-genai
```

---

## STEP 4 — Run Backend
```bash
python main.py
```
Backend → http://localhost:8000

Test → http://localhost:8000/api/health
Should show → {"status":"healthy","app":"DocSense AI"}

---

## STEP 5 — Frontend Setup
Open Terminal 2:
```bash
cd docsense-ai/frontend
npm install
npm run dev
```
Frontend → http://localhost:5173

---

## STEP 6 — Use DocSense AI
1. Open browser → http://localhost:5173
2. Drop any document in the upload zone
3. Wait for AI analysis
4. See extracted data instantly

---

## Every Time You Start
Terminal 1 (Backend):
```bash
cd docsense-ai/backend
.\venv\Scripts\Activate
python main.py
```

Terminal 2 (Frontend):
```bash
cd docsense-ai/frontend
npm run dev
```

---

## Troubleshooting
| Problem | Fix |
|---------|-----|
| Backend not starting | Check venv is activated |
| Gemini error | Check API key in .env |
| Frontend blank | Run npm install first |
| Port in use | Change port in main.py |