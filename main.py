# ============================================================
# TELEHEALTH MULTILINGUAL ASR BACKEND (HF UPDATED VERSION)
# ============================================================

import os
os.environ["TRANSFORMERS_NO_ONNX"] = "1"
os.environ["ORT_DISABLE_ARENA"] = "1"
os.environ["HF_HOME"] = "/tmp/hf_cache"   # ✅ IMPORTANT FOR RENDER

import tempfile
import shutil
import zipfile
import urllib.request

import torch
import librosa
import numpy as np
import onnxruntime as ort

from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from transformers import (
    WhisperProcessor,
    AutoModel,
    AutoConfig,
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)

from huggingface_hub import hf_hub_download   # ✅ NEW
from IndicTransToolkit.processor import IndicProcessor
from pydub import AudioSegment

# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# AUTO DOWNLOAD FFMPEG (UNCHANGED)
# ============================================================

FFMPEG_DIR = os.path.join(BASE_DIR, "ffmpeg")
FFMPEG_BIN = os.path.join(FFMPEG_DIR, "bin", "ffmpeg.exe")
FFPROBE_BIN = os.path.join(FFMPEG_DIR, "bin", "ffprobe.exe")


def ensure_ffmpeg():
    if os.path.exists(FFMPEG_BIN) and os.path.exists(FFPROBE_BIN):
        return True

    print("Downloading FFmpeg...")

    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = os.path.join(BASE_DIR, "ffmpeg.zip")

    urllib.request.urlretrieve(url, zip_path)

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(BASE_DIR)

    extracted = next(
        d for d in os.listdir(BASE_DIR)
        if d.startswith("ffmpeg") and "essentials" in d
    )

    shutil.move(os.path.join(BASE_DIR, extracted), FFMPEG_DIR)

    os.remove(zip_path)

    return True


FFMPEG_AVAILABLE = ensure_ffmpeg()

os.environ["PATH"] = os.path.join(FFMPEG_DIR, "bin") + os.pathsep + os.environ["PATH"]

# ============================================================
# 🔥 REPLACE LOCAL PATHS WITH HF REPOS
# ============================================================

INDICTRANS2_REPO = "vragipin/translation-model"
INDIC_CONFORMER_REPO = "vragipin/transcription-model"
WHISPER_REPO = "vragipin/whisper-kannada-onnx-model"

# ============================================================
# DEVICE CONFIG
# ============================================================

ASR_DEVICE = "cpu"
MT_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

USE_WHISPER_GPU = torch.cuda.is_available()

# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(title="Telehealth ASR API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# LOAD INDIC TRANS2 (FROM HF)
# ============================================================

print("Loading IndicTrans2...")

mt_tokenizer = AutoTokenizer.from_pretrained(
    INDICTRANS2_REPO,
    trust_remote_code=True
)

mt_model = AutoModelForSeq2SeqLM.from_pretrained(
    INDICTRANS2_REPO,
    trust_remote_code=True
).to(MT_DEVICE).eval()

mt_processor = IndicProcessor(inference=True)

print("IndicTrans2 loaded")

# ============================================================
# LOAD INDIC CONFORMER (FROM HF)
# ============================================================

print("Loading IndicConformer...")

asr_config = AutoConfig.from_pretrained(
    INDIC_CONFORMER_REPO,
    trust_remote_code=True
)

asr_model = AutoModel.from_pretrained(
    INDIC_CONFORMER_REPO,
    config=asr_config,
    trust_remote_code=True
).to(ASR_DEVICE).eval()

print("IndicConformer loaded")

# ============================================================
# LOAD WHISPER (FROM HF ONNX)
# ============================================================

print("Loading Whisper Kannada...")

providers = ["CPUExecutionProvider"]
if USE_WHISPER_GPU:
    providers.insert(0, "CUDAExecutionProvider")

# ✅ Download ONNX from HF
encoder_path = hf_hub_download(
    repo_id=WHISPER_REPO,
    filename="encoder_model.onnx"
)

