# cache.py
from __future__ import annotations
import json
import time
from hashlib import sha256
from pathlib import Path
from typing import Optional, Tuple
from settings import CACHE_DIR, CACHE_TTL_SEC


def _ensure_cache_dir() -> None:
    """
    Ensure the cache directory exists.
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _key(url: str) -> str:
    """
    Generate a SHA-256 hash key for the given URL.
    """
    return sha256(url.encode("utf-8")).hexdigest()


def _paths_for(url: str) -> Tuple[Path, Path]:
    """
    Return (html_path, metadata_path) for a given URL.
    """
    h = _key(url)
    html = CACHE_DIR / f"{h}.html"
    meta = CACHE_DIR / f"{h}.meta.json"
    return html, meta


def load(url: str, max_age_sec: int = CACHE_TTL_SEC) -> Optional[str]:
    """
    Return cached HTML if present and fresh; else None
    """
    _ensure_cache_dir()
    html_path, meta_path = _paths_for(url)
    if not (html_path.exists() and meta_path.exists()):
        return None

    # Check out the metadata if data presents
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except Exception:
        return None

    cached_at = float(meta.get("cached_at", 0.0))
    if (time.time() - cached_at) > max_age_sec:
        return None

    try:
        return html_path.read_text(encoding="utf-8")
    except Exception:
        return None


def save(url: str, html: str) -> None:
    """
    Save HTML to cache with metadata.
    """
    _ensure_cache_dir()
    html_path, meta_path = _paths_for(url)

    # Write HTML
    tmp_html = html_path.with_suffix(".html.tmp")
    tmp_html.write_text(html, encoding="utf-8")
    tmp_html.replace(html_path)

    # Write metadata
    meta = {
        "url": url,
        "cached_at": time.time(),
        "length": len(html),
    }
    tmp_meta = meta_path.with_suffix(".meta.json.tmp")
    tmp_meta.write_text(json.dumps(meta), encoding="utf-8")
    tmp_meta.replace(meta_path)
