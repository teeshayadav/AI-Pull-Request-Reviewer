from fastapi import APIRouter, HTTPException
from github import Github
from urllib.parse import urlparse

router = APIRouter()


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
        owner, repo_name, pr_number = parse_pr_url(pr_url)

        github = Github()

        repo = github.get_repo(f"{owner}/{repo_name}")
        pull_request = repo.get_pull(pr_number)

        files = pull_request.get_files()

        changed_files = []

        for file in files:
            changed_files.append({
                "filename": file.filename,
                "status": file.status,
                "additions": file.additions,
                "deletions": file.deletions,
                "patch": file.patch
            })

        return {
            "repository": f"{owner}/{repo_name}",
            "pull_request": pr_number,
            "title": pull_request.title,
            "files": changed_files
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )