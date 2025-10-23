# src/app_streamlit.py
import streamlit as st
import requests

st.title("Code-Mixed Sentiment Analysis with Sarcasm & Emotion")

text_input = st.text_area("Enter your text:")

if st.button("Predict"):
    response = requests.post("http://localhost:8000/predict", json={"text": text_input})
    if response.status_code == 200:
        result = response.json()
        st.write("Preprocessed Text:", result["preprocessed_text"])
        st.write("Sentiment:", result["sentiment"])
        st.write("Sarcasm (Rule-Based):", result["sarcasm_rule"])
        st.write("Emotions Detected:", result["emotions"])
        st.write("LLM Analysis:", result["llm_analysis"])
    else:
        st.error("API error!")
