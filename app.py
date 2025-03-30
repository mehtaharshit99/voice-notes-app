import asyncio
import tempfile
import torch
import streamlit as st
from transformers import pipeline
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from faster_whisper import WhisperModel

# Ensure an active event loop

def get_or_create_eventloop():
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop

get_or_create_eventloop()

# Load Whisper Model for Speech-to-Text
def transcribe_audio(audio_path):
    model = WhisperModel("medium", compute_type="float32")
    segments, _ = model.transcribe(audio_path, language="en")
    transcription = " ".join(segment.text for segment in segments)
    return transcription.strip()

# Load Summarizer Model
device = 0 if torch.cuda.is_available() else -1
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)

def summarize_text(text, max_chunk_length=1024):
    if len(text) < 50:
        return "⚠️ Text is too short to summarize."
    chunks = [text[i:i + max_chunk_length] for i in range(0, len(text), max_chunk_length)]
    summaries = summarizer(chunks, max_length=150, min_length=50, do_sample=False)
    summarized_text = " ".join([s["summary_text"] for s in summaries])
    return summarized_text

# Streamlit UI
st.title("🎙 Voice Notes App")
st.write("Record audio, transcribe it, and generate summaries.")

webrtc_ctx = webrtc_streamer(
    key="audio_recorder",
    mode=WebRtcMode.SENDRECV,
    media_stream_constraints={"video": False, "audio": True},
    frontend_rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    server_rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
)

if webrtc_ctx.audio_receiver:
    audio_frames = webrtc_ctx.audio_receiver.get_frames()
    if audio_frames:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            for frame in audio_frames:
                temp_audio.write(frame.to_ndarray().tobytes())
            audio_path = temp_audio.name
        
        st.success("✅ Recording complete! You can now transcribe it.")
        st.audio(audio_path, format="audio/wav")
        
        if st.button("Transcribe Audio"):
            transcript = transcribe_audio(audio_path)
            st.text_area("📜 Transcription:", transcript, height=200)
            
            if st.button("Summarize Text"):
                summary = summarize_text(transcript)
                st.text_area("📝 Summary:", summary, height=150)
