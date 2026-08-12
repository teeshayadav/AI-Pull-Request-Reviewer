import { useState } from "react";
import "./App.css";

function App() {
  const [prUrl, setPrUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const reviewPullRequest = async () => {
    if (!prUrl.trim()) {
      setError("Please enter a GitHub Pull Request URL.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/github/review-pr?pr_url=${encodeURIComponent(
          prUrl
        )}`,
        {
          method: "POST",
          headers: {
            Accept: "application/json",
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to review Pull Request");
      }

      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="hero">
        <div className="robot">🤖</div>
        <h1>AI Pull Request Reviewer</h1>
        <p>
          Review your GitHub Pull Request using AI
        </p>
      </header>

      <main className="container">
        <section className="review-box">
          <h2>🔗 Enter GitHub Pull Request</h2>

          <input
            type="text"
            value={prUrl}
            onChange={(e) => setPrUrl(e.target.value)}
            placeholder="https://github.com/username/repository/pull/1"
          />

          <button onClick={reviewPullRequest} disabled={loading}>
            {loading ? "🤖 Reviewing..." : "🔍 Review Pull Request"}
          </button>
        </section>

        {error && (
          <div className="error">
            ❌ {error}
          </div>
        )}

        {result && (
          <section className="results">
            <div className="repo-info">
              <h2>📋 AI Review Results</h2>

              <p>
                <strong>Repository:</strong>{" "}
                {result.repository}
              </p>

              <p>
                <strong>Pull Request:</strong> #{result.pull_request}
              </p>

              <p>
                <strong>Title:</strong> {result.title}
              </p>
            </div>

            {result.reviews.length === 0 ? (
              <div className="no-review">
                ℹ️ No Python files were found to review.
              </div>
            ) : (
              result.reviews.map((item, index) => (
                <div className="review-card" key={index}>
                  <h3>🐍 {item.filename}</h3>

                  <div className="review-content">
                    {item.review.split("\n").map((line, i) => (
                      <p key={i}>
                        {line || "\u00A0"}
                      </p>
                    ))}
                  </div>
                </div>
              ))
            )}
          </section>
        )}
      </main>
    </div>
  );
}

export default App;