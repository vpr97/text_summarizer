from transformers import pipeline

# Load once at startup — this takes 30-90s on first run
# ✅ New — load model directly without task string
from transformers import BartForConditionalGeneration, BartTokenizer

model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

# BART's hard token limit
MAX_INPUT_TOKENS = 1024

def summarize_text(text: str, max_length: int = 130, min_length: int = 30) -> str:
    if len(text.split()) < 50:
        raise ValueError("Text too short. Please provide at least 50 words.")
    if min_length >= max_length:
        raise ValueError("min_length must be less than max_length.")

    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=1024)
    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=max_length,
        min_length=min_length,
        do_sample=False
    )
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)



   