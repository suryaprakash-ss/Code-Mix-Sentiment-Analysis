"""Pipeline orchestrator for code-mixed sentiment analysis.

This file uses package-aware imports so it can be imported as
`src.pipeline_langchain` by uvicorn when running `uvicorn src.api_fastapi:app`.
"""
import importlib
from typing import Any, Dict


def _import(name: str):
    """Try package-relative import first, then fall back to top-level."""
    pkg = __package__
    if pkg:
        try:
            return importlib.import_module(f"{pkg}.{name}")
        except Exception:
            pass
    return importlib.import_module(name)


# Import modules (package-aware)
preproc_mod = _import("preprocessing")
sent_mod = _import("sentiment_model")
sarcasm_mod = _import("sarcasm_detector")
emotion_mod = _import("emotion_detector")
llm_mod = _import("llm_groq")

preprocess = getattr(preproc_mod, "preprocess")
get_sentiment_pipeline = getattr(sent_mod, "get_sentiment_pipeline")
detect_sarcasm = getattr(sarcasm_mod, "detect_sarcasm")
detect_emotion = getattr(emotion_mod, "detect_emotion")
analyze_with_llm = getattr(llm_mod, "analyze_with_llm")


sentiment_pipe = get_sentiment_pipeline()


def run_pipeline(text: str) -> Dict[str, Any]:
    clean = preprocess(text)
    sentiment_result = sentiment_pipe(clean)[0]
    sarcasm_flag = detect_sarcasm(clean)
    emotions = detect_emotion(clean)
    llm_result = analyze_with_llm(clean)

    return {
        "original_text": text,
        "preprocessed_text": clean,
        "sentiment": sentiment_result,
        "sarcasm_rule": sarcasm_flag,
        "emotions": emotions,
        "llm_analysis": llm_result,
    }


if __name__ == "__main__":
    sample = "Yeh movie was fire 🔥🔥"
    print(run_pipeline(sample))
