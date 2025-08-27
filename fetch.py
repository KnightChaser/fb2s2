# fetch.py
from __future__ import annotations
import requests
from settings import (
    TOR_SOCKS_PROXY,
    USER_AGENT,
    REQUEST_TIMEOUT_SEC,
    CACHE_TTL_SEC,
)
import cache


class TorFetchError(RuntimeError):
    pass


def fetch_html_via_tor(
    url: str,
    timeout_sec: int = REQUEST_TIMEOUT_SEC,
    use_cache: bool = True,
    cache_ttl_sec: int = CACHE_TTL_SEC,
) -> str:
    """
    Fetch raw HTML/text from URL via Tor's SOCKS5 proxy.

    If use_cache is True, return a fresh cached copy when available
    (fresh = cached within cache_ttl_sec). Otherwise, fetch and update cache.
    """
    if not url.startswith(("http://", "https://")):
        raise ValueError("URL must start with http:// or https://")

    # If caching is enabled, try to load from cache first
    if use_cache:
        cached = cache.load(url, cache_ttl_sec)
        if cached is not None:
            return cached

    # Manually create a session to set proxies and headers
    session = requests.Session()
    session.proxies = {"http": TOR_SOCKS_PROXY, "https": TOR_SOCKS_PROXY}
    session.headers.update({"User-Agent": USER_AGENT})

    try:
        resp = session.get(url, timeout=timeout_sec)
        resp.raise_for_status()
        if not resp.encoding:
            resp.encoding = resp.apparent_encoding or "utf-8"
        html = resp.text

        # If caching is enabled, save to cache
        if use_cache:
            cache.save(url, html)

        return html
    except requests.RequestException as exc:
        raise TorFetchError(f"Failed to fetch {url}: {exc}") from exc
