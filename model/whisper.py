# whisper.py - Transcription Logic
import torch
from faster_whisper import WhisperModel

# Auto-detect device
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Load Whisper model for transcription
whisper_model = WhisperModel("medium", compute_type="float32")

def transcribe_audio(audio_path):
    """Transcribes audio using Faster-Whisper."""
    segments, _ = whisper_model.transcribe(audio_path, language="en")
    transcription = " ".join(segment.text for segment in segments)
    return transcription.strip()
