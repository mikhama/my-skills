#!/usr/bin/env python3
"""Gather PKUP submission artifacts from a git repository."""

from __future__ import annotations

import argparse
import calendar
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse, urlunparse


def run_git(repo: Path, args: list[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout.strip()


def default_window(anchor: dt.date) -> tuple[dt.datetime, dt.datetime]:
    prev_year = anchor.year
    prev_month = anchor.month - 1
    if prev_month == 0:
        prev_year -= 1
        prev_month = 12

    start = dt.datetime(prev_year, prev_month, 19, 0, 0, 0)
    last_day = calendar.monthrange(anchor.year, anchor.month)[1]
    end_day = min(18, last_day)
    end = dt.datetime(anchor.year, anchor.month, end_day, 23, 59, 59)
    return start, end


def canonical_host(host: str | None) -> str:
    if not host:
        return ""
    for canonical in ("github.com", "gitlab.com"):
        if host == canonical or host.startswith(f"{canonical}-"):
            return canonical
    return host


def normalize_origin(origin: str) -> str:
    origin = origin.strip()
    if origin.startswith("git@"):
        match = re.match(r"git@([^:]+):(.+?)(?:\.git)?$", origin)
        if not match:
            raise SystemExit(f"Unsupported origin URL: {origin}")
        host, path = match.groups()
        host = canonical_host(host)
        return f"https://{host}/{path}"

    if origin.startswith("ssh://git@"):
        parsed = urlparse(origin)
        path = parsed.path.strip("/")
        if path.endswith(".git"):
            path = path[:-4]
        host = canonical_host(parsed.hostname)
        return f"https://{host}/{path}"

    if origin.startswith("http://") or origin.startswith("https://"):
        if origin.endswith(".git"):
            origin = origin[:-4]
        parsed = urlparse(origin)
        host = canonical_host(parsed.hostname)
        if not host:
            raise SystemExit(f"Unsupported origin URL: {origin}")
        return urlunparse(
            (
                parsed.scheme,
                host,
                parsed.path,
                parsed.params,
                parsed.query,
                parsed.fragment,
            )
        )

    raise SystemExit(f"Unsupported origin URL: {origin}")


def commit_url(origin: str, sha: str) -> str:
    base = normalize_origin(origin).rstrip("/")
    host = urlparse(base).hostname or ""
    if "github.com" in host:
        return f"{base}/commit/{sha}"
    return f"{base}/-/commit/{sha}"


def md_escape(value: str) -> str:
    return value.replace("|", r"\|").replace("\n", "<br>").strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Path to the git repository")
    parser.add_argument(
        "--anchor-date",
        help="Anchor date for default PKUP window in YYYY-MM-DD format",
    )
    parser.add_argument("--since", help="Explicit start date in YYYY-MM-DD format")
    parser.add_argument("--until", help="Explicit end date in YYYY-MM-DD format")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = Path(args.repo).resolve()
    anchor = (
        dt.datetime.strptime(args.anchor_date, "%Y-%m-%d").date()
        if args.anchor_date
        else dt.date.today()
    )

    if args.since or args.until:
        if not args.since or not args.until:
            raise SystemExit("Pass both --since and --until, or neither.")
        start = dt.datetime.strptime(args.since, "%Y-%m-%d")
        end = dt.datetime.strptime(args.until, "%Y-%m-%d").replace(
            hour=23, minute=59, second=59
        )
    else:
        start, end = default_window(anchor)

    user_email = run_git(repo, ["config", "--get", "user.email"])
    origin = run_git(repo, ["remote", "get-url", "origin"])
    raw = run_git(
        repo,
        [
            "log",
            "--reverse",
            f"--author={user_email}",
            f"--since={start.isoformat(sep=' ')}",
            f"--until={end.isoformat(sep=' ')}",
            "--date=format:%Y-%m-%d %H:%M",
            "--pretty=format:%H%x1f%ad%x1f%D%x1f%s%x1f%b%x1e",
        ],
    )

    print("| Date | Location | Commit subject | Commit body |")
    print("| --- | --- | --- | --- |")
    if not raw:
        return 0

    for record in raw.rstrip("\x1e").split("\x1e"):
        record = record.strip("\n")
        if not record:
            continue
        sha, commit_date, _refs, subject, body = (record.split("\x1f", 4) + [""])[:5]
        location = commit_url(origin, sha)
        print(
            "| "
            + " | ".join(
                [
                    md_escape(commit_date),
                    md_escape(location),
                    md_escape(subject),
                    md_escape(body),
                ]
            )
            + " |"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
