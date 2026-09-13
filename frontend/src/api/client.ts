/**
 * api.ts — Service layer for communicating with the FastAPI backend.
 * Uses relative URLs — works in both dev (Vite proxy) and production (FastAPI static serving).
 * All functions throw a plain-English Error string on failure.
 */

const BASE = "";  // relative — Vite proxy forwards /api/* to :8000 in dev; FastAPI serves directly in prod


async function post<T>(path: string, body: object): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const json = await res.json();
  if (!res.ok) {
    throw new Error(json.detail ?? `Request failed (${res.status})`);
  }
  return json as T;
}

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  const json = await res.json();
  if (!res.ok) throw new Error(json.detail ?? `Request failed (${res.status})`);
  return json as T;
}

// ── System ────────────────────────────────────────────────────────────────────

export interface StatusResponse {
  api_key_set: boolean;
  model: string;
}
export const getStatus = () => get<StatusResponse>("/api/status");
export const saveApiKey = (api_key: string) => post("/api/setup", { api_key });

// ── Tools ─────────────────────────────────────────────────────────────────────

interface GenerateResponse { result: string; }

export const runPlanner = (niche: string, platform: string, audience: string) =>
  post<GenerateResponse>("/api/planner", { niche, platform, audience });

export const runScriptwriter = (idea: string, platform: string, video_length: string) =>
  post<GenerateResponse>("/api/scriptwriter", { idea, platform, video_length });

export const runBlogWriter = (
  topic: string, audience: string, tone: string, length: string, keywords: string
) => post<GenerateResponse>("/api/blog_writer", { topic, audience, tone, length, keywords });

export const runWebsiteCopy = (product: string, audience: string, tone: string, usp: string) =>
  post<GenerateResponse>("/api/website_copy", { product, audience, tone, usp });

export const runProductDesc = (
  name: string, category: string, features: string, audience: string, platform: string
) => post<GenerateResponse>("/api/product_desc", { name, category, features, audience, platform });

export const runHookGenerator = (topic: string, audience: string, medium: string) =>
  post<GenerateResponse>("/api/hook_generator", { topic, audience, medium });

export const runToneRewriter = (text: string, tone: string, context: string) =>
  post<GenerateResponse>("/api/tone_rewriter", { text, tone, context });
