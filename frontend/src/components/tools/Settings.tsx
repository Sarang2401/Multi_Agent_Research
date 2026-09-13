import { useState } from "react";
import { saveApiKey } from "../../api/client";
import { Alert } from "../OutputBlock";

interface Props { model: string; onApiKeyChange: () => void; }

export default function Settings({ model, onApiKeyChange }: Props) {
  const [newKey, setNewKey]   = useState("");
  const [saving, setSaving]   = useState(false);
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);

  const handleSaveKey = async () => {
    if (!newKey.trim().startsWith("AIza")) { setMessage({ type: "error", text: "A Gemini key starts with 'AIza'." }); return; }
    setSaving(true); setMessage(null);
    try {
      await saveApiKey(newKey.trim());
      setMessage({ type: "success", text: "API key updated successfully." });
      setNewKey("");
      onApiKeyChange();
    } catch (e: any) {
      setMessage({ type: "error", text: e.message });
    } finally { setSaving(false); }
  };

  return (
    <div className="main-content fade-in">
      <h1 className="page-title">Settings</h1>
      <p className="page-lead">Configure your Pistelle AI workspace.</p>
      <hr className="page-divider" />

      {message && <Alert type={message.type} message={message.text} />}

      <div className="settings-section">
        <div className="settings-section-title">AI Configuration</div>
        <div className="settings-row">
          <div>
            <div className="settings-label">Active Model</div>
            <div className="settings-desc">The Gemini model used for all generations</div>
          </div>
          <span style={{ fontSize: 13, color: "var(--t1)", fontWeight: 600, background: "var(--raised)", border: "1px solid var(--border)", padding: "4px 10px", borderRadius: 6 }}>
            {model}
          </span>
        </div>
        <div className="settings-row" style={{ flexDirection: "column", alignItems: "flex-start", gap: 12 }}>
          <div>
            <div className="settings-label">Update API Key</div>
            <div className="settings-desc">Replace the currently stored Gemini API key</div>
          </div>
          <div style={{ display: "flex", gap: 10, width: "100%" }}>
            <input
              id="settings-api-key-input"
              className="form-input"
              type="password"
              placeholder="AIzaSy…"
              value={newKey}
              onChange={e => setNewKey(e.target.value)}
              style={{ maxWidth: 340 }}
            />
            <button id="settings-save-key-btn" className="btn btn-primary" onClick={handleSaveKey} disabled={saving} style={{ padding: "8px 16px" }}>
              {saving ? "Saving…" : "Update Key"}
            </button>
          </div>
        </div>
      </div>

      <div className="settings-section">
        <div className="settings-section-title">About</div>
        <div className="settings-row">
          <div className="settings-label">Pistelle AI</div>
          <span style={{ fontSize: 12, color: "var(--t3)", fontWeight: 500 }}>v2.0 — React Edition</span>
        </div>
        <div className="settings-row">
          <div>
            <div className="settings-label">Data Privacy</div>
            <div className="settings-desc">Your API key is stored locally in a <code style={{ fontSize: 11, background: "var(--raised)", border: "1px solid var(--border)", padding: "2px 6px", borderRadius: 4 }}>.env</code> file. No data is ever collected.</div>
          </div>
        </div>
      </div>
    </div>
  );
}
