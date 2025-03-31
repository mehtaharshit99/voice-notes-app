from transformers import pipeline
import streamlit as st

@st.cache_resource()
def load_summarizer():
    return pipeline("summarization", model="./bart-large-cnn")

summarizer = load_summarizer()

def summarize_text(text):
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]["summary_text"]
