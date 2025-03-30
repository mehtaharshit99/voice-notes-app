import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os
import tempfile
from fpdf import FPDF
from model.whisper import transcribe_audio
from model.summarizer import summarize_text

# Firebase initialization using Streamlit secrets
try:
    if not firebase_admin._apps:
        # Fetch Firebase credentials from Streamlit secrets
        firebase_config = st.secrets["firebase"]
        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred)
    db = firestore.client()  # Initialize Firestore after Firebase app is initialized

except KeyError as e:
    st.error(f"Error: Firebase configuration is missing in Streamlit secrets. Please add the 'firebase' key to your Streamlit secrets. Details: {e}")
except Exception as e:
    st.error(f"Error initializing Firebase: {e}")

MAX_FILE_SIZE_MB = 200

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

# Upload audio file
st.subheader("Upload a .wav file")
uploaded_file = st.file_uploader("Choose an audio file", type=["wav"])
if uploaded_file:
    st.write("Processing audio...")
    transcription, summary = process_audio_file(uploaded_file)
    if transcription and summary:
        st.subheader("Transcription")
        st.write(transcription)
        st.subheader("Summary")
        st.write(summary)
        pdf_path = save_transcription_as_pdf(uploaded_file.name, transcription, summary)
        st.download_button(label="Download PDF", data=open(pdf_path, "rb").read(), file_name="transcription.pdf", mime="application/pdf")
        st.success("Transcription and summary saved successfully!")
