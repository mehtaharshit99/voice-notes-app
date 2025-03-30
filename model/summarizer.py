# summarizer.py - Text Summarization Logic
import torch
from transformers import pipeline

# Load BART model for summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0 if torch.cuda.is_available() else -1)

def summarize_text(text, max_chunk_length=1024):
    """Summarizes text by splitting into chunks."""
    if len(text) < 50:
        return "⚠️ Text is too short to summarize."
    chunks = [text[i:i + max_chunk_length] for i in range(0, len(text), max_chunk_length)]
    summaries = summarizer(chunks, max_length=150, min_length=50, do_sample=False)
    summarized_text = " ".join([s["summary_text"] for s in summaries])
    return summarized_text