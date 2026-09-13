import { useState } from "react";
import { runPlanner, runScriptwriter } from "../../api/client";
import OutputBlock, { Spinner, Alert } from "../OutputBlock";

const PLATFORMS = ["YouTube", "YouTube Shorts", "Instagram Reels", "TikTok"];
const CONTENT_TYPES = ["Educational", "Entertainment", "Motivational", "How-To / Tutorial", "Storytelling"];
const TONES = ["Informative", "Casual", "Professional", "Humorous", "Inspirational"];
const LENGTHS_OPTIONS = ["30 seconds", "60 seconds", "3–5 minutes", "10 minutes", "20 minutes"];
const LENGTHS = [
  "30 s (~75 words)",
  "60 s (~150 words)",
  "3 min (~450 words)",
  "10 min (~1,500 words)",
  "20 min (~3,000 words)",
];

type Step = "topic" | "pick" | "length" | "result";

interface Props { onSave: (title: string, content: string) => void; }

export default function VideoScriptGenerator({ onSave }: Props) {
  const [step, setStep] = useState<Step>("topic");
  const [platform, setPlatform] = useState(PLATFORMS[0]);
  const [contentType, setContentType] = useState(CONTENT_TYPES[0]);
  const [niche, setNiche] = useState("");
  const [audience, setAudience] = useState("");
  const [tone, setTone] = useState(TONES[0]);
  const [lengthIdx, setLengthIdx] = useState(2);
  const [includeHook, setIncludeHook] = useState(true);
  const [scenesuggestions, setSceneSuggestions] = useState(true);
  const [ideas, setIdeas] = useState("");
  const [chosen, setChosen] = useState("");
  const [script, setScript] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const reset = () => { setStep("topic"); setIdeas(""); setChosen(""); setScript(""); setError(""); setNiche(""); setAudience(""); };

  const generateIdeas = async () => {
    if (!niche.trim() || !audience.trim()) { setError("Please fill in both topic and audience."); return; }
    setError(""); setLoading(true);
    try {
      const res = await runPlanner(niche.trim(), platform, audience.trim());
      setIdeas(res.result); setStep("pick");
    } catch (e: any) { setError(e.message); }
    finally { setLoading(false); }
  };

  const generateScript = async () => {
    setError(""); setLoading(true);
    try {
      const res = await runScriptwriter(chosen.trim(), platform, LENGTHS[lengthIdx]);
      setScript(res.result);
      onSave(chosen.trim(), res.result);
      setStep("result");
    } catch (e: any) { setError(e.message); }
    finally { setLoading(false); }
  };

  return (
    <div className="main-content fade-in">
      {/* ── Step 1: Topic ── */}
      {step === "topic" && (
        <div className="tool-card">
          <div className="tool-card-header">
            <div className="tool-card-title-row">
              <div className="tool-card-icon">🎬</div>
              <div>
                <div className="tool-card-title">Video Script Generator</div>
                <div className="tool-card-desc">Research a niche, pick a high-potential concept, and get a production-ready script in seconds.</div>
              </div>
            </div>
          </div>

          <div className="breadcrumb">
            <div className="bc-step active"><span className="bc-num">1</span><span>Topic</span></div>
            <span className="bc-sep">›</span>
            <div className="bc-step"><span className="bc-num">2</span><span>Pick idea</span></div>
            <span className="bc-sep">›</span>
            <div className="bc-step"><span className="bc-num">3</span><span>Script</span></div>
          </div>

          {error && <Alert type="error" message={error} />}

          <div className="form-grid-2">
            <div className="form-group">
              <label className="form-label">Platform</label>
              <select className="form-select" value={platform} onChange={e => setPlatform(e.target.value)}>
                {PLATFORMS.map(p => <option key={p}>{p}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Content Type</label>
              <select className="form-select" value={contentType} onChange={e => setContentType(e.target.value)}>
                {CONTENT_TYPES.map(c => <option key={c}>{c}</option>)}
              </select>
            </div>
          </div>

          <div className="form-grid-2">
            <div className="form-group">
              <label className="form-label">Topic / Niche</label>
              <input id="niche-input" className="form-input" placeholder="e.g. Personal finance, AI tools, fitness, real estate…" value={niche} onChange={e => setNiche(e.target.value)} />
            </div>
            <div className="form-group">
              <label className="form-label">Target Audience</label>
              <input id="audience-input" className="form-input" placeholder="e.g. Working professionals, 25–35, building passive income…" value={audience} onChange={e => setAudience(e.target.value)} />
            </div>
          </div>

          <div className="prefs-label">Additional Preferences <span className="opt">(Optional)</span></div>
          <div className="prefs-row">
            <div className="pref-chip">
              <span className="chip-icon">✦</span>
              Tone
              <select value={tone} onChange={e => setTone(e.target.value)}>
                {TONES.map(t => <option key={t}>{t}</option>)}
              </select>
            </div>
            <div className="pref-chip">
              <span className="chip-icon">⏱</span>
              Length
              <select value={LENGTHS_OPTIONS[lengthIdx]} onChange={e => setLengthIdx(LENGTHS_OPTIONS.indexOf(e.target.value))}>
                {LENGTHS_OPTIONS.map(l => <option key={l}>{l}</option>)}
              </select>
            </div>
            <div className="toggle-group">
              Include Hook
              <div className={`toggle${includeHook ? " on" : ""}`} onClick={() => setIncludeHook(!includeHook)} />
            </div>
            <div className="toggle-group">
              Scene Suggestions
              <div className={`toggle${scenesuggestions ? " on" : ""}`} onClick={() => setSceneSuggestions(!scenesuggestions)} />
            </div>
          </div>

          <button id="generate-ideas-btn" className="btn btn-primary btn-wide" onClick={generateIdeas} disabled={loading}>
            {loading ? "Researching…" : "✦ Generate Ideas →"}
          </button>
          {loading && <Spinner label="Researching trends and ideas…" />}
        </div>
      )}

      {/* ── Step 2: Pick ── */}
      {step === "pick" && (
        <div className="tool-card">
          <div className="tool-card-header">
            <div className="tool-card-title-row">
              <div className="tool-card-icon">🎬</div>
              <div>
                <div className="tool-card-title">Video Script Generator</div>
                <div className="tool-card-desc">Pick your favourite concept below.</div>
              </div>
            </div>
          </div>

          <div className="breadcrumb">
            <div className="bc-step"><span className="bc-num">1</span><span>Topic</span></div>
            <span className="bc-sep">›</span>
            <div className="bc-step active"><span className="bc-num">2</span><span>Pick idea</span></div>
            <span className="bc-sep">›</span>
            <div className="bc-step"><span className="bc-num">3</span><span>Script</span></div>
          </div>

          {error && <Alert type="error" message={error} />}
          <div className="output-block" style={{ maxHeight: "40vh", marginBottom: 20 }}>{ideas}</div>
          <div className="form-group" style={{ marginBottom: 20 }}>
            <label className="form-label">Which concept do you want to script?</label>
            <input id="chosen-concept-input" className="form-input" placeholder="Paste or type the concept title…" value={chosen} onChange={e => setChosen(e.target.value)} />
          </div>
          <div className="btn-row">
            <button className="btn btn-ghost" onClick={() => setStep("topic")}>← Back</button>
            <button className="btn btn-primary" style={{ flex: 1 }} onClick={() => { if (chosen.trim()) setStep("length"); else setError("Enter a concept title."); }}>Continue →</button>
          </div>
        </div>
      )}

      {/* ── Step 3: Length picker ── */}
      {step === "length" && (
        <div className="tool-card">
          <div className="tool-card-header">
            <div className="tool-card-title-row">
              <div className="tool-card-icon">🎬</div>
              <div>
                <div className="tool-card-title">Video Script Generator</div>
                <div className="tool-card-desc">Choose the length for your script.</div>
              </div>
            </div>
          </div>

          <div className="breadcrumb">
            <div className="bc-step"><span className="bc-num">1</span><span>Topic</span></div>
            <span className="bc-sep">›</span>
            <div className="bc-step"><span className="bc-num">2</span><span>Pick idea</span></div>
            <span className="bc-sep">›</span>
            <div className="bc-step active"><span className="bc-num">3</span><span>Script</span></div>
          </div>

          {error && <Alert type="error" message={error} />}
          <div className="form-group" style={{ marginBottom: 24 }}>
            <label className="form-label">Target Length</label>
            <div className="radio-group">
              {LENGTHS.map((l, i) => (
                <label key={l} className={`radio-item${lengthIdx === i ? " selected" : ""}`}>
                  <input type="radio" checked={lengthIdx === i} onChange={() => setLengthIdx(i)} />
                  <span className="radio-label">{l}</span>
                </label>
              ))}
            </div>
          </div>
          <div className="btn-row">
            <button className="btn btn-ghost" onClick={() => setStep("pick")}>← Back</button>
            <button id="write-script-btn" className="btn btn-primary" style={{ flex: 1 }} onClick={generateScript} disabled={loading}>
              {loading ? "Writing…" : "Write script →"}
            </button>
          </div>
          {loading && <Spinner label="Writing your production-ready script…" />}
        </div>
      )}

      {/* ── Result ── */}
      {step === "result" && (
        <OutputBlock title="Video Script" content={script} onReset={reset} />
      )}
    </div>
  );
}
