import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode

from app.core.config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET


router = APIRouter()

github_access_token = None


@router.get("/login")
def github_login():
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "redirect_uri": "http://127.0.0.1:8000/auth/github/callback",
        "scope": "repo",
    }

    github_url = "https://github.com/login/oauth/authorize?" + urlencode(params)

    return RedirectResponse(url=github_url)


@router.get("/callback")
async def github_callback(code: str):
    global github_access_token

    token_url = "https://github.com/login/oauth/access_token"

    data = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
    }

    headers = {
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            token_url,
            data=data,
            headers=headers
        )

    token_data = response.json()

    access_token = token_data.get("access_token")

    if not access_token:
        raise HTTPException(
            status_code=400,
            detail="Could not get GitHub access token"
        )

    github_access_token = access_token

    return {
        "message": "GitHub authentication successful!",
        "token_received": True
    }


@router.get("/me")
async def github_me():
    if not github_access_token:
        raise HTTPException(
            status_code=401,
            detail="Please login with GitHub first"
        )

    headers = {
        "Authorization": f"Bearer {github_access_token}",
        "Accept": "application/vnd.github+json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user",
            headers=headers
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch GitHub user"
        )

    user = response.json()

    return {
        "login": user.get("login"),
        "name": user.get("name"),
        "public_repos": user.get("public_repos"),
        "profile_url": user.get("html_url")
    }

@router.get("/repos")
async def github_repos():
    if not github_access_token:
        raise HTTPException(
            status_code=401,
            detail="Please login with GitHub first"
        )

    headers = {
        "Authorization": f"Bearer {github_access_token}",
        "Accept": "application/vnd.github+json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user/repos",
            headers=headers,
            params={
                "sort": "updated",
                "per_page": 20
            }
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch repositories"
        )

    repositories = response.json()

    return [
        {
            "name": repo.get("name"),
            "full_name": repo.get("full_name"),
            "private": repo.get("private"),
            "html_url": repo.get("html_url")
        }
        for repo in repositories
    ]

@router.get("/repos/{owner}/{repo}/pulls")
async def github_pull_requests(owner: str, repo: str):

    if not github_access_token:
        raise HTTPException(
            status_code=401,
            detail="Please login with GitHub first"
        )

    headers = {
        "Authorization": f"Bearer {github_access_token}",
        "Accept": "application/vnd.github+json"
    }

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=headers,
            params={
                "state": "open",
                "per_page": 20
            }
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch pull requests"
        )

    pull_requests = response.json()

    return [
        {
            "number": pr.get("number"),
            "title": pr.get("title"),
            "state": pr.get("state"),
            "user": pr.get("user", {}).get("login"),
            "html_url": pr.get("html_url")
        }
        for pr in pull_requests
    ]

@router.get("/repos/{owner}/{repo}/pulls/{pr_number}/files")
async def github_pull_request_files(
    owner: str,
    repo: str,
    pr_number: int
):
    if not github_access_token:
        raise HTTPException(
            status_code=401,
            detail="Please login with GitHub first"
        )

    headers = {
        "Authorization": f"Bearer {github_access_token}",
        "Accept": "application/vnd.github+json"
    }

    url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/pulls/{pr_number}/files"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=headers,
            params={
                "per_page": 30
            }
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch pull request files"
        )

    files = response.json()

    return [
        {
            "filename": file.get("filename"),
            "status": file.get("status"),
            "additions": file.get("additions"),
            "deletions": file.get("deletions"),
            "changes": file.get("changes"),
            "patch": file.get("patch")
        }
        for file in files
    ]