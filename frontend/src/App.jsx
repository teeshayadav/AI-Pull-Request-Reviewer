import { useState } from "react";
import "./App.css";

function App() {
  const [code, setCode] = useState("");
  const [review, setReview] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const reviewCode = async () => {
    if (!code.trim()) {
      setError("Please enter some code first.");
      return;
    }

    setLoading(true);
    setReview("");
    setError("");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/ai/review?code=${encodeURIComponent(code)}`,
        {
          method: "POST",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Something went wrong");
      }

      setReview(data.review);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header>
        <h1>🤖 AI Code Reviewer</h1>
        <p>Review your Python code using AI</p>
      </header>

      <main>
        <div className="editor-section">
          <h2>Enter Your Code</h2>

          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="Paste your Python code here..."
          />

          <button onClick={reviewCode} disabled={loading}>
            {loading ? "Reviewing..." : "🔍 Review Code"}
          </button>
        </div>

        {error && (
          <div className="error">
            ❌ {error}
          </div>
        )}

        {review && (
          <div className="review-section">
            <h2>📋 AI Review</h2>

            <pre>{review}</pre>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;