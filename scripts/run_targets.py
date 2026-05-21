#!/usr/bin/env python3
"""
scripts/run_targets.py
Cross-platform Python helper to run blackRIFT against multiple targets listed in a file.

Usage examples:
  # sequential (single-thread)
  python scripts/run_targets.py scans/targets.txt

  # parallel (4 workers)
  python scripts/run_targets.py scans/targets.txt --jobs 4

  # pass extra args through to blackRIFT
  python scripts/run_targets.py scans/targets.txt --extra-args "--artifact-dir artifacts"

The targets file format is: one target per line, optionally host:port. Lines starting
with '#' are ignored. The helper discovers the repo's `blackRIFT.py` automatically
when run from the repository tree.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List


def safe_name(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", s)


def build_cmd(blackrift: Path, target: str, args) -> List[str]:
    cmd = [sys.executable, str(blackrift), "--target", target]
    if args.no_subfinder:
        cmd.append("--no-subfinder")
    elif args.subfinder:
        cmd.append("--subfinder")
    if args.subfinder_output:
        host_only = target.split(":", 1)[0]
        out = args.subfinder_output.replace("{host}", host_only).replace("{safe_host}", safe_name(host_only))
        cmd += ["--subfinder-output", out]
    if args.scheme:
        cmd += ["--scheme", args.scheme]
    if args.port is not None:
        cmd += ["--port", str(args.port)]
    if args.extra_args:
        # naive split of extra args (user should quote correctly)
        cmd += args.extra_args.split()
    return cmd


def run_one(blackrift: Path, target: str, args) -> int:
    cmd = build_cmd(blackrift, target, args)
    workdir = str(blackrift.parent)
    print(f"\n[run] {target} -> {' '.join(cmd)}", flush=True)
    try:
        completed = subprocess.run(cmd, cwd=workdir)
        return completed.returncode
    except Exception as exc:
        print(f"[error] {target} exception: {exc}", file=sys.stderr, flush=True)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run blackRIFT against targets listed in a file (cross-platform Python helper).")
    parser.add_argument("targets_file", help="newline-separated targets file (host[:port] per line)")
    parser.add_argument("--blackrift", help="path to blackRIFT.py (defaults to repo root blackRIFT.py)")
    parser.add_argument("--jobs", "-j", type=int, default=1, help="parallel jobs; 1 = sequential")
    parser.add_argument("--no-subfinder", action="store_true")
    parser.add_argument("--subfinder", action="store_true")
    parser.add_argument("--subfinder-output", help="path pattern for subfinder output. supports {host} and {safe_host} placeholders.")
    parser.add_argument("--scheme", choices=("http", "https"), help="fallback scheme for targets")
    parser.add_argument("--port", type=int, help="fallback port when target omits one")
    parser.add_argument("--extra-args", help="extra arguments to pass to blackRIFT (quoted string)")
    args = parser.parse_args()

    targets_path = Path(args.targets_file)
    if not targets_path.exists():
        print(f"targets file not found: {targets_path}", file=sys.stderr)
        return 2

    targets = []
    with targets_path.open("r", encoding="utf-8") as fh:
        for ln in fh:
            s = ln.strip()
            if not s or s.startswith("#"):
                continue
            targets.append(s)
    if not targets:
        print("no targets to process", file=sys.stderr)
        return 1

    if args.blackrift:
        blackrift_script = Path(args.blackrift)
    else:
        # assume repository layout; scripts/ is one level below project root
        blackrift_script = Path(__file__).resolve().parents[1] / "blackRIFT.py"
    if not blackrift_script.exists():
        print(f"blackRIFT.py not found at {blackrift_script}", file=sys.stderr)
        return 2

    exit_code = 0
    if args.jobs <= 1:
        for t in targets:
            rc = run_one(blackrift_script, t, args)
            if rc != 0:
                exit_code = rc or exit_code or 1
    else:
        with ThreadPoolExecutor(max_workers=args.jobs) as ex:
            future_map = {ex.submit(run_one, blackrift_script, t, args): t for t in targets}
            for fut in as_completed(future_map):
                t = future_map[fut]
                try:
                    rc = fut.result()
                    if rc != 0:
                        exit_code = rc or exit_code or 1
                except Exception as exc:
                    print(f"[error] {t} raised {exc}", file=sys.stderr)
                    exit_code = 1

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
