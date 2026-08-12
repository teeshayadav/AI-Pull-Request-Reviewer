from fastapi import APIRouter, HTTPException
from github import Github
from urllib.parse import urlparse
import httpx

router = APIRouter()

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:3b"


def parse_pr_url(pr_url: str):
    parsed = urlparse(pr_url)

    if parsed.netloc != "github.com":
        raise ValueError("Only GitHub PR URLs are supported")

    parts = parsed.path.strip("/").split("/")

    if len(parts) < 4 or parts[2] != "pull":
        raise ValueError("Invalid GitHub Pull Request URL")

    owner = parts[0]
    repo = parts[1]
    pr_number = int(parts[3])

    return owner, repo, pr_number


@router.post("/review-pr")
async def review_pull_request(pr_url: str):

    try:
        # 1. Parse GitHub PR URL
        owner, repo_name, pr_number = parse_pr_url(pr_url)

        # 2. Connect to GitHub
        github = Github()

        repo = github.get_repo(f"{owner}/{repo_name}")
        pull_request = repo.get_pull(pr_number)

        # 3. Get changed files
        files = pull_request.get_files()

        reviews = []

        # 4. Send each changed file to Ollama
        for file in files:

            # Only review Python files
            if not file.filename.endswith(".py"):
                continue

            patch = file.patch

            if not patch:
                continue

            prompt = f"""
You are an expert Python code reviewer.

Review the following GitHub Pull Request change.

File:
{file.filename}

Changed code:
{patch}

Find:

1. Bugs
2. Security issues
3. Performance issues
4. Code quality problems
5. Suggestions for improvement

Give a clear and concise review.
"""

            # 5. Call Ollama
            async with httpx.AsyncClient(timeout=600.0) as client:

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
                    detail=f"Ollama returned {response.status_code}"
                )

            data = response.json()

            review = data.get("response")

            if review:
                reviews.append({
                    "filename": file.filename,
                    "review": review
                })

        return {
            "repository": f"{owner}/{repo_name}",
            "pull_request": pr_number,
            "title": pull_request.title,
            "reviews": reviews
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Could not connect to Ollama: {repr(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )