import os
import time

import httpx
from dotenv import load_dotenv

load_dotenv()

URL = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
RETRYABLE = (429, 500, 502, 503, 504)


class LLMUnavailable(Exception):
    pass


def ask_llm(system, user, retries=3):
    for attempt in range(retries):
        try:
            response = httpx.post(
                URL,
                headers={"Authorization": f"Bearer {os.environ['GEMINI_API_KEY']}"},
                json={
                    "model": os.environ["GEMINI_MODEL"],
                    "temperature": 0,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                },
                timeout=30,
            )
        except httpx.HTTPError:
            raise LLMUnavailable("could not reach the language model")
        if response.status_code in RETRYABLE:
            time.sleep(2 ** attempt * 2)
            continue
        if response.status_code >= 400:
            raise LLMUnavailable(f"language model rejected the request ({response.status_code})")
        return response.json()["choices"][0]["message"]["content"]
    raise LLMUnavailable("language model is rate limited or unavailable")