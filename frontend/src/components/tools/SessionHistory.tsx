import { useState } from "react";
import type { HistoryEntry } from "../../api/useHistory";

interface Props { history: HistoryEntry[]; }

export default function SessionHistory({ history }: Props) {
  const [expanded, setExpanded] = useState<string | null>(null);

  if (history.length === 0) {
    return (
      <div className="main-content fade-in">
        <h1 className="page-title">Session History</h1>
        <p className="page-lead">Generated content from this session will appear here.</p>
        <hr className="page-divider" />
        <div className="history-empty">
          <div style={{ fontSize: 40, marginBottom: 12, opacity: 0.5 }}>📋</div>
          <p>No outputs generated yet. Use any tool to get started.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="main-content fade-in">
      <h1 className="page-title">Session History</h1>
      <p className="page-lead">{history.length} item{history.length !== 1 ? "s" : ""} generated this session.</p>
      <hr className="page-divider" />

      {history.map((entry) => (
        <div key={entry.id} className="history-card" onClick={() => setExpanded(expanded === entry.id ? null : entry.id)}>
          <div className="history-card-header">
            <span className="history-type">{entry.type}</span>
            <span className="history-time">
              {entry.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
            </span>
          </div>
          <div className="history-title">{entry.title}</div>
          {expanded !== entry.id && (
            <div className="history-preview">
              {entry.content.slice(0, 140).trim()}{entry.content.length > 140 ? "…" : ""}
            </div>
          )}
          {expanded === entry.id && (
            <div className="output-block fade-in" style={{ marginTop: 12 }}>{entry.content}</div>
          )}
        </div>
      ))}
    </div>
  );
}
