# src/api_fastapi.py
from fastapi import FastAPI
from pydantic import BaseModel
import importlib
from typing import Any

app = FastAPI(title="Code-Mixed Sentiment LLM API")


class TextInput(BaseModel):
    text: str


@app.post("/predict")
def predict(input: TextInput) -> Any:
    """Import and call the pipeline at request time to avoid import-time failures
    when uvicorn imports this module.
    """
    # Preferred import path when running with uvicorn from the project root
    try:
        mod = importlib.import_module("src.pipeline_langchain")
    except Exception:
        # Fallback for environments where the package root isn't configured
        mod = importlib.import_module("pipeline_langchain")

    run_pipeline = getattr(mod, "run_pipeline")
    return run_pipeline(input.text)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.api_fastapi:app", host="0.0.0.0", port=8000, reload=False)
