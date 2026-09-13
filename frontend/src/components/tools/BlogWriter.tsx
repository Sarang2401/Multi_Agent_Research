import { useState } from "react";
import { runBlogWriter } from "../../api/client";
import OutputBlock, { Spinner, Alert } from "../OutputBlock";

const TONES  = ["Authoritative & Professional", "Conversational & Friendly", "Educational & Simple", "Bold & Opinionated"];
const LENGTHS = ["Short (600 words)", "Standard (1,200 words)", "Long-form (2,500 words)"];

interface Props { onSave: (title: string, content: string) => void; }

export default function BlogWriter({ onSave }: Props) {
  const [topic, setTopic]       = useState("");
  const [audience, setAudience] = useState("");
  const [tone, setTone]         = useState(TONES[0]);
  const [length, setLength]     = useState(LENGTHS[1]);
  const [keywords, setKeywords] = useState("");
  const [result, setResult]     = useState("");
  const [loading, setLoading]   = useState(false);
  const [error, setError]       = useState("");

  const reset = () => { setResult(""); setError(""); setTopic(""); setAudience(""); setKeywords(""); };

  const generate = async () => {
    if (!topic.trim() || !audience.trim()) { setError("Please fill in topic and audience."); return; }
    setError(""); setLoading(true);
    try {
      const res = await runBlogWriter(topic.trim(), audience.trim(), tone, length, keywords.trim());
      setResult(res.result);
      onSave(topic.trim(), res.result);
    } catch (e: any) { setError(e.message); }
    finally { setLoading(false); }
  };

  if (result) return (
    <div className="main-content fade-in">
      <OutputBlock title="Blog Post" content={result} onReset={reset} />
    </div>
  );

  return (
    <div className="main-content fade-in">
      <div className="tool-card">
        <div className="tool-card-header">
          <div className="tool-card-title-row">
            <div className="tool-card-icon">📝</div>
            <div>
              <div className="tool-card-title">SEO Blog Writer</div>
              <div className="tool-card-desc">Generate long-form, structured blog posts tailored for search engines and real readers.</div>
            </div>
          </div>
        </div>

        {error && <Alert type="error" message={error} />}

        <div className="form-grid-2">
          <div className="form-group">
            <label className="form-label">Blog Topic</label>
            <input id="blog-topic-input" className="form-input" placeholder="e.g. 10 ways to improve website conversion rates" value={topic} onChange={e => setTopic(e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Target Reader</label>
            <input id="blog-audience-input" className="form-input" placeholder="e.g. Small business owners" value={audience} onChange={e => setAudience(e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Tone of Voice</label>
            <select className="form-select" value={tone} onChange={e => setTone(e.target.value)}>
              {TONES.map(t => <option key={t}>{t}</option>)}
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Target Length</label>
            <select className="form-select" value={length} onChange={e => setLength(e.target.value)}>
              {LENGTHS.map(l => <option key={l}>{l}</option>)}
            </select>
          </div>
          <div className="form-group full-width">
            <label className="form-label">Target Keywords <span className="opt">(comma separated, optional)</span></label>
            <input id="blog-keywords-input" className="form-input" placeholder="e.g. conversion rate optimization, CRO tools" value={keywords} onChange={e => setKeywords(e.target.value)} />
          </div>
        </div>

        <button id="write-blog-btn" className="btn btn-primary btn-wide" onClick={generate} disabled={loading}>
          {loading ? "Writing…" : "✦ Write blog post →"}
        </button>
        {loading && <Spinner label="Writing your blog post…" />}
      </div>
    </div>
  );
}
