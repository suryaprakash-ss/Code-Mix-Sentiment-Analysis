# Code-Mix Sentiment Analysis

Lightweight scaffold for code-mixed sentiment analysis with rule-based sarcasm detection, a Hugging Face sentiment model, an LLM integration (Groq), a FastAPI backend and a Streamlit frontend.

## Repository structure
```
.
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── preprocessing.py
│   ├── sentiment_model.py       # Hugging Face transformer
│   ├── sarcasm_detector.py
│   ├── pipeline_langchain.py    # orchestration wrapper
│   ├── llm_groq.py              # Groq API interaction
│   ├── api_fastapi.py           # FastAPI backend
│   ├── app_streamlit.py         # Streamlit frontend
│   └── __init__.py
├── config.yaml
├── requirements.txt
└── README.md
```

## Quick overview
- `src/pipeline_langchain.py` — orchestrates preprocessing, sentiment, sarcasm, emotion (if present) and LLM analysis.
- `src/llm_groq.py` — small wrapper to call Groq LLM; requires `GROQ_API_KEY`.
- `src/sentiment_model.py` — loads a HF transformers model (heavy).
- `src/api_fastapi.py` — FastAPI app exposing `/predict`.
- `src/app_streamlit.py` — Streamlit UI (scaffold).

## Prerequisites
- Python 3.10+ recommended
- Windows (instructions below use PowerShell)
- Optional: GPU and appropriate CUDA toolchain if you plan to run heavy models locally

## Setup (Windows PowerShell)

1. Create and activate a venv (PowerShell):
```powershell
# from the project root
python -m venv .\venv

# Allow running the activate script for this session (if required)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Activate
.\venv\Scripts\Activate.ps1
```

If you use cmd.exe:
```cmd
.\venv\Scripts\activate.bat
```

2. Upgrade pip and install requirements:
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `requirements.txt` is minimal or missing, install recommended packages:
```powershell
pip install transformers torch fastapi uvicorn streamlit python-dotenv emoji langchain
# If you use Groq's LangChain integration:
pip install langchain-groq
```
Note: For PyTorch, choose the correct wheel for your CUDA version from https://pytorch.org/ — the above command installs the default CPU wheel or may detect a compatible wheel.

3. Environment variables
Create a `.env` file in the project root (not committed to git) to store secrets:
```
GROQ_API_KEY=your_groq_api_key_here
```
The project uses `python-dotenv` where appropriate.

## Run the pipeline (standalone)
You can run the pipeline directly for quick tests. Run from the project root to ensure package imports resolve:

PowerShell:
```powershell
# recommended - run as a module to preserve package import paths
python -m src.pipeline_langchain
```

Or:
```powershell
python src/pipeline_langchain.py
```

This will run the `run_pipeline` entry in `src.pipeline_langchain`. In minimal environments the modules provide graceful fallbacks (so you get predictable output even without heavy packages or API keys).

## Run the FastAPI server
From the project root run (PowerShell):
```powershell
uvicorn src.api_fastapi:app --reload
```
- Visit docs: http://127.0.0.1:8000/docs
- Predict endpoint: `POST /predict` with JSON body `{"text": "Some text"}`

Example curl:
```powershell
curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d "{\"text\": \"Worst first off but great ending\"}"
```

Expected (fallback) response example:
```json
{
  "original_text": "Worst first off but great ending",
  "preprocessed_text": "Worst first off but great ending",
  "sentiment": {"label": "NEUTRAL", "score": 1.0},
  "sarcasm_rule": 0,
  "emotions": ["neutral"],
  "llm_analysis": {"error": "GROQ_API_KEY not set"}  // or LLM output when available
}
```

## Run the Streamlit UI
```powershell
streamlit run src/app_streamlit.py
```
Then open the URL printed by Streamlit (usually http://localhost:8501).

## Troubleshooting — ModuleNotFoundError for `pipeline_langchain`
Symptom:
- Uvicorn fails with `ModuleNotFoundError: No module named 'pipeline_langchain'`.

Cause:
- When you run `uvicorn src.api_fastapi:app` the `src` package is imported as a package; internal imports must be package-aware or resolved relative to `src`. Running uvicorn from the project root and using `src.` module paths helps.

Fixes:
1. Run uvicorn from the project root:
```powershell
uvicorn src.api_fastapi:app --reload
```
2. Make sure `src` is a package (there is an `__init__.py` in `src/`).
3. Prefer package imports inside modules (the project uses a safe import pattern that resolves `src.*` first).
4. If you still see import errors inside handler code, `api_fastapi.py` delays importing `pipeline_langchain` until request time to reduce startup import-time failures.

If you see `ModuleNotFoundError: No module named 'preprocessing'` from `src.pipeline_langchain`:
- This means Python attempted to import the sibling modules using top-level names. Ensure you run from project root and that `src` is on the import path (running uvicorn as `src.api_fastapi:app` does this). Alternatively, run `python -m src.pipeline_langchain` to exercise the pipeline as a module.

## Environment & dependency notes
- `transformers` and `torch` are heavy. If you only want to prototype without downloading models, keep the fallback implementations or stub the calls.
- For production LLM calls (Groq), ensure `GROQ_API_KEY` is set and `langchain-groq` is installed. The `src/llm_groq.py` file wraps the client and ensures a safe fallback if the client or key is missing.
- If you plan to use GPU, install appropriate `torch` version (see https://pytorch.org/get-started/locally/).

## Debugging tips
- Inspect server logs: they show full tracebacks.
- Reproduce import errors with a small Python snippet:
```powershell
python -c "import importlib; importlib.import_module('src.api_fastapi')"
```
If `fastapi` is not installed, stub it via `sys.modules` for import tests, but to run the server install the package in the venv.

## Recommended next steps
- Add unit tests for `preprocessing`, `sarcasm_detector`, and `pipeline_langchain`.
- Add CI to run linting and tests.
- Add a `requirements-dev.txt` for linters/test runners (pytest, black, flake8).
- Implement real Streamlit UI and production-ready FastAPI features (schemas, validation, CORS, auth).

## .gitignore snippet (recommended)
```
venv/
__pycache__/
.env
*.pyc
*.pkl
.cache/
```