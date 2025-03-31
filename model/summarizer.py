from transformers import pipeline

def load_summarizer():
    return pipeline("summarization", model="t5-small", tokenizer="t5-small")

summarizer = load_summarizer()

def summarize_text(text):
    return summarizer(text, max_length=150, min_length=50, do_sample=False)[0]["summary_text"]
