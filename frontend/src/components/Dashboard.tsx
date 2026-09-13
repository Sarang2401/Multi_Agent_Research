import React from "react";
import type { View } from "./Sidebar";
import type { HistoryEntry } from "../api/useHistory";

interface Props {
  onNavigate: (v: View) => void;
  currentTool: View;
  history: HistoryEntry[];
}

const TOOL_CARDS: { label: View; icon: string; desc: string }[] = [
  { label: "Video Script Generator", icon: "🎬", desc: "Turn ideas into engaging scripts." },
  { label: "SEO Blog Writer",        icon: "📝", desc: "Rank higher with AI-powered blogs." },
  { label: "Website Copywriter",     icon: "🌐", desc: "Convert visitors into customers." },
  { label: "Viral Hook Generator",   icon: "⚡", desc: "Stop the scroll. Get attention." },
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
          <div className="dash-label">Turn ideas into impact</div>

          <div className="dash-hero">
            <div className="dash-hero-text">
              <h1>Create better content.<br/>Faster, with AI.</h1>
              <p>Powerful tools for content creators, marketers and agencies.</p>
            </div>
            <div className="hero-visual">
              <div className="hero-script-text">Good<br/>Content<br/>Builds<br/>Brands.</div>
              <div className="hero-card">
                <h3>Ideas<br/>Drafts<br/>Growth<br/>All in one place.</h3>
                <div className="hero-card-arrow">→</div>
              </div>
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

          {/* Popular Tools */}
          <div className="popular-section">
            <div className="popular-header">
              <div>
                <div className="popular-title">Popular Tools</div>
                <div className="popular-subtitle">Everything you need to create, at your fingertips.</div>
              </div>
              <span className="popular-link" onClick={() => onNavigate("Video Script Generator")}>
                View all tools →
              </span>
            </div>

            <div className="popular-grid">
              {TOOL_CARDS.map((card) => (
                <div
                  key={card.label}
                  className={`popular-card${currentTool === card.label ? " active" : ""}`}
                  onClick={() => onNavigate(card.label)}
                >
                  <div className="popular-card-top">
                    <div className="popular-card-icon">{card.icon}</div>
                    <div className="popular-card-arrow">→</div>
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
            <div className="footer-center">
              <a href="#">Terms</a>
              <a href="#">Privacy</a>
              <a href="#">Support</a>
            </div>
            <div className="footer-right">
              <span className="footer-social">𝕏</span>
              <span className="footer-social">in</span>
              <span className="footer-social">◉</span>
              <span className="footer-social">▶</span>
            </div>
          </div>
        </div>

        {/* ── RIGHT: Aside column ── */}
        <div className="dashboard-aside">
          {/* Progress card */}
          <div className="aside-card">
            <div className="aside-card-title">
              Your Progress
              <span className="aside-card-link">View Plan</span>
            </div>
            <div className="progress-section">
              <div className="progress-ring-wrap">
                <svg viewBox="0 0 76 76">
                  <circle className="progress-ring-bg" cx="38" cy="38" r="32" />
                  <circle
                    className="progress-ring-fill"
                    cx="38" cy="38" r="32"
                    strokeDasharray={circumference}
                    strokeDashoffset={offset}
                  />
                </svg>
                <div className="progress-ring-text">
                  <span className="progress-ring-num">{totalGenerated}</span>
                  <span className="progress-ring-sub">/ 50</span>
                </div>
              </div>
              <div className="stat-list">
                <div className="stat-row">
                  <span className="stat-row-label"><span className="stat-dot" style={{ background: "#0a0a0a" }} /> Scripts generated</span>
                  <span className="stat-row-val">{scriptCount}</span>
                </div>
                <div className="stat-row">
                  <span className="stat-row-label"><span className="stat-dot" style={{ background: "#6b7280" }} /> Blogs written</span>
                  <span className="stat-row-val">{blogCount}</span>
                </div>
                <div className="stat-row">
                  <span className="stat-row-label"><span className="stat-dot" style={{ background: "#a3a3a3" }} /> Copy pieces</span>
                  <span className="stat-row-val">{copyCount}</span>
                </div>
                <div className="stat-row">
                  <span className="stat-row-label"><span className="stat-dot" style={{ background: "#d4d4d4" }} /> Others</span>
                  <span className="stat-row-val">{otherCount}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Pro Tip */}
          <div className="aside-card">
            <div className="aside-card-title" style={{ marginBottom: 12 }}>
              <span>💡 Pro Tip</span>
            </div>
            <div className="pro-tip">
              <div className="pro-tip-text">
                The more specific you are with your niche and audience, the better the results. Try adding tone and format preferences.
              </div>
            </div>
          </div>

          {/* Quote */}
          <div className="quote-card">
            <div className="quote-mark">"</div>
            <div className="quote-text">Good content isn't luck.<br/>It's a system.</div>
            <div className="quote-author">— Pistelle AI</div>
          </div>
        </div>
      </div>
    </div>
  );
}
