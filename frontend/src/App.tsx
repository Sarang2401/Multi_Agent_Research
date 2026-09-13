import { useState, useEffect, useCallback } from "react";
import "./index.css";
import { getStatus } from "./api/client";
import { useHistory } from "./api/useHistory";
import type { View } from "./components/Sidebar";
import Sidebar from "./components/Sidebar";
import TopBar from "./components/TopBar";
import SetupScreen from "./components/SetupScreen";
import Dashboard from "./components/Dashboard";
import VideoScriptGenerator from "./components/tools/VideoScriptGenerator";
import BlogWriter from "./components/tools/BlogWriter";
import WebsiteCopywriter from "./components/tools/WebsiteCopywriter";
import ProductDescription from "./components/tools/ProductDescription";
import ViralHookGenerator from "./components/tools/ViralHookGenerator";
import ToneRewriter from "./components/tools/ToneRewriter";
import SessionHistory from "./components/tools/SessionHistory";
import Settings from "./components/tools/Settings";

export default function App() {
  const [view, setView]           = useState<View>("Dashboard");
  const [apiKeySet, setApiKeySet] = useState(false);
  const [model, setModel]         = useState("gemini-3.6-flash");
  const [checking, setChecking]   = useState(true);
  const { history, addEntry }     = useHistory();

  const checkStatus = useCallback(async () => {
    try {
      const s = await getStatus();
      setApiKeySet(s.api_key_set);
      setModel(s.model);
    } catch {
      // backend not yet up
    } finally {
      setChecking(false);
    }
  }, []);

  useEffect(() => { checkStatus(); }, [checkStatus]);

  const onSave = useCallback((type: string) => (title: string, content: string) => {
    addEntry(type, title, content);
  }, [addEntry]);

  if (checking) {
    return (
      <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "100vh", flexDirection: "column", gap: 16, background: "#f5f5f5" }}>
        <div className="spinner" />
        <span style={{ color: "#a3a3a3", fontSize: 14, fontWeight: 500 }}>Connecting to Pistelle AI…</span>
      </div>
    );
  }

  if (!apiKeySet) {
    return <SetupScreen onConnected={() => { setApiKeySet(true); checkStatus(); }} />;
  }

  const renderView = () => {
    switch (view) {
      case "Dashboard":              return <Dashboard onNavigate={setView} currentTool={view} history={history} />;
      case "Video Script Generator": return <VideoScriptGenerator onSave={onSave("Script")} />;
      case "SEO Blog Writer":        return <BlogWriter onSave={onSave("Blog Post")} />;
      case "Website Copywriter":     return <WebsiteCopywriter onSave={onSave("Website Copy")} />;
      case "Product Description":    return <ProductDescription onSave={onSave("Product Desc")} />;
      case "Viral Hook Generator":   return <ViralHookGenerator onSave={onSave("Hooks")} />;
      case "Tone Rewriter":          return <ToneRewriter onSave={onSave("Rewrite")} />;
      case "Session History":        return <SessionHistory history={history} />;
      case "Settings":               return <Settings model={model} onApiKeyChange={checkStatus} />;
      default:                       return null;
    }
  };

  return (
    <div className="app-shell">
      <Sidebar current={view} onNavigate={setView} />
      <div className="main-wrap">
        <TopBar />
        {renderView()}
      </div>
    </div>
  );
}
