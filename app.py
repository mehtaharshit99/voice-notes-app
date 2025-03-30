# app.py - Streamlit UI and Firebase Integration for Cloud Deployment
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os
import tempfile
from fpdf import FPDF
import json
import numpy as np
import wave
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode

# Import the transcription and summarization functions from the 'model' folder
from model.whisper import transcribe_audio
from model.summarizer import summarize_text

# Firebase initialization
try:
    if not firebase_admin._apps:
        # Fetch Firebase credentials directly from Streamlit secrets
        firebase_config = st.secrets["firebase"]
        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred)

    db = firestore.client()

except KeyError as e:
    st.error(f"Error: Firebase configuration is missing in Streamlit secrets. Please add the 'firebase' key to your secrets in Streamlit Cloud. Details: {e}")
except Exception as e:
    st.error(f"Error initializing Firebase: {e}")

MAX_FILE_SIZE_MB = 200
MAX_RECORDING_DURATION = 60  # in seconds

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.audio_data = []

    def recv(self, frame):
        # Append audio frames as they are received
        self.audio_data.append(frame)
        return frame

    def get_audio(self):
        # Return the recorded audio data as a numpy array
        return np.concatenate(self.audio_data, axis=0)

def store_transcription(filename, transcription, summary):
    """Stores the transcription and summary in Firebase."""
    doc_ref = db.collection("transcriptions").document(filename)
    doc_ref.set({"transcription": transcription, "summary": summary})

def process_audio_file(audio_file):
    """Processes an uploaded audio file."""
    if audio_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        st.error("File size exceeds 200MB limit.")
        return None, None
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_file.read())
        temp_audio_path = temp_audio.name
    
    # Transcribe and summarize
    transcription = transcribe_audio(temp_audio_path)
    summary = summarize_text(transcription)
    store_transcription(audio_file.name, transcription, summary)
    
    # Clean up
    os.remove(temp_audio_path)
    
    return transcription, summary

def save_transcription_as_pdf(filename, transcription, summary):
    """Saves the transcription and summary as a PDF file."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Transcription & Summary", ln=True, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Transcription:\n{transcription}\n\nSummary:\n{summary}")
    pdf_path = f"{filename}.pdf"
    pdf.output(pdf_path)
    return pdf_path

st.title("Voice Notes Transcription & Summarization")

# Display instructions for voice recording
st.subheader("Record Your Audio")

# We use the WebRTC component for voice recording
webrtc_ctx = webrtc_streamer(
    key="voice-recorder", 
    mode=WebRtcMode.SENDRECV,
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True, "video": False},
)

# When the user clicks on the "Stop Recording" button, process the audio
if webrtc_ctx.state.playing:
    st.write("Recording audio... Please wait.")
    if st.button("Stop Recording"):
        # Process the recorded audio
        audio_processor = webrtc_ctx.audio_processor
        audio_data = audio_processor.get_audio()

        # Convert to WAV file format
        temp_audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
        with wave.open(temp_audio_path, 'wb') as f:
            f.setnchannels(1)  # Mono audio
            f.setsampwidth(2)  # 16-bit depth
            f.setframerate(16000)  # 16 kHz sample rate
            f.writeframes(audio_data.tobytes())
        
        # Process the audio for transcription and summarization
        transcription, summary = process_audio_file(open(temp_audio_path, "rb"))
        if transcription and summary:
            st.subheader("Transcription")
            st.write(transcription)
            st.subheader("Summary")
            st.write(summary)
            pdf_path = save_transcription_as_pdf("recorded_transcription", transcription, summary)
            st.download_button(label="Download PDF", data=open(pdf_path, "rb").read(), file_name="transcription.pdf", mime="application/pdf")
        
        # Clean up
        os.remove(temp_audio_path)
