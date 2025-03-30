import os
import asyncio
import torch
from streamlit_webrtc import webrtc_streamer
from faster_whisper import WhisperModel
from transformers import pipeline
import streamlit as st

# Ensure event loop is initialized
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# Set environment variables to fix Streamlit path issues
os.environ["STREAMLIT_WATCH_FILES"] = "false"

def transcribe_audio(audio_path):
    """Transcribes audio using Faster-Whisper with English language preference."""
    model = WhisperModel("medium", compute_type="float32")  # Change model size if needed
    segments, _ = model.transcribe(audio_path, language="en")
    return " ".join(segment.text for segment in segments).strip()

# Auto-detect device (force CPU if CUDA is unavailable)
device = 0 if torch.cuda.is_available() else -1
torch.set_default_device("cpu")

# Load BART summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)

def summarize_text(text, max_chunk_length=1024):
    """Summarizes long text by splitting it into chunks."""
    if len(text) < 50:
        return "⚠️ Text is too short to summarize."
    
    chunks = [text[i:i + max_chunk_length] for i in range(0, len(text), max_chunk_length)]
    summaries = summarizer(chunks, max_length=150, min_length=50, do_sample=False)
    return " ".join([s["summary_text"] for s in summaries])

# Streamlit UI
st.title("Voice Notes App")
webrtc_ctx = webrtc_streamer(
    key="speech-to-text",
    rtc_configuration={"iceServers": []},  # Use empty ICE servers if needed
)

if st.button("Process Audio"):
    audio_file = "recorded_audio.wav"  # Placeholder for actual audio file
    transcription = transcribe_audio(audio_file)
    summary = summarize_text(transcription)
    st.text_area("Transcription", transcription, height=200)
    st.text_area("Summary", summary, height=100)

st.write("📌 Ensure microphone permissions are enabled.")
