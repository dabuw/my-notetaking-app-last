import os
from dotenv import load_dotenv
from typing import List, Dict, Any

# Use a lightweight HTTP client for the example. We keep this implementation
# generic so you can replace the client with the official SDK if desired.
import requests


load_dotenv()  # Loads environment variables from .env


GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
ENDPOINT = os.environ.get("GITHUB_MODELS_ENDPOINT", "https://models.github.ai/inference")
DEFAULT_MODEL = os.environ.get("GITHUB_MODEL", "openai/gpt-4.1-mini")


def call_llm_model(model: str, messages: List[Dict[str, Any]], temperature: float = 1.0, top_p: float = 1.0) -> str:
    """Call an LLM model via a simple HTTP API. Returns the assistant text.

    This function assumes the endpoint accepts a POST with JSON like:
    {"model": model, "messages": messages, ...}
    and returns a JSON where choices[0].message.content holds the text.
    """
    if not GITHUB_TOKEN:
        raise RuntimeError("GITHUB_TOKEN is not set in environment")

    # If a GitHub Models endpoint is configured, try to use the OpenAI-compatible
    # client (the user's `test.py` uses `from openai import OpenAI` with base_url).
    github_endpoint = os.environ.get("GITHUB_MODELS_ENDPOINT") or ENDPOINT
    # Try OpenAI-compatible SDK with the GitHub models endpoint (or default ENDPOINT)
    try:
        from openai import OpenAI
        client = OpenAI(base_url=github_endpoint, api_key=GITHUB_TOKEN)
        resp = client.chat.completions.create(model=model, messages=messages, temperature=temperature, top_p=top_p)
        # response shape may contain choices[0].message.content or choices[0].text
        try:
            return resp.choices[0].message.content
        except Exception:
            try:
                return resp.choices[0].text
            except Exception:
                raise RuntimeError(f"Unexpected SDK response shape: {resp}")
    except Exception as e:
        # If SDK not installed or request failed, surface helpful message and fall back to HTTP
        sdk_err = e

    # Fallback: plain HTTP POST to ENDPOINT
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "top_p": top_p,
    }

    try:
        resp = requests.post(ENDPOINT, headers=headers, json=payload, timeout=30)
    except Exception as e:
        raise RuntimeError(f"Failed to contact LLM endpoint {ENDPOINT}: {e}")

    # If non-2xx, include body for easier debugging
    if not resp.ok:
        body = None
        try:
            body = resp.text
        except Exception:
            body = '<unavailable>'
        raise RuntimeError(f"LLM request failed: {resp.status_code} {resp.reason}. Response body: {body}")

    data = resp.json()

    # Try common response shapes
    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        # fallback: try other keys
        if "choices" in data and len(data["choices"]) > 0:
            c = data["choices"][0]
            if isinstance(c, dict) and "text" in c:
                return c["text"]
        raise RuntimeError("Unexpected LLM response format: %r" % (data,))


def translate(text: str, target_lang: str = "zh-CN") -> str:
    """Translate `text` into `target_lang` using the configured LLM model.

    Returns translated string. This is a simple wrapper that sends a system
    instruction + user message to the model.
    """
    system_prompt = (
        f"You are a helpful translator. Translate the user's text into {target_lang}. "
        "Return only the translation without extra commentary."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text},
    ]

    # If OPENAI_API_KEY is provided and openai package is available, prefer that SDK path
    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        try:
            import openai
            openai.api_key = openai_key
            # Use ChatCompletion (classic interface)
            completion = openai.ChatCompletion.create(model=DEFAULT_MODEL, messages=messages, temperature=1.0)
            return completion.choices[0].message.content if hasattr(completion.choices[0], 'message') else completion.choices[0].text
        except Exception:
            # fall back to HTTP call below if SDK not available or fails
            pass

    return call_llm_model(DEFAULT_MODEL, messages)


def main():
    # Simple CLI test: read from stdin or a sample string and translate to Chinese
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--text", "-t", help="Text to translate", required=False)
    parser.add_argument("--lang", "-l", help="Target language (e.g. zh-CN)", default="zh-CN")
    args = parser.parse_args()

    source = args.text
    if not source:
        source = "Hello, this is a test of the translation feature."

    try:
        translated = translate(source, args.lang)
        print("Translated:\n", translated)
    except Exception as e:
        print("Error calling LLM:", e)


if __name__ == "__main__":
    main()
