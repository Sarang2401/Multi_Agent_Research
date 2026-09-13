import React from "react";
import type { View } from "./Sidebar";
import type { HistoryEntry } from "../api/useHistory";

interface Props {
  onNavigate: (v: View) => void;
  currentTool: View;
  history: HistoryEntry[];
}

const USE_CASES: { label: string; desc: string; icon: React.ReactNode; target: View }[] = [
  { 
    label: "YouTube Explainer", 
    desc: "How to use Notion for content planning", 
    icon: <svg viewBox="0 0 24 24" fill="#ff0000" width="20" height="20"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33 2.78 2.78 0 0 0 1.94 2c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.33 29 29 0 0 0-.46-5.33z"/><polygon fill="white" points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"/></svg>,
    target: "Video Script Generator"
  },
  { 
    label: "Instagram Reel", 
    desc: "5 AI tools every creator should use in 2026", 
    icon: <svg viewBox="0 0 24 24" fill="none" stroke="#e1306c" strokeWidth="2" width="20" height="20"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>,
    target: "Viral Hook Generator"
  },
  { 
    label: "TikTok Script", 
    desc: "Morning habits for productivity", 
    icon: <svg viewBox="0 0 24 24" fill="black" width="20" height="20"><path d="M12.53.02C13.84 0 15.14.01 16.44 0c.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 2.23-.9 4.4-2.33 6.16-1.4 1.7-3.4 2.87-5.59 3.23-2.18.35-4.47.07-6.42-1.02-1.97-1.1-3.47-2.9-4.14-5.02-.68-2.15-.49-4.52.48-6.52 1-2 2.8-3.56 4.95-4.3 2.11-.73 4.45-.69 6.51.09V13.6c-1.3-.44-2.77-.38-4.01.2-1.25.59-2.2 1.7-2.6 3.01-.4 1.3-.23 2.74.45 3.9.68 1.15 1.88 1.95 3.24 2.18 1.34.22 2.74-.03 3.87-.77 1.13-.75 1.86-1.96 2.1-3.3.06-.32.08-.66.08-.99V.02z"/></svg>,
    target: "Video Script Generator"
  },
  { 
    label: "LinkedIn Thought Piece", 
    desc: "The future of remote work in 2026", 
    icon: <svg viewBox="0 0 24 24" fill="#0077b5" width="20" height="20"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>,
    target: "Tone Rewriter"
  },
];

