# settings.py
from __future__ import annotations
from pathlib import Path

TOR_SOCKS_PROXY: str = "socks5h://127.0.0.1:9050"

USER_AGENT: str = (
    "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0"
)

REQUEST_TIMEOUT_SEC: int = 60

CACHE_DIR: Path = Path(".cache/freebbs")
CACHE_TTL_SEC: int = 600  # 10 minutes
