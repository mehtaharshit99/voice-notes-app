from transformers import pipeline

def load_summarizer():
    return pipeline("summarization", model="facebook/bart-base", tokenizer="facebook/bart-base")

summarizer = load_summarizer()

def summarize_text(text):
    return summarizer(text, max_length=130, min_length=30, do_sample=False)[0]["summary_text"]
