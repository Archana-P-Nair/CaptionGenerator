# 🖼️ Image Caption Generator using Deep Learning

🚀 A full-stack **Image Caption Generator** that automatically generates meaningful captions for images using **CNN + LSTM** architecture, wrapped with a **frontend UI**, **backend API**, and **deployed for real-world usage**.

This project combines **Computer Vision**, **Natural Language Processing**, and **Web Development**, making it a strong end-to-end ML application.

---

## 🌟 Live Demo
🔗 **Deployed Application:** *(Add your deployed URL here)*  
📦 **GitHub Repository:** https://github.com/Archana-P-Nair/CaptionGenerator

---

## 📌 Project Overview

The goal of this project is to generate **human-like captions** for images by learning visual features and linguistic patterns.

🔍 The system:
- Takes an image as input
- Extracts visual features using a pre-trained CNN
- Generates captions **word-by-word** using an LSTM
- Serves predictions through a **backend API**
- Displays results via a **frontend interface**

---

## 🧠 Model Architecture

🧩 The model is built using a **CNN + RNN (LSTM)** hybrid approach:

### 🔹 CNN – Image Feature Extraction
- **Model:** Xception (pre-trained on ImageNet)
- **Output:** 2048-dimensional feature vector
- **Why Xception?**
  - Strong feature extraction
  - Faster convergence using transfer learning

### 🔹 RNN – Caption Generation
- **Embedding Layer:** Converts word indices into dense vectors
- **LSTM:** Captures sequence context
- **Softmax Layer:** Predicts the next word in the caption

📌 Image features and text embeddings are merged to predict captions sequentially.

---

## 📂 Dataset

📦 **Flickr8K Dataset**
- ~8,000 images
- 5 captions per image
- ~8,763 unique words

🔧 Preprocessing includes:
- Lowercasing text
- Removing punctuation & numbers
- Adding `<start>` and `<end>` tokens
- Tokenization & padding

---

## 🔄 Workflow

1️⃣ Load and preprocess captions  
2️⃣ Extract image features using Xception  
3️⃣ Tokenize and pad caption sequences  
4️⃣ Train CNN + LSTM model using a data generator  
5️⃣ Save model checkpoints  
6️⃣ Generate captions iteratively during inference  
7️⃣ Serve predictions via backend  
8️⃣ Display results on frontend UI  

---

## 🛠️ Tech Stack

### 🧠 Machine Learning
- TensorFlow / Keras
- CNN (Xception)
- RNN / LSTM
- NumPy, Pandas
- Pickle (feature storage)

### 🌐 Backend
- Python
- Flask / FastAPI *(whichever you used)*
- REST API for inference

### 🎨 Frontend
- HTML / CSS / JavaScript *(or React, if used)*
- Image upload interface
- Caption display

### ☁️ Deployment
- Model served via backend API
- Frontend + backend deployed *(platform: Render / Vercel / AWS / Heroku etc.)*

---

## 📊 Model Configuration

| Component                  | Value |
|---------------------------|------|
| Dataset                   | Flickr8K |
| CNN Model                 | Xception |
| Image Size                | 299 × 299 |
| Feature Vector Size       | 2048 |
| Embedding Dimension       | 256 |
| LSTM Units                | 256 |
| Loss Function             | Categorical Crossentropy |
| Optimizer                 | Adam |
| Batch Size                | 32 |
| Caption Generation        | Word-by-word |

---

## 🧪 Caption Generation Logic

🧠 Caption generation follows this loop:

- Start with `<start>` token
- Predict next word using model
- Append predicted word
- Repeat until `<end>` token or max length

📌 This ensures grammatically coherent captions.

---

## 🖥️ Application Features

✨ Upload any image  
✨ Generate captions instantly  
✨ Clean & interactive UI  
✨ Backend-powered inference  
✨ Deployed and accessible online  

---

## 📁 Project Structure

