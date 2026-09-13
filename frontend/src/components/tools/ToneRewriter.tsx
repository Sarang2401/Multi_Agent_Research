import { useState } from "react";
import { runToneRewriter } from "../../api/client";
import OutputBlock, { Spinner, Alert } from "../OutputBlock";

const TONES = ["More Professional", "More Casual & Friendly", "Shorter & Punchier", "Persuasive / Sales", "Emphatic / Emotional"];

interface Props { onSave: (title: string, content: string) => void; }

export default function ToneRewriter({ onSave }: Props) {
  const [text, setText]       = useState("");
  const [tone, setTone]       = useState(TONES[0]);
  const [context, setContext] = useState("");
  const [result, setResult]   = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState("");

  const reset = () => { setResult(""); setError(""); setText(""); setContext(""); };

  const generate = async () => {
    if (!text.trim()) { setError("Please provide the text you want to rewrite."); return; }
    setError(""); setLoading(true);
    try {
      const res = await runToneRewriter(text.trim(), tone, context.trim());
      setResult(res.result);
      onSave("Rewritten Text", res.result);
    } catch (e: any) { setError(e.message); }
    finally { setLoading(false); }
  };

  if (result) return (
    <div className="main-content fade-in">
      <OutputBlock title="Rewritten Text" content={result} onReset={reset} />
    </div>
  );

  return (
    <div className="main-content fade-in">
      <div className="tool-card">
        <div className="tool-card-header">
          <div className="tool-card-title-row">
            <div className="tool-card-icon">✨</div>
            <div>
              <div className="tool-card-title">Tone Rewriter</div>
              <div className="tool-card-desc">Instantly adapt your copy for a different audience or platform.</div>
            </div>
          </div>
        </div>

        {error && <Alert type="error" message={error} />}

        <div className="form-grid-2">
          <div className="form-group full-width">
            <label className="form-label">Original Text</label>
            <textarea className="form-textarea" placeholder="Paste the text you want to rewrite here..." style={{ minHeight: 120 }} value={text} onChange={e => setText(e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Target Tone</label>
            <select className="form-select" value={tone} onChange={e => setTone(e.target.value)}>
              {TONES.map(t => <option key={t}>{t}</option>)}
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Context <span className="opt">(Optional)</span></label>
            <input className="form-input" placeholder="e.g. This is for an email to our CEO" value={context} onChange={e => setContext(e.target.value)} />
          </div>
        </div>

        <button className="btn btn-primary btn-wide" onClick={generate} disabled={loading} style={{ marginTop: 8 }}>
          {loading ? "Rewriting…" : "✦ Rewrite Text →"}
        </button>
        {loading && <Spinner label="Analyzing and rewriting text…" />}
      </div>
    </div>
  );
}
