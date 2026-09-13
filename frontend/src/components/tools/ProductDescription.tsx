import { useState } from "react";
import { runProductDesc } from "../../api/client";
import OutputBlock, { Spinner, Alert } from "../OutputBlock";

const TYPES = ["Physical Product", "Digital Product / SaaS", "Service"];
const TONES = ["Benefit-Driven", "Feature-Heavy", "Luxury / Premium", "Short & Punchy"];

interface Props { onSave: (title: string, content: string) => void; }

export default function ProductDescription({ onSave }: Props) {
  const [product, setProduct] = useState("");
  const [type, setType]       = useState(TYPES[0]);
  const [features, setFeatures] = useState("");
  const [tone, setTone]       = useState(TONES[0]);
  const [result, setResult]   = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState("");

  const reset = () => { setResult(""); setError(""); setProduct(""); setFeatures(""); };

  const generate = async () => {
    if (!product.trim() || !features.trim()) { setError("Please fill in product name and features."); return; }
    setError(""); setLoading(true);
    try {
      const res = await runProductDesc(product.trim(), type, features.trim(), tone, "E-commerce");
      setResult(res.result);
      onSave(product.trim(), res.result);
    } catch (e: any) { setError(e.message); }
    finally { setLoading(false); }
  };

  if (result) return (
    <div className="main-content fade-in">
      <OutputBlock title="Product Description" content={result} onReset={reset} />
    </div>
  );

  return (
    <div className="main-content fade-in">
      <div className="tool-card">
        <div className="tool-card-header">
          <div className="tool-card-title-row">
            <div className="tool-card-icon">🛍️</div>
            <div>
              <div className="tool-card-title">Product Description</div>
              <div className="tool-card-desc">Create compelling, benefit-driven product descriptions for ecommerce.</div>
            </div>
          </div>
        </div>

        {error && <Alert type="error" message={error} />}

        <div className="form-grid-2">
          <div className="form-group">
            <label className="form-label">Product Name</label>
            <input className="form-input" placeholder="e.g. Ergonomic Office Chair X1" value={product} onChange={e => setProduct(e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Product Type</label>
            <select className="form-select" value={type} onChange={e => setType(e.target.value)}>
              {TYPES.map(t => <option key={t}>{t}</option>)}
            </select>
          </div>
          <div className="form-group full-width">
            <label className="form-label">Key Features</label>
            <textarea className="form-textarea" placeholder="e.g. Lumbar support, breathable mesh, adjustable armrests..." value={features} onChange={e => setFeatures(e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Tone</label>
            <select className="form-select" value={tone} onChange={e => setTone(e.target.value)}>
              {TONES.map(t => <option key={t}>{t}</option>)}
            </select>
          </div>
        </div>

        <button className="btn btn-primary btn-wide" onClick={generate} disabled={loading} style={{ marginTop: 8 }}>
          {loading ? "Writing…" : "✦ Generate Description →"}
        </button>
        {loading && <Spinner label="Writing product description…" />}
      </div>
    </div>
  );
}
