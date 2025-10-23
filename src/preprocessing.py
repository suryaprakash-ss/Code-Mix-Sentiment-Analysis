# src/preprocessing.py
import re
import emoji

def clean_text(text):
    # Remove URLs, mentions, hashtags
    text = re.sub(r"http\S+|www\S+|@\S+|#\S+", "", text)
    text = text.strip()
    return text

def emoji_to_text(text):
    return emoji.demojize(text)  # 🙂 → :slightly_smiling_face:

def preprocess(text):
    text = clean_text(text)
    text = emoji_to_text(text)
    return text

if __name__ == "__main__":
    sample = "Yeh movie was fire 🔥🔥"
    print(preprocess(sample))
