# Image Caption Generator

Generate captions for images using a trained Xception + LSTM model. This repo includes the training script, a FastAPI backend, and a dark-themed Next.js frontend.

## Quick start (local)

### 1. Backend (from project root)

```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Requires `tokenizer.p` and `models/model_9.h5` in the project root (from training).

### 2. Frontend

```bash
cd frontend
cp .env.example .env.local
# Edit .env.local if your backend is not at http://localhost:8000
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000), upload an image, and click **Generate caption**.

## Deploy on Vercel

- **Frontend**: Deploy the `frontend` folder on [Vercel](https://vercel.com). Set **Root Directory** to `frontend` and add `NEXT_PUBLIC_API_URL` to your backend URL.
- **Backend**: Run the FastAPI app on Railway, Render, or another host (see [DEPLOYMENT.md](DEPLOYMENT.md)).

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for step-by-step Vercel and backend deployment.
