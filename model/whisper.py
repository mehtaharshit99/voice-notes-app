from faster_whisper import WhisperModel

def transcribe_audio(audio_path):
    """Transcribes audio using Faster-Whisper with English language preference."""
    # Load Whisper model (medium version for better accuracy)
    model = WhisperModel("medium", compute_type="float32")  # Options: "tiny", "small", "medium", "large-v2"
    
    segments, _ = model.transcribe(audio_path, language="en")  # Force English transcription
    
    transcription = " ".join(segment.text for segment in segments)
    
    return transcription.strip()
