# 🏥 Multi-Lingual-Voice-to-text-model-for-rural-users-of-Telehealth

---

## 📌 Overview

This project presents a **multilingual speech-to-text and translation system** designed specifically for rural telehealth applications.

The system enables users to:

* 🎤 Speak in their native language
* 📝 Receive accurate transcription
* 🌍 Obtain English translation

### 🌐 Supported Languages

* Kannada
* Hindi
* Telugu
* Tamil
* Malayalam

---

## 🧠 System Architecture

```id="pzt69x"
Android App → FastAPI Backend → Hugging Face Models → Output
```

### 🔧 Components

* 📱 **Android Application**

  * Records or uploads audio
  * Sends audio data to backend server

* ⚙️ **Backend (FastAPI)**

  * Handles API requests
  * Processes audio input
  * Integrates ML models for inference

* 🤖 **Machine Learning Models (Hugging Face)**

  * ASR (Speech-to-Text)
  * Translation (Indian Languages → English)

---

## 🤖 Models (Hosted on Hugging Face)

The models are hosted on Hugging Face and loaded dynamically at runtime:

* 🔤 **Translation Model (IndicTrans2)**
  https://huggingface.co/vragipin/translation-model

* 🎤 **Transcription Model (IndicConformer)**
  https://huggingface.co/vragipin/transcription-model

* 🧠 **Whisper Kannada ONNX Model**
  https://huggingface.co/vragipin/whisper-kannada-onnx-model

> ⚠️ During the first execution, approximately **13GB of model data** will be downloaded automatically.
> Afterward, models are cached locally and reused.

---

# 💻 Backend Setup (Step-by-Step)

---

## 1️⃣ Clone the Repository

```bash id="tweyf3"
git clone https://github.com/vragipin/Multi-Lingual-Voice-to-text-model-for-rural-users-of-Telehealth
cd telehealth_backend
```

---

## 2️⃣ Create Virtual Environment

```bash id="nqruzy"
python -m venv venv
```

### Activate Environment (Windows)

```bash id="21840i"
venv\scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash id="86is02"
pip install -r requirements.txt
```

---

## 4️⃣ Run Backend Server

```bash id="yzq55z"
python main.py
```

---

## 5️⃣ Backend Running Location

```id="wz8sqi"
http://127.0.0.1:8000
```

---

## 6️⃣ Swagger UI (API Testing)

```id="58hw0r"
http://127.0.0.1:8000/docs
```

---

# 🌍 Public Access using Ngrok

---

## 7️⃣ Start Ngrok

```bash id="3b0xyw"
ngrok http 8000 --domain=sacramentally-humeral-shantelle.ngrok-free.dev
```

---

## 8️⃣ Public Backend URL

```id="t790g9"
https://sacramentally-humeral-shantelle.ngrok-free.dev
```

---

# 📱 Android Application Usage

---

## 🔽 Install APK

```id="yq5eed"
app.apk
```

---

## 📲 Steps to Use

1. Open the application
2. Select preferred language
3. Choose model:

   * **Indic Model** → Supports all languages
   * **Whisper Model** → Supports Kannada only
4. Record or upload audio
5. Click **Transcribe**

---

## ✅ Output

* 📝 Native language transcription
* 🌍 English translation

---

# ⚠️ Important Notes

* First run downloads ~13GB models
* Takes 10–20 minutes
* Works offline after first run
* Backend + ngrok must be running

---

# 🚀 Features

* Multilingual speech recognition
* Real-time translation
* Hugging Face integration
* ONNX optimized inference
* Android + Backend integration

---

# 🧪 Testing Workflow

1. Run backend
2. Start ngrok
3. Open Swagger UI
4. Use Android app
5. Get results

---

# 👨‍💻 Authors

* **Dr. Viswa Bharathy A. M (Project Guide)**
* **Vishnuvardhan Reddy**
* **Bharath Kumar**
* **Varshith**
* **Masineni Kowshik**

---
