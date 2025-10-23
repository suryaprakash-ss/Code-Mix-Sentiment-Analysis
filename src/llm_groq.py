import os
from dotenv import load_dotenv
from typing import Any, Dict

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def _init_groq_client():
    """Try to initialize the Groq client. Return None on failure."""
    try:
        # Import lazily so environments without the package won't fail on import
        from langchain_groq.chat_models import ChatGroq

        return ChatGroq(model="groq/compound", api_key=GROQ_API_KEY)
    except Exception:
        return None


_groq_client = _init_groq_client()


def analyze_with_llm(text: str) -> Dict[str, Any]:
    """Sends text to Groq LLM and returns a structured response.

    Returns a dict with either an "output" key or an "error" key.
    """
    if not GROQ_API_KEY:
        return {"error": "GROQ_API_KEY not set"}

    if _groq_client is None:
        return {"error": "Groq client not available in this environment"}

    try:
        messages = [{"role": "user", "content": f"Analyze this text for sentiment, sarcasm, and emotion: {text}"}]
        response = _groq_client.generate(messages)

        # Try various shapes that the client might return
        output_text = None
        try:
            # langchain-like: response.generations[0][0].text
            output_text = response.generations[0][0].text
        except Exception:
            try:
                # alternative: response[0].text
                output_text = response[0].text
            except Exception:
                output_text = str(response)

        # Return a consistent dict shape
        return {"output": output_text}
    except Exception as e:
        return {"error": str(e)}


def llm(text: str) -> Any:
    """Compatibility wrapper named `llm` so other modules can call `llm(...)`.

    It will return the raw output string when possible, or a dict containing an
    "error" key on failure.
    """
    res = analyze_with_llm(text)

    class LLMResult:
        def __init__(self, content=None, error=None):
            self.content = content
            self.error = error

        def __repr__(self):
            return f"LLMResult(content={self.content!r}, error={self.error!r})"

    if isinstance(res, dict):
        if "output" in res:
            return LLMResult(content=res["output"], error=None)
        if "error" in res:
            return LLMResult(content=None, error=res["error"])

    # Fallback - wrap the raw response
    return LLMResult(content=str(res), error=None)


if __name__ == "__main__":
    print(llm("Wow! Another Monday 😒"))
