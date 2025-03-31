from transformers import pipeline

# Specify the model for summarization explicitly
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", use_fast=True)


def summarize_text(text):
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]["summary_text"]
