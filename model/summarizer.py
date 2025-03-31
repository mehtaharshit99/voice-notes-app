from transformers import pipeline

summarizer = pipeline("summarization", model="t5-small")

def summarize_text(text):
    summary = summarizer("summarize: " + text, max_length=100, min_length=30, do_sample=False)
    return summary[0]["summary_text"]
