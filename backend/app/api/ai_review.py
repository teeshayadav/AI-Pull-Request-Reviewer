import httpx
from fastapi import APIRouter, HTTPException

router = APIRouter()

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:3b"


@router.post("/review")
async def review_code(code: str):

    if not code:
        raise HTTPException(
            status_code=400,
            detail="No code provided"
        )

    prompt = f"""
You are an expert Python code reviewer.

Review the following Python code.

Find:

1. Bugs
2. Security issues
3. Performance issues
4. Code quality problems
5. Suggestions for improvement

Explain each issue clearly and provide a fix.

Here is the code:

{code}
"""

    try:
        async with httpx.AsyncClient(timeout=180.0) as client:

            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False
                }
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=f"Ollama returned {response.status_code}: {response.text}"
            )

        data = response.json()

        review = data.get("response")

        if not review:
            raise HTTPException(
                status_code=500,
                detail=f"Ollama returned no review: {data}"
            )

        return {
            "review": review
        }

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Could not connect to Ollama: {repr(e)}"
        )