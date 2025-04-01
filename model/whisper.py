
from faster_whisper import WhisperModel

def transcribe_audio(audio_path):
    """
    Transcribes an audio file to text using the Faster Whisper model.
    :param audio_path: Path to the audio file.
    :return: Transcribed text.
    """
    model = WhisperModel("base")
    segments, _ = model.transcribe(audio_path)
    transcription = " ".join(segment.text for segment in segments)
    return transcription
