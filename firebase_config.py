import firebase_admin
from firebase_admin import credentials, firestore
import json
import streamlit as st

# Check if Firebase is already initialized
if not firebase_admin._apps:
    # Load Firebase credentials from Streamlit secrets
    firebase_key_dict = st.secrets["firebase_key"]

    # Initialize Firebase
    cred = credentials.Certificate(firebase_key_dict)
    firebase_admin.initialize_app(cred)

# Get Firestore database instance
db = firestore.client()

def save_transcription(audio_name, transcription, summary):
    """Saves the audio filename, transcription, and summary to Firestore."""
    doc_ref = db.collection("transcriptions").document(audio_name)
    doc_ref.set({
        "audio_name": audio_name,
        "transcription": transcription,
        "summary": summary,
        "timestamp": firestore.SERVER_TIMESTAMP
    })

def get_all_transcriptions():
    """Fetches all stored transcriptions."""
    transcriptions = []
    docs = db.collection("transcriptions").order_by("timestamp", direction=firestore.Query.DESCENDING).stream()
    for doc in docs:
        transcriptions.append(doc.to_dict())
    return transcriptions
