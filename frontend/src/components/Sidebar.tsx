import React from "react";

export type View =
  | "Dashboard"
  | "Video Script Generator"
  | "SEO Blog Writer"
  | "Website Copywriter"
  | "Product Description"
  | "Viral Hook Generator"
  | "Tone Rewriter"
  | "Session History"
  | "Settings";

interface SidebarProps {
  current: View;
  onNavigate: (v: View) => void;
}

/* ── SVG icon components (stroke-based, matching the reference) ─────────── */
const icons: Record<string, React.ReactNode> = {
  Dashboard: <svg viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>,
  "Video Script Generator": <svg viewBox="0 0 24 24"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>,
  "SEO Blog Writer": <svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>,
  "Website Copywriter": <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>,
  "Product Description": <svg viewBox="0 0 24 24"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>,
  "Viral Hook Generator": <svg viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>,
  "Tone Rewriter": <svg viewBox="0 0 24 24"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>,
  "Session History": <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>,
  Settings: <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>,
};

const NAV_TOOLS: View[] = [
  "Dashboard",
  "Video Script Generator",
  "SEO Blog Writer",
  "Website Copywriter",
  "Product Description",
  "Viral Hook Generator",
  "Tone Rewriter",
];

const NAV_BOTTOM: View[] = ["Session History", "Settings"];

export default function Sidebar({ current, onNavigate }: SidebarProps) {
  return (
    <aside className="sidebar">
      {/* Brand */}
      <div className="sidebar-brand">
        <img src="/logo.png" alt="Pistelle AI" className="sidebar-logo" />
        <div className="sidebar-brand-text">
          <span className="sidebar-wordmark">Pistelle AI</span>
          <span className="sidebar-tagline">Content · Automation · Growth</span>
        </div>
      </div>

      {/* Main Nav */}
      <nav className="sidebar-nav">
        {NAV_TOOLS.map((label) => (
          <button
            key={label}
            className={`nav-btn${current === label ? " active" : ""}`}
            onClick={() => onNavigate(label)}
          >
            <span className="nav-icon">{icons[label]}</span>
            {label}
          </button>
        ))}
      </nav>

      {/* Bottom Nav */}
      <div className="sidebar-footer">
        {NAV_BOTTOM.map((label) => (
          <button
            key={label}
            className={`nav-btn${current === label ? " active" : ""}`}
            onClick={() => onNavigate(label)}
          >
            <span className="nav-icon">{icons[label]}</span>
            {label}
          </button>
        ))}
      </div>
    </aside>
  );
}
