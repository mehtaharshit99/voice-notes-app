import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import json

# Ensure Firebase is initialized only once
if not firebase_admin._apps:
    try:
        # Load Firebase credentials from Streamlit secrets
        firebase_key_dict = json.loads(st.secrets["firebase_key"])

        # Initialize Firebase
        cred = credentials.Certificate(firebase_key_dict)
        firebase_admin.initialize_app(cred)

        st.success("✅ Firebase initialized successfully!")

    except Exception as e:
        st.error(f"❌ Error initializing Firebase: {e}")

# Get Firestore database instance
db = firestore.client()

def save_transcription(audio_name, transcription, summary):
    """Saves transcription data to Firestore."""
    try:
        doc_ref = db.collection("transcriptions").document(audio_name)
        doc_ref.set({
            "audio_name": audio_name,
            "transcription": transcription,
            "summary": summary,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        st.success("✅ Transcription saved successfully!")
    except Exception as e:
        st.error(f"❌ Error saving transcription: {e}")

def get_all_transcriptions():
    """Fetches all stored transcriptions sorted by timestamp (latest first)."""
    transcriptions = []
    try:
        docs = db.collection("transcriptions").order_by("timestamp", direction=firestore.Query.DESCENDING).stream()
        for doc in docs:
            transcriptions.append(doc.to_dict())
    except Exception as e:
        st.error(f"❌ Error fetching transcriptions: {e}")
    return transcriptions

