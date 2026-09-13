import { useState } from "react";
import { runHookGenerator } from "../../api/client";
import OutputBlock, { Spinner, Alert } from "../OutputBlock";

const PLATFORMS = ["TikTok", "Instagram Reels", "YouTube Shorts", "Twitter / X", "LinkedIn"];
const TONES = ["Curiosity Gap", "Controversial / Bold", "Pain Point / Solution", "Storytelling"];

const PlatformIcon = ({ platform }: { platform: string }) => {
  if (platform.includes("YouTube")) return <svg viewBox="0 0 24 24" fill="#ff0000"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33 2.78 2.78 0 0 0 1.94 2c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.33 29 29 0 0 0-.46-5.33z"/><polygon fill="white" points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"/></svg>;
  if (platform.includes("TikTok")) return <svg viewBox="0 0 24 24" fill="black"><path d="M12.53.02C13.84 0 15.14.01 16.44 0c.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 2.23-.9 4.4-2.33 6.16-1.4 1.7-3.4 2.87-5.59 3.23-2.18.35-4.47.07-6.42-1.02-1.97-1.1-3.47-2.9-4.14-5.02-.68-2.15-.49-4.52.48-6.52 1-2 2.8-3.56 4.95-4.3 2.11-.73 4.45-.69 6.51.09V13.6c-1.3-.44-2.77-.38-4.01.2-1.25.59-2.2 1.7-2.6 3.01-.4 1.3-.23 2.74.45 3.9.68 1.15 1.88 1.95 3.24 2.18 1.34.22 2.74-.03 3.87-.77 1.13-.75 1.86-1.96 2.1-3.3.06-.32.08-.66.08-.99V.02z"/></svg>;
  if (platform.includes("Instagram")) return <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>;
  if (platform.includes("Twitter") || platform.includes("X")) return <svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>;
  if (platform.includes("LinkedIn")) return <svg viewBox="0 0 24 24" fill="#0077b5"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>;
  return <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/></svg>;
};

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
            <div className="select-icon-wrap">
              <span className="input-icon"><PlatformIcon platform={platform} /></span>
              <select className="form-select" value={platform} onChange={e => setPlatform(e.target.value)}>
                {PLATFORMS.map(p => <option key={p}>{p}</option>)}
              </select>
            </div>
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
