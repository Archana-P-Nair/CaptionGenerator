# 🖼️ Image Caption Generator using Deep Learning

🚀 A **full-stack Image Caption Generator** that automatically generates meaningful, human-like captions for images using **CNN + LSTM**, wrapped with a **frontend UI**, **backend API**, and **deployed for real-world usage**.
---

## 🌟 Live Deployment

🔗 https://caption-generator-green.vercel.app/

---

## 📌 Project Overview

The goal of this project is to generate **descriptive captions for images** by learning both:
- **visual features** from images, and
- **linguistic patterns** from text data.

🧠 The system:
- Accepts an image upload from the user
- Extracts image features using a pre-trained CNN
- Generates captions **word-by-word** using an LSTM
- Serves predictions through a **backend API**
- Displays results on a **deployed frontend interface**

---

## 🧠 Model Architecture

This project uses a **CNN + RNN (LSTM)** hybrid deep learning architecture.

### 🔹 CNN – Image Feature Extraction
- **Model:** Xception (pre-trained on ImageNet)
- **Input Size:** 299 × 299
- **Output:** 2048-dimensional feature vector

### 🔹 RNN – Caption Generation
- **Embedding Layer:** Converts tokens into dense vectors
- **LSTM Layer:** Captures sequence and context
- **Dense + Softmax:** Predicts next word from vocabulary

📌 Image features and text embeddings are merged to predict captions sequentially.

---

## 🛠️ Tech Stack

### 🧠 Machine Learning
- TensorFlow
- Keras
- CNN (Xception)
- RNN / LSTM
- NumPy, Pandas
- Pickle

### 🌐 Backend
- Python
- FastAPI
- Uvicorn
- TensorFlow Serving Logic
- REST API

### 🎨 Frontend
- Next.js
- React
- Image Upload Interface
- Caption Display UI

### ☁️ Deployment
- **Frontend:** Vercel
- **Backend:** Render (FastAPI)
- **Model:** Loaded at runtime for inference

---
## 🖥️ Application Features

✨ Upload any image  
✨ Generate captions instantly  
✨ Clean & responsive UI  
✨ Backend-powered inference  
✨ Fully deployed and accessible online  

---

## 📁 Project Structure

CaptionGenerator/
│
├── frontend/
│ ├── app/ # Next.js app router pages
│ ├── components/ # Reusable React components
│ ├── public/ # Static assets
│ ├── styles/ # Global and component styles
│ └── package.json # Frontend dependencies
│
├── backend/
│ ├── main.py # FastAPI entry point
│ ├── caption_service.py # Image captioning inference logic
│ ├── utils.py # Helper functions
│ └── requirements.txt # Backend dependencies
│
├── models/
│ └── model_9.h5 # Trained CNN + LSTM model
│
├── tokenizer.p # Saved tokenizer for caption generation
└── README.md # Project documentation

---

## 🚀 Running Locally

### 🔧 Backend
```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```
### 🔧 Frontend
```bash
cd frontend
npm install
npm run dev
Set environment variable: NEXT_PUBLIC_API_URL=http://localhost:8000
```
---
🔮 Future Enhancements

-🔹 Transformer-based captioning models
-🔹 Beam search decoding
-🔹 Multilingual captions
-🔹 Video captioning
-🔹 Performance metrics (BLEU score)


👩‍💻 Author

Archana P Nair
🔗 GitHub: https://github.com/Archana-P-Nair

⭐ If you like this project, don’t forget to star the repo!
