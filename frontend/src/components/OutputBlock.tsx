import React from "react";

interface OutputBlockProps {
  title: string;
  content: string;
  onReset: () => void;
  onCopy?: () => void;
}

export default function OutputBlock({ title, content, onReset }: OutputBlockProps) {
  const [copied, setCopied] = React.useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const wc = content.split(/\s+/).filter(Boolean).length;
  const readSecs = Math.round((wc / 140) * 60);
  const readTime = readSecs < 60 ? `~${readSecs}s` : `~${(readSecs / 60).toFixed(1)} min`;

  return (
    <div className="fade-in">
      <div className="stat-strip" style={{ gridTemplateColumns: "repeat(3,1fr)" }}>
        <div className="stat-cell">
          <div className="stat-k">Type</div>
          <div className="stat-v">{title}</div>
        </div>
        <div className="stat-cell">
          <div className="stat-k">Word Count</div>
          <div className="stat-v stat-v-ok">{wc.toLocaleString()}</div>
        </div>
        <div className="stat-cell">
          <div className="stat-k">Read Time</div>
          <div className="stat-v">{readTime}</div>
        </div>
      </div>

      <div className="output-block">{content}</div>

      <div className="output-actions">
        <button id="copy-output-btn" className="btn btn-ghost" onClick={handleCopy}>
          {copied ? "✓ Copied!" : "📋 Copy"}
        </button>
        <button id="start-over-btn" className="btn btn-ghost" onClick={onReset}>
          ↺ Start Over
        </button>
      </div>
    </div>
  );
}

/* ── Shared Spinner ────────────────────────────────────────────────────────── */
export function Spinner({ label = "Working…" }: { label?: string }) {
  return (
    <div className="spinner-wrap">
      <div className="spinner" />
      <div className="spinner-label">{label}</div>
    </div>
  );
}

/* ── Shared Alert ──────────────────────────────────────────────────────────── */
export function Alert({ type, message }: { type: "error" | "warning" | "success"; message: string }) {
  return <div className={`alert alert-${type}`}>{message}</div>;
}
