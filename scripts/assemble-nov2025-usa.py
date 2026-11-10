import json
from pathlib import Path

d = Path("prisma/data/2025-nov-us-a")


def load_answers(name: str) -> list[str]:
    a = json.loads((d / name).read_text(encoding="utf-8"))
    if isinstance(a, dict) and "answers" in a:
        ans = a["answers"]
        if isinstance(ans, dict):
            return [ans[str(i)] for i in range(1, len(ans) + 1)]
        return list(ans)
    if isinstance(a, dict):
        return [a[str(i)] for i in range(1, len(a) + 1)]
    return list(a)


def load_qs(name: str) -> dict:
    q = json.loads((d / name).read_text(encoding="utf-8"))
    out = {}
    for k, v in q.items():
        stim = v.get("stimulus")
        out[k] = {
            "stimulus": stim if stim not in ("", None) else None,
            "text": v["text"],
            "choices": v["choices"],
            "imageUrl": v.get("imageUrl") or None,
        }
    return out


rw1 = load_qs("_rw1.json")
if rw1["5"]["choices"].get("D") == "Categorize":
    rw1["5"]["choices"]["D"] = "categorize"

rw2 = load_qs("_rw2.json")
m1 = load_qs("_math1.json")
m2 = load_qs("_math2.json")

for qs in (m1, m2):
    for v in qs.values():
        if v["stimulus"] in ("", None):
            v["stimulus"] = None

questions = {
    "ENGLISH": {"1": rw1, "2": rw2},
    "MATH": {"1": m1, "2": m2},
}

meta = {
    "slug": "2025-nov-us-a",
    "title": "2025 November Digital",
    "year": 2025,
    "month": 11,
    "version": "US Form A",
    "modules": {
        "ENGLISH": {
            "1": {"timeLimit": 1920, "answers": load_answers("_answers_rw1.json")},
            "2": {"timeLimit": 1920, "answers": load_answers("_answers_rw2.json")},
        },
        "MATH": {
            "1": {"timeLimit": 2100, "answers": load_answers("_answers_math1.json")},
            "2": {"timeLimit": 2100, "answers": load_answers("_answers_math2.json")},
        },
    },
    "notes": (
        "EliteXSAT 2025 Nov US-A single-route form. "
        "Source PDF has no answer-key pages — keys solved from items. "
        "Figures remade as SVGs."
    ),
}

for sec in ("ENGLISH", "MATH"):
    for mod in ("1", "2"):
        nq = len(questions[sec][mod])
        na = len(meta["modules"][sec][mod]["answers"])
        assert nq == na, (sec, mod, nq, na)
        for i in range(1, nq + 1):
            q = questions[sec][mod][str(i)]
            assert q["text"].strip(), (sec, mod, i)
            ans = meta["modules"][sec][mod]["answers"][i - 1]
            ch = q["choices"]
            if ans in ("A", "B", "C", "D"):
                assert isinstance(ch, dict) and ans in ch and not ch.get("gridIn"), (
                    sec,
                    mod,
                    i,
                    ans,
                    ch,
                )
            else:
                assert ch.get("gridIn") is True, (sec, mod, i, ans, ch)
            if q.get("imageUrl"):
                assert "/pages/" not in q["imageUrl"]
                assert Path("public" + q["imageUrl"]).exists(), q["imageUrl"]

(d / "questions.json").write_text(
    json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
(d / "meta.json").write_text(
    json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

src = json.loads((d / "_rw1.json").read_text(encoding="utf-8"))
if src["5"]["choices"].get("D") == "Categorize":
    src["5"]["choices"]["D"] = "categorize"
    (d / "_rw1.json").write_text(
        json.dumps(src, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("fixed Categorize in _rw1")

print("wrote meta + questions")
print("EN M1", "".join(meta["modules"]["ENGLISH"]["1"]["answers"]))
print("EN M2", "".join(meta["modules"]["ENGLISH"]["2"]["answers"]))
print("MA M1", meta["modules"]["MATH"]["1"]["answers"])
print("MA M2", meta["modules"]["MATH"]["2"]["answers"])
