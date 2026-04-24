from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.selector import HashtagSelector, serialize_selection


ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "web"

app = FastAPI(title="instatags")
app.mount("/static", StaticFiles(directory=str(WEB_DIR)), name="static")

selector = HashtagSelector()


@app.get("/")
def index() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")


@app.get("/api/status")
def status() -> JSONResponse:
    state = selector._read_state()
    return JSONResponse(
        {
            "iteration": state["iteration"],
            "active_deck_size": selector.active_deck_size,
            "queue_head": state["queue"][:12],
        }
    )


@app.get("/api/preview")
def preview(
    iterations: int = Query(6, ge=1, le=12),
    categories: Optional[str] = Query(None),
    forced_tag: Optional[str] = Query(None),
) -> JSONResponse:
    category_list = [part.strip() for part in categories.split(",")] if categories else []
    results = selector.preview(iterations=iterations, categories=category_list, forced_tag=forced_tag)
    return JSONResponse({"results": [serialize_selection(result) for result in results]})


@app.post("/api/next")
def next_tags(
    categories: Optional[str] = Query(None),
    forced_tag: Optional[str] = Query(None),
) -> JSONResponse:
    category_list = [part.strip() for part in categories.split(",")] if categories else []
    result = selector.next_selection(categories=category_list, forced_tag=forced_tag)
    payload = serialize_selection(result)
    payload["active_deck_size"] = selector.active_deck_size
    return JSONResponse(payload)


@app.post("/api/reset")
def reset() -> JSONResponse:
    state = selector.reset()
    return JSONResponse(
        {
            "iteration": state["iteration"],
            "active_deck_size": selector.active_deck_size,
            "queue_head": state["queue"][:12],
        }
    )
