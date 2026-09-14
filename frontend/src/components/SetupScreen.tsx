import React, { useState } from "react";
import { saveApiKey } from "../api/client";

interface SetupScreenProps {
  onConnected: () => void;
}

export default function SetupScreen({ onConnected }: SetupScreenProps) {
  const [key, setKey] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showHint, setShowHint] = useState(false);

  const handleConnect = async () => {
    setError("");
    if (!key.trim()) { setError("Please paste your API key above."); return; }
    if (!key.trim().startsWith("AIza")) { setError("A Gemini key starts with 'AIza'."); return; }
    setLoading(true);
    try {
      await saveApiKey(key.trim());
      onConnected();
    } catch (e: any) {
      setError(e.message ?? "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="setup-fullscreen">
      <div className="setup-wrap fade-in">
        <div className="setup-brand">
          <img src="/logo.png" alt="Pistelle AI" style={{ height: 80, objectFit: "contain" }} />
          <p style={{ marginTop: 8, fontSize: 13 }}>Content Intelligence Suite</p>
        </div>

        <div className="setup-card">
          <h2>Connect your AI engine</h2>
          <p style={{ marginTop: 8 }}>
            Pistelle AI runs on your machine using the free Gemini API.
            No subscription, no data leaves your device.
          </p>
        </div>

        <button
          className="btn btn-ghost btn-wide"
          style={{ marginBottom: 12, justifyContent: "flex-start" }}
          onClick={() => setShowHint(!showHint)}
        >
          {showHint ? "▲" : "▶"} &nbsp;How to get a free API key
        </button>

        {showHint && (
          <div className="setup-hint fade-in">
            <p>
              1. Open <a href="https://aistudio.google.com/apikey" target="_blank" rel="noreferrer" style={{ color: "#7c3aed", fontWeight: 500 }}>aistudio.google.com/apikey</a><br />
              2. Sign in with any Google account<br />
              3. Click <strong>Create API Key</strong><br />
              4. Copy the key — it starts with <code>AIzaSy…</code>
            </p>
          </div>
        )}

        {error && <div className="alert alert-error">{error}</div>}

        <div className="form-group" style={{ marginBottom: 12 }}>
          <input
            id="api-key-input"
            className="form-input"
            type="password"
            placeholder="AIzaSy…"
            value={key}
            onChange={(e) => setKey(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleConnect()}
          />
        </div>

        <button
          id="connect-btn"
          className="btn btn-primary btn-wide"
          onClick={handleConnect}
          disabled={loading}
        >
          {loading ? "Connecting…" : "Connect →"}
        </button>

        <div className="setup-trust-row">
          <div className="setup-trust-item"><span className="ok">✓</span> Key stored in <code style={{ fontSize: 11, background: "#f5f5f5", padding: "1px 5px", borderRadius: 3 }}>.env</code> on this machine only</div>
          <div className="setup-trust-item"><span className="ok">✓</span> No platform fees — free Gemini tier</div>
          <div className="setup-trust-item"><span className="ok">✓</span> Your PC calls the Google AI API directly</div>
        </div>
      </div>
    </div>
  );
}
