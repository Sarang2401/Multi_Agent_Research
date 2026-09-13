import { useState } from "react";
import { runHookGenerator } from "../../api/client";
import OutputBlock, { Spinner, Alert } from "../OutputBlock";

const PLATFORMS = ["TikTok", "Instagram Reels", "YouTube Shorts", "Twitter / X", "LinkedIn"];
const TONES = ["Curiosity Gap", "Controversial / Bold", "Pain Point / Solution", "Storytelling"];

interface Props { onSave: (title: string, content: string) => void; }

export default function ViralHookGenerator({ onSave }: Props) {
  const [topic, setTopic]     = useState("");
  const [platform, setPlatform] = useState(PLATFORMS[0]);
  const [tone, setTone]       = useState(TONES[0]);
  const [result, setResult]   = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState("");

  const reset = () => { setResult(""); setError(""); setTopic(""); };

  const generate = async () => {
    if (!topic.trim()) { setError("Please provide a topic."); return; }
    setError(""); setLoading(true);
    try {
      const res = await runHookGenerator(topic.trim(), platform, tone);
      setResult(res.result);
      onSave(`Hooks: ${topic.trim().slice(0, 20)}`, res.result);
    } catch (e: any) { setError(e.message); }
    finally { setLoading(false); }
  };

  if (result) return (
    <div className="main-content fade-in">
      <OutputBlock title="Viral Hooks" content={result} onReset={reset} />
    </div>
  );

  return (
    <div className="main-content fade-in">
      <div className="tool-card">
        <div className="tool-card-header">
          <div className="tool-card-title-row">
            <div className="tool-card-icon">⚡</div>
            <div>
              <div className="tool-card-title">Viral Hook Generator</div>
              <div className="tool-card-desc">Generate attention-grabbing hooks to stop the scroll.</div>
            </div>
          </div>
        </div>

        {error && <Alert type="error" message={error} />}

        <div className="form-grid-2">
          <div className="form-group full-width">
            <label className="form-label">What is your content about?</label>
            <input className="form-input" placeholder="e.g. Why most startups fail in year one" value={topic} onChange={e => setTopic(e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Platform</label>
            <select className="form-select" value={platform} onChange={e => setPlatform(e.target.value)}>
              {PLATFORMS.map(p => <option key={p}>{p}</option>)}
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Hook Style</label>
            <select className="form-select" value={tone} onChange={e => setTone(e.target.value)}>
              {TONES.map(t => <option key={t}>{t}</option>)}
            </select>
          </div>
        </div>

        <button className="btn btn-primary btn-wide" onClick={generate} disabled={loading} style={{ marginTop: 8 }}>
          {loading ? "Generating…" : "✦ Generate Hooks →"}
        </button>
        {loading && <Spinner label="Brainstorming viral hooks…" />}
      </div>
    </div>
  );
}