decoder_path = hf_hub_download(
    repo_id=WHISPER_REPO,
    filename="decoder_model.onnx"
)

whisper_processor = WhisperProcessor.from_pretrained(WHISPER_REPO)

whisper_encoder = ort.InferenceSession(encoder_path, providers=providers)
whisper_decoder = ort.InferenceSession(decoder_path, providers=providers)

print("Whisper loaded")

# ============================================================
# LANGUAGE MAP (UNCHANGED)
# ============================================================

LANG_MAP = {
    "kannada": ("kn", "kan_Knda"),
    "hindi": ("hi", "hin_Deva"),
    "telugu": ("te", "tel_Telu"),
    "tamil": ("ta", "tam_Taml"),
    "malayalam": ("ml", "mal_Mlym"),
}

# ============================================================
# AUDIO PROCESSING (UNCHANGED)
# ============================================================

def convert_to_wav(path):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        wav_path = tmp.name

    audio = AudioSegment.from_file(path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(wav_path, format="wav")

    return wav_path


def load_audio(path):
    audio, _ = librosa.load(path, sr=16000)
    audio, _ = librosa.effects.trim(audio, top_db=20)
    return audio

# ============================================================
# ASR + TRANSLATION (UNCHANGED)
# ============================================================

def run_indic(audio, lang):
    wav = torch.tensor(audio).unsqueeze(0).to(ASR_DEVICE)
    with torch.no_grad():
        text = asr_model(wav, LANG_MAP[lang][0], "ctc")
    return text.strip()


def run_whisper(audio):
    inputs = whisper_processor(audio, sampling_rate=16000, return_tensors="np")
    enc = whisper_encoder.run(None, {"input_features": inputs.input_features})[0]

    ids = np.array([[whisper_processor.tokenizer.bos_token_id]])
    tokens = []

    for _ in range(96):
        logits = whisper_decoder.run(
            None,
            {"input_ids": ids, "encoder_hidden_states": enc}
        )[0]

        next_id = int(np.argmax(logits[:, -1, :]))

        if next_id == whisper_processor.tokenizer.eos_token_id:
            break

        tokens.append(next_id)
        ids = np.concatenate([ids, [[next_id]]], axis=1)

    return whisper_processor.tokenizer.decode(tokens, skip_special_tokens=True)


def translate_to_english(text, lang):
    if not text.strip():
        return ""

    _, src_lang = LANG_MAP[lang]

    processed = mt_processor.preprocess_batch(
        [text],
        src_lang=src_lang,
        tgt_lang="eng_Latn"
    )

    inputs = mt_tokenizer(
        processed,
        return_tensors="pt",
        padding=True,
        truncation=True
    ).to(MT_DEVICE)

    with torch.no_grad():
        outputs = mt_model.generate(**inputs, max_length=256, num_beams=5)

    decoded = mt_tokenizer.batch_decode(outputs, skip_special_tokens=True)

    return mt_processor.postprocess_batch(decoded, lang="eng_Latn")[0]

# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def health():
    return {
        "status": "running",
        "source": "Hugging Face",
        "languages": list(LANG_MAP.keys())
    }

# ============================================================
# MAIN API (UNCHANGED)
# ============================================================

@app.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    engine: str = Query("indic"),
    language: str = Query("kannada")
):

    if language not in LANG_MAP:
        raise HTTPException(400, "Unsupported language")

    input_path = None
    wav_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await file.read())
            input_path = tmp.name

        wav_path = convert_to_wav(input_path)
        audio = load_audio(wav_path)

        if engine == "whisper":
            if language != "kannada":
                raise HTTPException(400, "Whisper supports Kannada only")
            text = run_whisper(audio)
        else:
            text = run_indic(audio, language)

        english = translate_to_english(text, language)

        return {
            "transcription": text,
            "english_translation": english
        }

    finally:
        for p in [input_path, wav_path]:
            if p and os.path.exists(p):
                os.remove(p)

# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)