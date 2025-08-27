# main.py
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from fetch import fetch_html_via_tor, TorFetchError


def main() -> int:
    ap = argparse.ArgumentParser(description="Minimal Tor HTML fetcher for .onion URLs")
    ap.add_argument("url", help="Target URL (e.g., http://examplev3address.onion/)")
    ap.add_argument(
        "--out",
        type=Path,
        help="Write raw HTML to this file (default: print to stdout)",
    )
    args = ap.parse_args()

    try:
        html = fetch_html_via_tor(args.url)
    except TorFetchError as e:
        print(f"[error] {e}", file=sys.stderr)
        return 1

    if args.out:
        args.out.write_text(html, encoding="utf-8")
        print(f"[ok] wrote {args.out}")
    else:
        # Print to stdout (raw)
        print(html)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
