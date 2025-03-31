from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

model_name = "facebook/bart-large-cnn"

print("Downloading the model...")
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

model.save_pretrained("./bart-large-cnn")
tokenizer.save_pretrained("./bart-large-cnn")

print("Model saved successfully!")
