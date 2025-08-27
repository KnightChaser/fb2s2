# fetch.py
from __future__ import annotations
import requests
from settings import TOR_SOCKS_PROXY, USER_AGENT, REQUEST_TIMEOUT_SEC


class TorFetchError(RuntimeError):
    pass


def fetch_html_via_tor(url: str, timeout_sec: int = REQUEST_TIMEOUT_SEC) -> str:
    """
    Fetch raw HTML/text from an onion (or clearnet) URL via Tor's SOCKS5 proxy.

    - Uses socks5h so DNS resolution happens *inside* Tor (no leaks).
    - Raises TorFetchError on non-200 or network errors.
    """
    if not url.startswith(("http://", "https://")):
        raise ValueError("URL must start with http:// or https://")

    session = requests.Session()
    session.proxies = {
        "http": TOR_SOCKS_PROXY,
        "https": TOR_SOCKS_PROXY,
    }
    session.headers.update({"User-Agent": USER_AGENT})

    try:
        resp = session.get(url, timeout=timeout_sec)
        resp.raise_for_status()
        # Trust site-provided encoding; fall back if missing
        if not resp.encoding:
            resp.encoding = resp.apparent_encoding or "utf-8"
        return resp.text
    except requests.RequestException as e:
        raise TorFetchError(f"Failed to fetch {url}: {e}") from e
