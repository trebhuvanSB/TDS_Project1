import httpx
import json
import numpy as np
import time
from function_definitions import FUNCTION_DEFINITIONS
from dotenv import load_dotenv
import os

AIPROXY_URL = "http://aiproxy.sanand.workers.dev/openai/v1"
load_dotenv()
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")

def query_llm(task_description: str, retries: int = 5, delay: int = 1):
    for attempt in range(retries):
        try:
            response = httpx.post(
                AIPROXY_URL + "/chat/completions",
                headers={
                    "Authorization": f"Bearer {AIPROXY_TOKEN}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": task_description}],
                    "tools": FUNCTION_DEFINITIONS,
                    "tool_choice": "auto",
                },
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            if attempt < retries - 1:
                print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise

def ask_llm(prompt: str) -> str:
    response = httpx.post(
        AIPROXY_URL + "/chat/completions",
        headers={
            "Authorization": f"Bearer {AIPROXY_TOKEN}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 1,
            "max_tokens": 100,
        },
    )
    return response.json()["choices"][0]["message"]["content"]

async def generate_embeddings(text: str):
    response = httpx.post(
        AIPROXY_URL + "/embeddings",
        headers={
            "Authorization": f"Bearer {AIPROXY_TOKEN}",
            "Content-Type": "application/json",
        },
        json={
            "model": "text-embedding-3-small",
            "input": text,
        },
    )
    return np.array([emb["embedding"] for emb in response.json()["data"]])