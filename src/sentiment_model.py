# src/sentiment_model.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

MODEL_NAME = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

def get_sentiment_pipeline():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    sentiment_pipe = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    return sentiment_pipe
