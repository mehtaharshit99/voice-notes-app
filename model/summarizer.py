from transformers import pipeline

def load_summarizer():
    return pipeline("summarization", model="./bart-large-cnn", tokenizer="./bart-large-cnn")

summarizer = load_summarizer()

def summarize_text(text):
    return summarizer(text, max_length=130, min_length=30, do_sample=False)[0]["summary_text"]
