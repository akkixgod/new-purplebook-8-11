#!/usr/bin/env python3
"""Merge _rw1/_rw2/_math1/_math2 into questions.json for a PurpleBook test slug."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_mod(path: Path, expected: int) -> dict:
    if not path.exists():
        raise FileNotFoundError(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    # unwrap accidental nesting
    if isinstance(data, dict) and not all(str(k).isdigit() for k in data.keys()):
        for v in data.values():
            if isinstance(v, dict) and all(str(k).isdigit() for k in v.keys()):
                data = v
                break
    keys = [str(i) for i in range(1, expected + 1)]
    missing = [k for k in keys if k not in data]
    if missing:
        raise SystemExit(f"{path}: missing questions {missing[:10]}{'...' if len(missing)>10 else ''}")
    for k in keys:
        q = data[k]
        if not q.get("text"):
            raise SystemExit(f"{path}: Q{k} missing text")
        if "choices" not in q:
            raise SystemExit(f"{path}: Q{k} missing choices")
    return {k: data[k] for k in keys}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", help="e.g. purplebook-test-4")
    args = ap.parse_args()
    d = Path("prisma/data") / args.slug
    out = {
        "ENGLISH": {
            "1": load_mod(d / "_rw1.json", 27),
            "2": load_mod(d / "_rw2.json", 27),
        },
        "MATH": {
            "1": load_mod(d / "_math1.json", 22),
            "2": load_mod(d / "_math2.json", 22),
        },
    }
    needs = []
    for sec, mods in out.items():
        for mod, qs in mods.items():
            for num, q in qs.items():
                url = q.get("imageUrl")
                if isinstance(url, str) and url.startswith("NEEDS_SVG"):
                    needs.append(f"{sec} M{mod} Q{num}: {url}")
    dest = d / "questions.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {dest}")
    print(f"NEEDS_SVG count: {len(needs)}")
    for line in needs:
        print(" ", line)


if __name__ == "__main__":
    main()
