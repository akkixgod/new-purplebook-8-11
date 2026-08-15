from pathlib import Path
import re
import json

d = Path("public/mocks/2025-august-us-v3/pages")
rows = []
for i in range(1, 104):
    t = (d / f"page-{i:02d}.txt").read_text(encoding="utf-8", errors="replace")
    low = t.lower()
    first_lines = [ln.strip() for ln in t.splitlines() if ln.strip()][:6]
    mod = None
    if "section 1, module 1" in low:
        mod = "RW1"
    elif "section 1, module 2" in low:
        mod = "RW2"
    elif "section 2, module 1" in low:
        mod = "M1"
    elif "section 2, module 2" in low:
        mod = "M2"
    # bank id: lone number line often
    bank = None
    for ln in t.splitlines():
        s = ln.strip()
        if re.fullmatch(r"\d{1,4}", s):
            bank = int(s)
            break
    rows.append(
        {
            "page": i,
            "mod_hint": mod,
            "bank": bank,
            "head": " | ".join(first_lines)[:200],
            "chars": len(t),
        }
    )

out = Path("prisma/data/2025-august-us-v3")
out.mkdir(parents=True, exist_ok=True)
(out / "_page_map.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

# summary transitions
prev = None
for r in rows:
    h = r["head"].encode("ascii", "replace").decode()
    mark = ""
    if r["mod_hint"] and r["mod_hint"] != prev:
        mark = f" *** {r['mod_hint']} ***"
        prev = r["mod_hint"]
    print(f"{r['page']:03d} bank={r['bank']} {r['mod_hint'] or '----'}{mark} {h[:100]}")
