import streamlit as st
import os
import wave
import numpy as np
import pyaudio
from pydub import AudioSegment
from model.whisper import transcribe_audio
from model.summarizer import summarize_text
from firebase_config import save_transcription, get_all_transcriptions
from fpdf import FPDF

# Set up Streamlit UI
st.title("🎤 Voice Notes AI - Record, Upload & Transcribe")

# Create recordings directory if it doesn't exist
os.makedirs("recordings", exist_ok=True)

# Audio recording settings
SAMPLE_RATE = 44100  # CD quality
CHANNELS = 1  # Mono audio
CHUNK = 1024  # Buffer size
FORMAT = pyaudio.paInt16

def record_audio(duration=5, filename="recordings/recorded_audio.wav"):
    """Records audio for a given duration and saves it as a WAV file."""
    st.info(f"Recording for {duration} seconds... 🎙️")

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=SAMPLE_RATE, input=True,
                        frames_per_buffer=CHUNK)

    frames = []
    for _ in range(0, int(SAMPLE_RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b''.join(frames))

    st.success(f"✅ Recording saved as {filename}")
    return filename

# 📌 **Audio Recording**
st.subheader("🎙️ Record Audio")
record_seconds = st.slider("Select recording duration (seconds)", 1, 10, 5)

if st.button("🔴 Start Recording"):
    recorded_audio = record_audio(duration=record_seconds)
    st.audio(recorded_audio, format="audio/wav")
    st.success("🎉 Recording complete! You can now transcribe it.")

# 📂 **Upload an Audio File**
st.subheader("📂 Upload an Audio File")
uploaded_file = st.file_uploader("Choose a WAV file", type=["wav"])

audio_path = None
if uploaded_file:
    audio_path = os.path.join("recordings", uploaded_file.name)
    with open(audio_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ File uploaded and saved as {audio_path}")

# **Proceed with Transcription if a file is available**
if audio_path:
    # 📜 **Transcription**
    st.write("⏳ Transcribing...")
    transcription = transcribe_audio(audio_path)
    st.subheader("📝 Transcription")
    st.write(transcription)

    # 📌 **Auto Summarization**
    st.write("⏳ Generating Summary...")
    summary = summarize_text(transcription)
    st.subheader("📌 Summary & Action Items")
    st.write(summary)

    # 📥 **Save to Database**
    save_transcription(os.path.basename(audio_path), transcription, summary)
    st.success("✅ Transcription and summary saved to Firestore!")

    # 📥 **Download as TXT or PDF**
    def download_notes(format):
        """Generate and download transcription and summary."""
        content = f"Transcription:\n{transcription}\n\nSummary:\n{summary}"
        filename = f"voice_notes.{format}"
        
        if format == "txt":
            st.download_button(label="📥 Download TXT", data=content, file_name=filename, mime="text/plain")
        elif format == "pdf":
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, content)
            pdf.output(filename)
            with open(filename, "rb") as pdf_file:
                st.download_button(label="📥 Download PDF", data=pdf_file, file_name=filename, mime="application/pdf")

    download_notes("txt")
    download_notes("pdf")

# 📜 **Retrieve Previous Transcriptions**
st.subheader("📜 View Saved Transcriptions")
transcriptions = get_all_transcriptions()

if transcriptions:
    for entry in transcriptions:
        with st.expander(f"{entry['audio_name']} - {entry['timestamp']}"):
            st.write("📝 **Transcription:**")
            st.write(entry["transcription"])
            st.write("📌 **Summary:**")
            st.write(entry["summary"])
else:
    st.write("No transcriptions saved yet.")
