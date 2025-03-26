import streamlit as st
import os
import time
import wave
from pydub import AudioSegment
from model.whisper import transcribe_audio
from model.summarizer import summarize_text
from firebase_config import save_transcription, get_all_transcriptions
from fpdf import FPDF

st.title("🎤 Voice Notes AI - Upload, Transcribe & Download")

# Create a folder for recordings
os.makedirs("recordings", exist_ok=True)

# 📂 **Upload a .wav File**
st.subheader("📂 Upload an Audio File")
uploaded_file = st.file_uploader("Choose a WAV file", type=["wav"])

if uploaded_file:
    audio_path = os.path.join("recordings", uploaded_file.name)
    with open(audio_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ File uploaded and saved as {audio_path}")

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
