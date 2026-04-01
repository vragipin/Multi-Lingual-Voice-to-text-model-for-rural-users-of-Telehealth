# 🏥 Multilingual Telehealth Voice-to-Text System

## 📌 Overview

This project provides **speech-to-text and translation for Indian languages** (Kannada, Hindi, Telugu, Tamil, Malayalam) for rural telehealth applications.

The system converts spoken audio into:

* 📝 Native language transcription
* 🌍 English translation

---

## 🧠 Architecture

```
Android App → FastAPI Backend → Hugging Face Models → Output
```

* 📱 Android App → Records audio
* ⚙️ Backend → Processes audio
* 🤖 Models → Perform ASR + Translation

---

## 🤖 Models (Hosted on Hugging Face)

All models are publicly available on Hugging Face:

* 🔤 Translation Model (IndicTrans2)
  https://huggingface.co/vragipin/translation-model

* 🎤 Transcription Model (IndicConformer)
  https://huggingface.co/vragipin/transcription-model

* 🧠 Whisper Kannada ONNX Model
  https://huggingface.co/vragipin/whisper-kannada-onnx-model

> ⚠️ First run will download ~13GB of models automatically.

---

## 💻 Backend Setup (Local PC)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/vragipin/Multi-Lingual-Voice-to-text-model-for-rural-users-of-Telehealth
cd telehealth_backend
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
venv\scripts\activate   # Windows
```

---

### 3️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run Backend

```bash
python main.py
```

---

## 🌐 Backend Access

### 🔹 Local API

```
http://127.0.0.1:8000
```

### 🔹 Swagger UI (API Testing)

```
http://127.0.0.1:8000/docs
```

👉 You can test transcription directly from browser.

---

## 🌍 Public Access using Ngrok

Run:

```bash
ngrok http 8000 --domain=sacramentally-humeral-shantelle.ngrok-free.dev
```

👉 Your backend will be available at:

```
https://sacramentally-humeral-shantelle.ngrok-free.dev
```

---

## 📱 Android App Usage

1. Install APK (provided in this repo)
2. Open app
3. Record or upload audio 🎤
4. Select language
5. Click **Transcribe**

### ✅ Output:

* Transcription (native language)
* English translation

---

## ⚠️ Important Notes

* First run downloads models (~13GB)
* Requires internet for first run only
* After that → works offline
* Backend runs on:

  ```
  http://127.0.0.1:8000
  ```

---

## 🚀 Features

* Multilingual ASR (Indic languages)
* Real-time translation
* ONNX optimized Whisper model
* Hugging Face model integration
* Android + Backend integration

---


---
