# 🏥 Multilingual Telehealth Voice-to-Text System

---

## 📌 Overview

This project provides a **complete speech-to-text and translation system for Indian languages** designed for rural telehealth applications.

It enables users to:

* 🎤 Speak in native language
* 📝 Get transcription
* 🌍 Get English translation

Supported Languages:

* Kannada
* Hindi
* Telugu
* Tamil
* Malayalam

---

## 🧠 System Architecture

```
Android App → FastAPI Backend → Hugging Face Models → Output
```

### Components:

* 📱 **Android App**

  * Records or uploads audio
  * Sends request to backend

* ⚙️ **Backend (FastAPI)**

  * Handles API requests
  * Processes audio
  * Calls ML models

* 🤖 **Models (Hugging Face)**

  * ASR (Speech-to-Text)
  * Translation (Indian → English)

---

## 🤖 Models (Hosted on Hugging Face)

All models are hosted and loaded dynamically:

* 🔤 Translation Model (IndicTrans2)
  https://huggingface.co/vragipin/translation-model

* 🎤 Transcription Model (IndicConformer)
  https://huggingface.co/vragipin/transcription-model

* 🧠 Whisper Kannada ONNX Model
  https://huggingface.co/vragipin/whisper-kannada-onnx-model

> ⚠️ First run will automatically download ~13GB of models
> After that → models are cached locally (no re-download)

---

# 💻 Backend Setup (Step-by-Step)

---

## 1️⃣ Clone Repository

```bash
git clone https://github.com/vragipin/Multi-Lingual-Voice-to-text-model-for-rural-users-of-Telehealth
cd telehealth_backend
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows:

```bash
venv\scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Run Backend Server

```bash
python main.py
```

---

## 5️⃣ Backend Running Location

Once started, backend runs at:

```
http://127.0.0.1:8000
```

---

## 6️⃣ Swagger UI (Testing API)

Open in browser:

```
http://127.0.0.1:8000/docs
```

👉 You can upload audio and test API directly

---

# 🌍 Public Access using Ngrok

---

## 7️⃣ Start Ngrok

```bash
ngrok http 8000 --domain=sacramentally-humeral-shantelle.ngrok-free.dev
```

---

## 8️⃣ Public Backend URL

```
https://sacramentally-humeral-shantelle.ngrok-free.dev
```

👉 This is used by Android app

---

# 📱 Android App Usage

---

## 🔽 Install APK

Download from this repository:

```
app.apk
```

Install it on your Android device.

---

## 📲 Steps to Use

1. Open the app

2. Select language:

   * Kannada / Hindi / Telugu / Tamil / Malayalam

3. Select model:

   * **Indic** → supports all languages
   * **Whisper** → supports Kannada only

4. Choose input method:

   * 🎤 Record audio
   * 📂 Upload audio file

5. Click **Upload / Transcribe**

---

## ✅ Output

The app will display:

* 📝 Native language transcription
* 🌍 English translation

---

# ⚠️ Important Notes

* First run:

  * Downloads ~13GB models
  * Takes 10–20 minutes

* After first run:

  * Works offline
  * Faster execution

* Backend must be running before using app

* Ngrok must be active for mobile access

---

# 🚀 Features

* Multilingual speech recognition
* Real-time translation
* Hugging Face model integration
* ONNX optimized Whisper model
* Android + Backend integration
* Works offline after initial setup

---

# 🧪 Testing Flow

1. Run backend
2. Start ngrok
3. Open Swagger → test API
4. Open Android app
5. Record speech
6. Get results


# 👨‍💻 Author

**Vishnuvardhan Reddy**
**Bharath Kumar**
**Varshith**
**Masineni Kowshik**
Final Year Project – Multilingual Telehealth AI System

Under the guidance of :-
**Dr. Viswa Bharathy A. M 
Assistant Professor**

---
