import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os
from model.whisper import transcribe_audio  
from model.summarizer import summarize_text  

# Initialize Firebase only if it's not already initialized
if not firebase_admin._apps:
    try:
        firebase_config = st.secrets["firebase"]
        cred = credentials.Certificate(dict(firebase_config))  # Convert secrets to dict
        firebase_admin.initialize_app(cred)
        st.success("Firebase initialized successfully.")
    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")
        st.stop()  # Stop execution if Firebase fails

# Firestore client
db = firestore.client()

# Function to store transcription and summary in Firebase
def store_transcription(filename, transcription, summary):
    """Stores transcription and summary in Firebase."""
    try:
        db.collection("transcriptions").document(filename).set({
            "transcription": transcription,
            "summary": summary
        })
        st.success("Transcription and summary stored in Firebase.")
    except Exception as e:
        st.error(f"Error storing transcription in Firebase: {e}")

# Function to process uploaded audio files
def process_audio_file(audio_file):
    """Process uploaded audio file, transcribe, and summarize."""
    try:
        temp_audio_path = "temp_audio.wav"
        with open(temp_audio_path, "wb") as f:
            f.write(audio_file.getbuffer())

        transcription = transcribe_audio(temp_audio_path)
        summary = summarize_text(transcription)

        store_transcription(audio_file.name, transcription, summary)
        os.remove(temp_audio_path)  # Clean up

        return transcription, summary
    except Exception as e:
        st.error(f"Error processing audio: {e}")
        return None, None

# Streamlit UI
st.title("Voice Notes Transcription and Summarization")
uploaded_file = st.file_uploader("Upload an audio file", type=["wav"])

if uploaded_file:
    st.write("Processing audio...")
    transcription, summary = process_audio_file(uploaded_file)

    if transcription and summary:
        st.subheader("Transcription")
        st.write(transcription)
        st.subheader("Summary")
        st.write(summary)



