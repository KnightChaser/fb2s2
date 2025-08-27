# main.py
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from fetch import fetch_html_via_tor, TorFetchError
from settings import CACHE_TTL_SEC


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Minimal Tor HTML fetcher for .onion URLs with a tiny cache"
    )
    ap.add_argument("url", help="Target URL (e.g., http://examplev3address.onion/)")
    ap.add_argument("--out", type=Path, help="Write raw HTML to this file")
    ap.add_argument("--no-cache", action="store_true", help="Bypass cache entirely")
    ap.add_argument(
        "--ttl",
        type=int,
        default=CACHE_TTL_SEC,
        help=f"Cache TTL seconds (default: {CACHE_TTL_SEC})",
    )
    args = ap.parse_args()

    try:
        html = fetch_html_via_tor(
            args.url, use_cache=not args.no_cache, cache_ttl_sec=args.ttl
        )
    except TorFetchError as e:
        print(f"[error] {e}", file=sys.stderr)
        return 1

    if args.out:
        args.out.write_text(html, encoding="utf-8")
        print(f"[ok] wrote {args.out}")
    else:
        print(html)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
