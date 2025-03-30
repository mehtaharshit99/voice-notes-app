import asyncio
import torch
import streamlit as st
from streamlit_webrtc import webrtc_streamer
from model.whisper import transcribe_audio
from model.summarizer import summarize_text

# Ensure an event loop is running for async operations
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# Set device for Torch (CPU/GPU handling)
device = "cuda" if torch.cuda.is_available() else "cpu"
st.write(f"Device set to use {device}")

# Streamlit UI
st.title("Voice Notes App")

# WebRTC Configuration Fix
webrtc_ctx = webrtc_streamer(
    key="speech-recognition",
    frontend_rtc_configuration={},
    server_rtc_configuration={}
)

if st.button("Transcribe Audio"):
    audio_path = "recorded_audio.wav"  # Placeholder for actual recorded file path
    transcription = transcribe_audio(audio_path)
    st.write("**Transcription:**", transcription)
    
    summary = summarize_text(transcription)
    st.write("**Summary:**", summary)

st.write("📌 Record audio, transcribe, and summarize your voice notes!")
