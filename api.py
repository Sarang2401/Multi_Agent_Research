"""
api.py — FastAPI backend for Pistelle AI
Exposes all AI generation functions from crew.py as REST endpoints.
In production: also serves the pre-built React frontend as static files.
Run with: uvicorn api:app --host 127.0.0.1 --port 8000
"""
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

# Path to the pre-built React app
FRONTEND_DIST = Path(__file__).parent / "frontend" / "dist"

app = FastAPI(title="Pistelle AI API", version="2.0.0")

# Allow the Vite dev server to call us during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request / Response models ─────────────────────────────────────────────────

class SetupRequest(BaseModel):
    api_key: str = Field(..., min_length=10)

class StatusResponse(BaseModel):
    api_key_set: bool
    model: str

class GenerateResponse(BaseModel):
    result: str

class PlannerRequest(BaseModel):
    niche: str
    platform: str
    audience: str

class ScriptwriterRequest(BaseModel):
    idea: str
    platform: str
    video_length: str

class BlogWriterRequest(BaseModel):
    topic: str
    audience: str
    tone: str
    length: str
    keywords: str = ""

class WebsiteCopyRequest(BaseModel):
    product: str
    audience: str
    tone: str
    usp: str

class ProductDescRequest(BaseModel):
    name: str
    category: str
    features: str
    audience: str
    platform: str

class HookGeneratorRequest(BaseModel):
    topic: str
    audience: str
    medium: str

class ToneRewriterRequest(BaseModel):
    text: str
    tone: str
    context: str = ""


# ── Helper ────────────────────────────────────────────────────────────────────

def _handle_crew_errors(exc: Exception) -> HTTPException:
    """Convert crew.py custom exceptions into HTTP responses."""
    from crew import RateLimitError, NoKeyError, ConnectionError as CrewConnectionError
    if isinstance(exc, RateLimitError):
        return HTTPException(status_code=429, detail=str(exc))
    if isinstance(exc, NoKeyError):
        return HTTPException(status_code=401, detail=str(exc))
    if isinstance(exc, CrewConnectionError):
        return HTTPException(status_code=503, detail=str(exc))
    if isinstance(exc, ValueError):
        return HTTPException(status_code=422, detail=str(exc))
    return HTTPException(status_code=500, detail=f"Unexpected error: {exc}")


# ── System endpoints ──────────────────────────────────────────────────────────

@app.get("/api/status", response_model=StatusResponse)
def get_status():
    """Check whether an API key is configured."""
    from config import is_api_key_set, GEMINI_MODEL
    return {"api_key_set": is_api_key_set(), "model": GEMINI_MODEL}


@app.post("/api/setup")
def save_setup(req: SetupRequest):
    """Persist a new API key to the local .env file."""
    key = req.api_key.strip()
    if not key.startswith("AIza"):
        raise HTTPException(status_code=422, detail="A Gemini API key must start with 'AIza'.")
    from config import save_api_key
    save_api_key(key)
    return {"message": "API key saved successfully."}


# ── Generation endpoints ──────────────────────────────────────────────────────

@app.post("/api/planner", response_model=GenerateResponse)
def planner(req: PlannerRequest):
    try:
        from crew import run_planner
        result = run_planner(req.niche, req.platform, req.audience)
        return {"result": result}
    except Exception as exc:
        raise _handle_crew_errors(exc)


@app.post("/api/scriptwriter", response_model=GenerateResponse)
def scriptwriter(req: ScriptwriterRequest):
    try:
        from crew import run_scriptwriter
        result = run_scriptwriter(req.idea, req.platform, req.video_length)
        return {"result": result}
    except Exception as exc:
        raise _handle_crew_errors(exc)


@app.post("/api/blog_writer", response_model=GenerateResponse)
def blog_writer(req: BlogWriterRequest):
    try:
        from crew import run_blog_writer
        result = run_blog_writer(req.topic, req.audience, req.tone, req.length, req.keywords)
        return {"result": result}
    except Exception as exc:
        raise _handle_crew_errors(exc)


@app.post("/api/website_copy", response_model=GenerateResponse)
def website_copy(req: WebsiteCopyRequest):
    try:
        from crew import run_website_copy
        result = run_website_copy(req.product, req.audience, req.tone, req.usp)
        return {"result": result}
    except Exception as exc:
        raise _handle_crew_errors(exc)


@app.post("/api/product_desc", response_model=GenerateResponse)
def product_desc(req: ProductDescRequest):
    try:
        from crew import run_product_desc
        result = run_product_desc(req.name, req.category, req.features, req.audience, req.platform)
        return {"result": result}
    except Exception as exc:
        raise _handle_crew_errors(exc)


@app.post("/api/hook_generator", response_model=GenerateResponse)
def hook_generator(req: HookGeneratorRequest):
    try:
        from crew import run_hook_generator
        result = run_hook_generator(req.topic, req.audience, req.medium)
        return {"result": result}
    except Exception as exc:
        raise _handle_crew_errors(exc)


@app.post("/api/tone_rewriter", response_model=GenerateResponse)
def tone_rewriter(req: ToneRewriterRequest):
    try:
        from crew import run_tone_rewriter
        result = run_tone_rewriter(req.text, req.tone, req.context)
        return {"result": result}
    except Exception as exc:
        raise _handle_crew_errors(exc)


# ── Serve the pre-built React frontend ───────────────────────────────────────
# This block only activates when `frontend/dist` exists (after npm run build).
# All /api/* routes above are matched first; everything else serves the React app.

if FRONTEND_DIST.exists():
    # Serve static assets (JS, CSS, images) from /assets
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def serve_react(full_path: str):
        """Catch-all: return index.html so React Router handles the route."""
        index = FRONTEND_DIST / "index.html"
        return FileResponse(str(index))

