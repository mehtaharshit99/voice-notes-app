# app.py - Streamlit UI and Firebase Integration
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os
from model.whisper import transcribe_audio
from model.summarizer import summarize_text
import tempfile

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("path/to/your/firebase/credentials.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

def store_transcription(filename, transcription, summary):
    """Stores the transcription and summary in Firebase."""
    doc_ref = db.collection("transcriptions").document(filename)
    doc_ref.set({"transcription": transcription, "summary": summary})

def process_audio_file(audio_file):
    """Processes an uploaded audio file."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_file.read())
        temp_audio_path = temp_audio.name
    transcription = transcribe_audio(temp_audio_path)
    summary = summarize_text(transcription)
    store_transcription(audio_file.name, transcription, summary)
    os.remove(temp_audio_path)
    return transcription, summary

st.title("Voice Notes Transcription & Summarization")

# Upload audio file
uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a"])
if uploaded_file:
    st.write("Processing audio...")
    transcription, summary = process_audio_file(uploaded_file)
    st.subheader("Transcription")
    st.write(transcription)
    st.subheader("Summary")
    st.write(summary)
    st.success("Transcription and summary saved successfully!")