from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.github_auth import router as github_router
from app.api.ai_review import router as ai_review_router
from app.api.github_pr import router as github_pr_router


app = FastAPI(title="AI Pull Request Reviewer")



# Allow React frontend to communicate with FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(github_router, prefix="/auth/github")
app.include_router(ai_review_router, prefix="/ai")
app.include_router(github_pr_router, prefix="/github")



@app.get("/")
def home():
    return {"message": "AI Pull Request Reviewer API is running!"}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Pull Request Reviewer"
    }