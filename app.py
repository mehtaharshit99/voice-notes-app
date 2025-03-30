import streamlit as st
import os
import tempfile
from whisper import transcribe_audio  # Ensure correct import
from summarizer import summarize_text  # Ensure correct import
from firebase_config import save_transcription, get_all_transcriptions
from fpdf import FPDF
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import av
import asyncio

# Ensure AsyncIO Event Loop
def ensure_event_loop():
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

ensure_event_loop()

# Set up Streamlit UI
st.title("🎤 Voice Notes AI - Record, Upload & Transcribe")

# WebRTC Audio Processor Class
class AudioProcessor(AudioProcessorBase):
    def recv_audio(self, frame: av.AudioFrame) -> av.AudioFrame:
        raw_audio = frame.to_ndarray()
        return av.AudioFrame.from_ndarray(raw_audio, format="s16")

# 📌 **Audio Recording using WebRTC**
st.subheader("🎤 Record Audio")
webrtc_ctx = webrtc_streamer(
    key="audio_recorder",
    mode=WebRtcMode.SENDRECV,
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"video": False, "audio": True},
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
)

audio_path = None
if webrtc_ctx.audio_receiver:
    audio_frames = webrtc_ctx.audio_receiver.get_frames()
    if audio_frames:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_frames[0].to_ndarray().tobytes())
            audio_path = temp_audio.name
            st.success("✅ Recording complete! You can now transcribe it.")
            st.audio(audio_path, format="audio/wav")

# 📂 **Upload an Audio File**
st.subheader("📂 Upload an Audio File")
uploaded_file = st.file_uploader("Choose a WAV file", type=["wav"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(uploaded_file.read())
        audio_path = temp_audio.name
    st.success(f"✅ File uploaded and saved as {audio_path}")
    st.audio(audio_path, format="audio/wav")

# **Proceed with Transcription if a file is available**
if audio_path:
    # 💜 **Transcription**
    st.write("⏳ Transcribing...")
    transcription = transcribe_audio(audio_path)
    st.subheader("📝 Transcription")
    st.write(transcription)

    # 📌 **Auto Summarization**
    st.write("⏳ Generating Summary...")
    summary = summarize_text(transcription)
    st.subheader("📌 Summary & Action Items")
    st.write(summary)

    # 👥 **Save to Database**
    save_transcription(os.path.basename(audio_path), transcription, summary)
    st.success("✅ Transcription and summary saved to Firestore!")

    # 📅 **Download as TXT or PDF**
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

# 📝 **Retrieve Previous Transcriptions**
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
