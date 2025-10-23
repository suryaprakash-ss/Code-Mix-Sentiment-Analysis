# src/emotion_detector.py
import emoji

# Map common emojis to emotions
emoji_emotions = {
    ":smile:": "joy",
    ":grinning_face_with_smiling_eyes:": "joy",
    ":fire:": "excitement",
    ":cry:": "sadness",
    ":pensive:": "sadness",
    ":angry:": "anger",
    ":heart:": "love",
    ":disappointed:": "disappointment",
    ":unamused:": "sarcasm"
}

def detect_emotion(text):
    text_emoji = emoji.demojize(text)
    emotions = []
    for emo, emotion in emoji_emotions.items():
        if emo in text_emoji:
            emotions.append(emotion)
    return emotions if emotions else ["neutral"]
