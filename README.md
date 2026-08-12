# 🤖 AI Pull Request Reviewer

An AI-powered code review tool that analyzes GitHub Pull Requests and provides automated feedback on Python code using FastAPI, React, and Ollama.

## ✨ Features

- 🔗 Enter any GitHub Pull Request URL
- 📂 Automatically fetch changed files from the Pull Request
- 🐍 Analyze Python files
- 🤖 AI-powered code review using Ollama
- 🐛 Detect potential bugs
- 🔒 Identify security issues
- ⚡ Find performance problems
- 🧹 Review code quality
- 💡 Provide improvement suggestions
- 🎨 Clean React-based interface
- ⚡ FastAPI backend

## 🏗️ How It Works

```text
GitHub Pull Request URL
          ↓
      React Frontend
          ↓
      FastAPI Backend
          ↓
      GitHub API
          ↓
   Changed Python Files
          ↓
        Ollama
          ↓
      AI Code Review
          ↓
      React Frontend
          ↓
       Review Results



## 🛠️ Tech Stack

### Frontend
- React
- Vite
- JavaScript
- CSS

### Backend
- Python
- FastAPI
- PyGithub
- HTTPX

### AI
- Ollama
- Qwen2.5-Coder 3B

### APIs & Tools
- GitHub API
- Git
- GitHub
- VS Code

## 📁 Project Structure

```text
AI-Pull-Request-Reviewer/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── ai_review.py
│   │   │   ├── github_pr.py
│   │   │   └── github_auth.py
│   │   ├── core/
│   │   └── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   ├── package.json
│   └── vite.config.js
│
├── tests/
├── .gitignore
├── PROJECT_PLAN.md
└── README.md