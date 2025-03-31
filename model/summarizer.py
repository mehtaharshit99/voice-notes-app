from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
import os

MODEL_DIR = "./bart-large-cnn"

def download_model():
    """Downloads the model if not found."""
    if not os.path.exists(MODEL_DIR):
        print("Downloading model...")
        model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
        tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
        
        # Save model and tokenizer locally
        model.save_pretrained(MODEL_DIR)
        tokenizer.save_pretrained(MODEL_DIR)

def load_summarizer():
    """Loads the summarization pipeline, ensuring the model is available."""
    download_model()  # Ensure the model is downloaded before loading
    return pipeline("summarization", model=MODEL_DIR, tokenizer=MODEL_DIR)

summarizer = load_summarizer()

def summarize_text(text):
    return summarizer(text, max_length=130, min_length=30, do_sample=False)[0]["summary_text"]