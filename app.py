import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os
from io import BytesIO
import wave
import numpy as np
import librosa
from model.whisper import transcribe_audio  # Assuming you have this function in model/whisper.py
from model.summarizer import summarize_text  # Assuming you have this function in model/summarizer.py

# Initialize Firebase using Streamlit Secrets
if not firebase_admin._apps:
    try:
        # Retrieve Firebase credentials from Streamlit secrets
        firebase_config = st.secrets["firebase"]
        
        # Firebase credentials in dictionary format
        cred_dict = {
            "project_id": firebase_config["project_id"],
            "private_key_id": firebase_config["private_key_id"],
            "private_key": firebase_config["private_key"],
            "client_email": firebase_config["client_email"],
            "client_id": firebase_config["client_id"],
            "auth_uri": firebase_config["auth_uri"],
            "token_uri": firebase_config["token_uri"],
            "auth_provider_x509_cert_url": firebase_config["auth_provider_x509_cert_url"],
            "client_x509_cert_url": firebase_config["client_x509_cert_url"]
        }

        # Initialize Firebase with the credentials
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        st.success("Firebase initialized successfully.")
    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")

# Firebase Firestore client
db = firestore.client()

# Function to store transcription and summary in Firebase
def store_transcription(filename, transcription, summary):
    """Stores the transcription and summary in Firebase."""
    try:
        doc_ref = db.collection("transcriptions").document(filename)
        doc_ref.set({
            "transcription": transcription,
            "summary": summary
        })
        st.success("Transcription and summary stored in Firebase.")
    except Exception as e:
        st.error(f"Error storing transcription in Firebase: {e}")

# Function to process uploaded audio files
def process_audio_file(audio_file):
    """Process the uploaded audio file, transcribe and summarize."""
    # Temporarily save the audio file
    temp_audio_path = os.path.join("temp_audio.wav")
    with open(temp_audio_path, "wb") as f:
        f.write(audio_file.getbuffer())

    # Transcribe and summarize
    transcription = transcribe_audio(temp_audio_path)
    summary = summarize_text(transcription)

    # Store the transcription and summary in Firebase
    store_transcription(audio_file.name, transcription, summary)

    # Clean up the temporary file
    os.remove(temp_audio_path)

    return transcription, summary

# Streamlit UI components
st.title("Voice Notes Transcription and Summarization")
uploaded_file = st.file_uploader("Choose an audio file", type=["wav"])

if uploaded_file:
    st.write("Processing audio...")
    transcription, summary = process_audio_file(uploaded_file)
    
    if transcription and summary:
        st.subheader("Transcription")
        st.write(transcription)
        st.subheader("Summary")
        st.write(summary)
