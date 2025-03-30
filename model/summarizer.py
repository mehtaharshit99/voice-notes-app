# summarizer.py
from transformers import pipeline

# Load the summarization model
summarizer = pipeline("summarization")

def summarize_text(text):
    """
    Summarizes the given text using a pre-trained summarization model.
    :param text: The text to summarize.
    :return: The summary of the text.
    """
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]["summary_text"]
