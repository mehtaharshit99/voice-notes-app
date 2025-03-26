from transformers import pipeline

# Load BART summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)  # Runs on CPU

def summarize_text(text):
    """Summarizes text using the BART model."""
    if len(text) < 50:  # Avoid short texts
        return "⚠️ Text is too short to summarize."

    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']
