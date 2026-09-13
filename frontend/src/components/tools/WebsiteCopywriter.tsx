import { useState } from "react";
import { runWebsiteCopy } from "../../api/client";
import OutputBlock, { Spinner, Alert } from "../OutputBlock";

const TONES = ["Modern & Confident", "Friendly & Approachable", "Luxury & Exclusive", "Direct & Punchy"];

interface Props { onSave: (title: string, content: string) => void; }

export default function WebsiteCopywriter({ onSave }: Props) {
  const [product, setProduct]   = useState("");
  const [audience, setAudience] = useState("");
  const [tone, setTone]         = useState(TONES[0]);
  const [usp, setUsp]           = useState("");
  const [result, setResult]     = useState("");
  const [loading, setLoading]   = useState(false);
  const [error, setError]       = useState("");

  const reset = () => { setResult(""); setError(""); setProduct(""); setAudience(""); setUsp(""); };

  const generate = async () => {
    if (!product.trim() || !usp.trim()) { setError("Please fill in product name and USP."); return; }
    setError(""); setLoading(true);
    try {
      const res = await runWebsiteCopy(product.trim(), audience.trim(), tone, usp.trim());
      setResult(res.result);
      onSave(product.trim(), res.result);
    } catch (e: any) { setError(e.message); }
    finally { setLoading(false); }
  };

  if (result) return (
    <div className="main-content fade-in">
      <OutputBlock title="Website Copy" content={result} onReset={reset} />
    </div>
  );

  return (
    <div className="main-content fade-in">
      <div className="tool-card">
        <div className="tool-card-header">
          <div className="tool-card-title-row">
            <div className="tool-card-icon">🌐</div>
            <div>
              <div className="tool-card-title">Website Copywriter</div>
              <div className="tool-card-desc">Write high-converting landing page copy with a structured layout.</div>
            </div>
          </div>
        </div>

        {error && <Alert type="error" message={error} />}

        <div className="form-grid-2">
          <div className="form-group">
            <label className="form-label">Product / Service Name</label>
            <input className="form-input" placeholder="e.g. Pistelle Analytics" value={product} onChange={e => setProduct(e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Target Customer</label>
            <input className="form-input" placeholder="e.g. SaaS founders" value={audience} onChange={e => setAudience(e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Brand Tone</label>
            <select className="form-select" value={tone} onChange={e => setTone(e.target.value)}>
              {TONES.map(t => <option key={t}>{t}</option>)}
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Unique Selling Point</label>
            <input className="form-input" placeholder="e.g. The only tool that tracks X natively" value={usp} onChange={e => setUsp(e.target.value)} />
          </div>
        </div>

        <button className="btn btn-primary btn-wide" onClick={generate} disabled={loading}>
          {loading ? "Writing…" : "✦ Write website copy →"}
        </button>
        {loading && <Spinner label="Crafting your landing page copy…" />}
      </div>
    </div>
  );
}
