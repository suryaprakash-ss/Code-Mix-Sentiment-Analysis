# src/sarcasm_detector.py
def detect_sarcasm(text):
    # Simple keyword-based sarcasm detection
    sarcasm_keywords = ["yeah right", "great job", "wow", "nice", "sure"]
    text_lower = text.lower()
    return int(any(word in text_lower for word in sarcasm_keywords))