export default function Dashboard({ onNavigate, currentTool, history }: Props) {
  const totalGenerated = history.length;
  const scriptCount = history.filter(h => h.type === "Script").length;
  const blogCount   = history.filter(h => h.type === "Blog Post").length;
  const copyCount   = history.filter(h => h.type === "Website Copy" || h.type === "Product Desc").length;
  const otherCount  = totalGenerated - scriptCount - blogCount - copyCount;

  const progressPct = Math.min((totalGenerated / 50) * 100, 100);
  const circumference = 2 * Math.PI * 32;
  const offset = circumference - (progressPct / 100) * circumference;

  return (
    <div className="main-content fade-in">
      <div className="dashboard-layout">
        {/* ── LEFT: Main column ── */}
        <div className="dashboard-main">
          <div className="dash-label" style={{ display: "flex", alignItems: "center", gap: 6, fontSize: "14px", textTransform: "none", letterSpacing: "normal", color: "var(--t2)", fontWeight: 500 }}>
            Good afternoon, Creator <span style={{ fontSize: "16px" }}>👋</span>
          </div>

          <div className="dash-hero">
            <div className="dash-hero-text">
              <h1>Let's create something amazing.</h1>
              <p>AI-powered tools for content creators, marketers and agencies.</p>
            </div>
            <div className="hero-visual">
              <div className="hero-script-text">Content<br/>Automates<br/>Growth.</div>
            </div>
          </div>

          {/* Tool form card — show Video Script Generator inline */}
          <div className="tool-card">
            <div className="tool-card-header">
              <div className="tool-card-title-row">
                <div className="tool-card-icon">🎬</div>
                <div>
                  <div className="tool-card-title">Video Script Generator</div>
                  <div className="tool-card-desc">Research a niche, pick a high-potential concept, and get a production-ready script in seconds.</div>
                </div>
              </div>
              <button className="view-examples-btn" onClick={() => onNavigate("Video Script Generator")}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><polygon points="10 8 16 12 10 16 10 8"/></svg>
                View examples
              </button>
            </div>

            {/* Steps breadcrumb */}
            <div className="breadcrumb">
              <div className="bc-step active"><span className="bc-num">1</span><span>Topic</span></div>
              <span className="bc-sep">›</span>
              <div className="bc-step"><span className="bc-num">2</span><span>Pick idea</span></div>
              <span className="bc-sep">›</span>
              <div className="bc-step"><span className="bc-num">3</span><span>Script</span></div>
            </div>

            {/* Quick launch button */}
            <button className="btn btn-primary btn-wide" onClick={() => onNavigate("Video Script Generator")} style={{ marginTop: 4 }}>
              ✦ Generate Ideas →
            </button>
          </div>

          {/* Example Use Cases */}
          <div className="popular-section">
            <div className="popular-header">
              <div>
                <div className="popular-title">Example Use Cases</div>
                <div className="popular-subtitle">Not sure what to try? Here are some popular examples to get you started.</div>
              </div>
              <span className="popular-link" onClick={() => onNavigate("Video Script Generator")}>
                View all examples →
              </span>
            </div>

            <div className="popular-grid">
              {USE_CASES.map((card, idx) => (
                <div
                  key={idx}
                  className="popular-card"
                  onClick={() => onNavigate(card.target)}
                >
                  <div className="popular-card-top" style={{ marginBottom: "auto" }}>
                    <div className="popular-card-icon" style={{ background: "transparent" }}>{card.icon}</div>
                    <div className="popular-card-arrow" style={{ width: 24, height: 24, fontSize: 12 }}>→</div>
                  </div>
                  <div className="popular-card-title">{card.label}</div>
                  <div className="popular-card-desc">{card.desc}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Footer */}
          <div className="app-footer">
            <div className="footer-left">© 2026 Pistelle AI. All rights reserved.</div>
            <div className="footer-center" style={{ display: "flex", gap: "20px", color: "rgba(255,255,255,0.6)", fontSize: "12px", fontWeight: 500 }}>
              <span><span style={{ color: "var(--green)" }}>✓</span> 100% Local Execution</span>
              <span><span style={{ color: "var(--green)" }}>✓</span> Zero Data Collection</span>
            </div>
            <div className="footer-right">
              {/* Removed social icons */}
            </div>
          </div>
        </div>

        {/* ── RIGHT: Aside column ── */}
        <div className="dashboard-aside">
          {/* Tips */}
          <div className="aside-card">
            <div className="aside-card-title" style={{ marginBottom: 16 }}>
              <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <span style={{ fontSize: "16px" }}>💡</span> Tips for better results
              </span>
            </div>
            
            <div className="tips-list" style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
              <div style={{ display: "flex", gap: "10px", alignItems: "flex-start", fontSize: "12.5px", color: "var(--t2)" }}>
                <span style={{ color: "var(--green)" }}>✓</span>
                Be specific with your niche and audience
              </div>
              <div style={{ display: "flex", gap: "10px", alignItems: "flex-start", fontSize: "12.5px", color: "var(--t2)" }}>
                <span style={{ color: "var(--green)" }}>✓</span>
                Try different content types
              </div>
              <div style={{ display: "flex", gap: "10px", alignItems: "flex-start", fontSize: "12.5px", color: "var(--t2)" }}>
                <span style={{ color: "var(--green)" }}>✓</span>
                Add tone and length preferences
              </div>
              <div style={{ display: "flex", gap: "10px", alignItems: "flex-start", fontSize: "12.5px", color: "var(--t2)" }}>
                <span style={{ color: "var(--green)" }}>✓</span>
                Review and refine the generated script
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
