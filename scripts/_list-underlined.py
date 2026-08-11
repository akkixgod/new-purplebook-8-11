import json
import re
from pathlib import Path

for p in sorted(Path("prisma/data").glob("*/questions.json")):
    q = json.loads(p.read_text(encoding="utf-8"))
    for sec, mods in q.items():
        if sec != "ENGLISH":
            continue
        for mod, qs in mods.items():
            for num, item in qs.items():
                text = item.get("text") or ""
                stim = item.get("stimulus") or ""
                if re.search(r"underlin", text, re.I):
                    marked = bool(re.search(r"_[^_\n]{1,400}_", stim))
                    print(f"{p.parent.name} M{mod}Q{num} marked={marked} :: {text[:100]}")
