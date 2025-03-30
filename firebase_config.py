import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# Ensure Firebase is only initialized once
if not firebase_admin._apps:
    try:
        firebase_key_dict = None

        # ✅ Streamlit Cloud: Use st.secrets
        if "firebase_key" in st.secrets:
            firebase_key_dict = json.loads(st.secrets["firebase_key"])

        # ✅ Local/Production: Use environment variable
        elif os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            firebase_key_dict = json.loads(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

        else:
            raise ValueError("❌ Firebase credentials not found! Set up Streamlit secrets or an environment variable.")

        # Initialize Firebase
        cred = credentials.Certificate(firebase_key_dict)
        firebase_admin.initialize_app(cred)
        print("✅ Firebase initialized successfully!")

    except Exception as e:
        print(f"❌ Error initializing Firebase: {e}")

# Get Firestore database instance
db = firestore.client()

def save_transcription(audio_name, transcription, summary):
    """Saves the audio filename, transcription, and summary to Firestore."""
    try:
        doc_ref = db.collection("transcriptions").document(audio_name)
        doc_ref.set({
            "audio_name": audio_name,
            "transcription": transcription,
            "summary": summary,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        print("✅ Transcription saved successfully!")
    except Exception as e:
        print(f"❌ Error saving transcription: {e}")

def get_all_transcriptions():
    """Fetches all stored transcriptions sorted by timestamp (latest first)."""
    transcriptions = []
    try:
        docs = db.collection("transcriptions").order_by("timestamp", direction=firestore.Query.DESCENDING).stream()
        for doc in docs:
            transcriptions.append(doc.to_dict())
    except Exception as e:
        print(f"❌ Error fetching transcriptions: {e}")
    return transcriptions
