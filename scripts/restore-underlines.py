import json
import re
from pathlib import Path

ROOT = Path("prisma/data")

# Markdown-style underline used in some transcriptions: _word or phrase_
UNDERSCORE_SPAN = re.compile(r"(?<![A-Za-z0-9])_([^_\n]{1,120}?)_(?![A-Za-z0-9])")
AS_USED_WORD = re.compile(
    r'As used in the text,\s*what does the word\s+[\"“”](.+?)[\"“”]',
    re.I,
)
AS_USED_PHRASE = re.compile(
    r'As used in the text,\s*what does the (?:underlined )?(?:figurative )?phrase\s+[\"“”](.+?)[\"“”]',
    re.I,
)
FUNCTION_OF_PHRASE = re.compile(
    r'function of the phrase\s+[\"“”](.+?)[\"“”]',
    re.I,
)


def already_marked(stim: str, target: str) -> bool:
    if not stim or not target:
        return False
    # already underscore or <u>
    if f"_{target}_" in stim:
        return True
    if re.search(rf"<u[^>]*>\s*{re.escape(target)}\s*</u>", stim, re.I):
        return True
    return False


def wrap_first(stim: str, target: str) -> str | None:
    """Wrap first case-sensitive occurrence of target with _target_."""
    if not stim or not target or already_marked(stim, target):
        return None
    idx = stim.find(target)
    if idx < 0:
        # try case-insensitive
        m = re.search(re.escape(target), stim, re.I)
        if not m:
            return None
        idx = m.start()
        target = stim[m.start() : m.end()]
    return stim[:idx] + f"_{target}_" + stim[idx + len(target) :]


def fix_item(item: dict) -> bool:
    text = item.get("text") or ""
    stim = item.get("stimulus") or ""
    if not stim:
        return False
    changed = False

    # Prefer explicit targets from the prompt.
    for rx in (AS_USED_WORD, AS_USED_PHRASE, FUNCTION_OF_PHRASE):
        m = rx.search(text)
        if not m:
            continue
        target = m.group(1).strip()
        if not target:
            continue
        new_stim = wrap_first(stim, target)
        if new_stim:
            item["stimulus"] = new_stim
            changed = True
            stim = new_stim
        break

    return changed


def main() -> None:
    total = 0
    for path in sorted(ROOT.glob("*/questions.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        n = 0
        for sec, mods in data.items():
            if not isinstance(mods, dict):
                continue
            for mod, qs in mods.items():
                if not isinstance(qs, dict):
                    continue
                for num, item in qs.items():
                    if isinstance(item, dict) and fix_item(item):
                        n += 1
                        print(f"{path.parent.name} {sec} M{mod} Q{num}")
        if n:
            # also sync module shards if present
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            for shard, sec, mod in (
                ("_rw1.json", "ENGLISH", "1"),
                ("_rw2.json", "ENGLISH", "2"),
            ):
                sp = path.parent / shard
                if sp.exists() and "ENGLISH" in data and mod in data["ENGLISH"]:
                    sp.write_text(
                        json.dumps(data["ENGLISH"][mod], ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8",
                    )
            print(f"  -> wrote {n} fixes to {path}")
            total += n
    print(f"Total fixed: {total}")


if __name__ == "__main__":
    main()
