import torch
from transformers import pipeline

# Auto-detect device (GPU if available, else CPU)
device = 0 if torch.cuda.is_available() else -1

# Load BART summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)

def summarize_text(text, max_chunk_length=1024):
    """Summarizes long text by splitting it into chunks."""
    if len(text) < 50:
        return "⚠️ Text is too short to summarize."

    # Split text into manageable chunks
    chunks = [text[i:i + max_chunk_length] for i in range(0, len(text), max_chunk_length)]
    
    # Generate summary for each chunk
    summaries = summarizer(chunks, max_length=150, min_length=50, do_sample=False)
    
    # Combine summaries
    summarized_text = " ".join([s["summary_text"] for s in summaries])
    
    return summarized_text
