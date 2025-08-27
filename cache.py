# cache.py
from __future__ import annotations
import json
import re
import time
from hashlib import sha256
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse
from settings import CACHE_ROOT, CACHE_TTL_SEC


def _safe_host_dir_name(hostname: str) -> str:
    """
    Convert a hostname to a safe directory name.
    - Strips the '.onion' suffix if present (abc.onion -> abc).
    - Keeps other TLDs (example.com -> example.com).
    - Allows [A-Za-z0-9._-]; replaces others with '_'.
    """
    if hostname.endswith(".onion"):
        base = hostname[:-6]  # remove trailing '.onion'
    else:
        base = hostname
    safe = re.sub(r"[^A-Za-z0-9._-]", "_", base)
    return safe or "unknown"


def _cache_dir_for(url: str) -> Path:
    """
    Return the cache directory Path for a given URL.
    """
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.hostname:
        raise ValueError(f"Invalid URL: {url}")
    host_dir = _safe_host_dir_name(parsed.hostname)
    return CACHE_ROOT / host_dir


def _ensure_dir(path: Path) -> None:
    """
    Ensure that the given directory path exists.
    """
    path.mkdir(parents=True, exist_ok=True)


def _key(url: str) -> str:
    """
    Generate a SHA-256 hash key for the given URL.
    """
    return sha256(url.encode("utf-8")).hexdigest()


def _paths_for(url: str) -> Tuple[Path, Path]:
    """
    Return (html_path, metadata_path) for a given URL.
    """
    cache_dir = _cache_dir_for(url)
    _ensure_dir(cache_dir)
    key_hash = _key(url)
    html_path = cache_dir / f"{key_hash}.html"
    meta_path = cache_dir / f"{key_hash}.meta.json"
    return html_path, meta_path


def load(url: str, max_age_sec: int = CACHE_TTL_SEC) -> Optional[str]:
    """
    Return cached HTML if present and fresh; else None
    """
    html_path, meta_path = _paths_for(url)
    if not (html_path.exists() and meta_path.exists()):
        return None

    # Check out the metadata if data presents
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except Exception:
        return None

    # Check age
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
