# Image Caption Generator – Deployment Guide

## Overview

- **Frontend**: Next.js app (dark theme). Deploy on **Vercel**.
- **Backend**: FastAPI server that runs the caption model. Deploy on **Railway**, **Render**, or run locally.

The frontend calls the backend at the URL set in `NEXT_PUBLIC_API_URL`.

---

## 1. Deploy frontend on Vercel

### Option A: Deploy only the frontend (recommended)

1. Push your code to GitHub (ensure `frontend/`, `backend/`, `models/`, `tokenizer.p` are in the repo if you want backend elsewhere from same repo).

2. Go to [vercel.com](https://vercel.com) → **Add New Project** → Import your repository.

3. Set **Root Directory** to `frontend`:
   - Project Settings → General → Root Directory → `frontend` → Save.

4. Add environment variable:
   - Project Settings → Environment Variables
   - Name: `NEXT_PUBLIC_API_URL`
   - Value: your backend URL (e.g. `https://your-backend.up.railway.app` or `https://your-app.onrender.com`)

5. Deploy. Vercel will run `npm install` and `npm run build` in the `frontend` folder.

### Option B: Deploy from repo root with root set to frontend

- In Vercel project settings, set **Root Directory** to `frontend`. No need for a root `vercel.json` if you do that.

---

## 2. Run the backend (required for captions)

The frontend needs the backend API to generate captions. The backend uses TensorFlow and the saved model files (`models/`, `tokenizer.p`).

### Local (development)

From the **project root** (not inside `backend/`):

```bash
# Create and activate a virtual environment, then:
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Ensure `tokenizer.p` and `models/model_9.h5` exist in the project root. Frontend: set `NEXT_PUBLIC_API_URL=http://localhost:8000` in `frontend/.env.local`.

### Production (Railway / Render / similar)

1. **Include in deployment**:
   - `backend/` (code)
   - `tokenizer.p` (project root)
   - `models/` (e.g. `model_9.h5`) at project root so `backend/caption_service.py` can find them.

2. **Railway**
   - New Project → Deploy from GitHub.
   - Root directory: leave as repo root (so `tokenizer.p` and `models/` are present).
   - Start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - Add `requirements.txt` at repo root that includes `backend/requirements.txt` content, or run `pip install -r backend/requirements.txt` in build.
   - Set the public URL as `NEXT_PUBLIC_API_URL` in Vercel (frontend).

3. **Render**
   - New Web Service → connect repo.
   - Build: `pip install -r backend/requirements.txt` (from root so `backend/` is available).
   - Start: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`.
   - Use the Render service URL as `NEXT_PUBLIC_API_URL` in Vercel.

---

## 3. CORS

The backend allows all origins (`allow_origins=["*"]`). For production you can restrict this to your Vercel frontend URL in `backend/main.py` if you prefer.

---

## 4. Quick checklist

- [ ] Backend running and reachable at a public URL (or localhost for dev).
- [ ] Frontend `NEXT_PUBLIC_API_URL` points to that URL.
- [ ] Vercel project root set to `frontend`.
- [ ] `tokenizer.p` and `models/model_9.h5` available in the environment where the backend runs.
