from faster_whisper import WhisperModel

# Load Whisper model (medium version for better accuracy)
model = WhisperModel("medium", compute_type="float32")  # Options: "tiny", "small", "medium", "large-v2"

def transcribe_audio(audio_path):
    """Transcribes audio using Faster-Whisper with English language preference."""
    segments, info = model.transcribe(audio_path, language="en")  # Force English transcription

    transcription = ""
    for segment in segments:
        transcription += f"{segment.text} "

    return transcription.strip()
