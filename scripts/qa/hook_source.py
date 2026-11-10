#!/usr/bin/env python3
"""vocab.jsonl is the source for a word's hook, except two painted variants.

A hooks.json or vocab_fixes.json "hook" may repeat that scene. It may not
disagree with it. Words listed in data/hooks/qa/two_hooks_ok.tsv keep a
per-painting hook. fr_boulier_noun has no vocab row; its kept card stays.

  python3 scripts/qa/hook_source.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TWO = ROOT / "data" / "hooks" / "qa" / "two_hooks_ok.tsv"
KEEP_WITHOUT_VOCAB = {"fr_boulier_noun"}


def vocab_scenes():
    out = {}
    with open(ROOT / "data" / "source" / "vocab.jsonl", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            w = json.loads(line)
            out[w["id"]] = ((w.get("mnemonic_hook") or {}).get("scene") or "")
    return out


def two_hooks():
    ids = set()
    for line in TWO.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        ids.add(line.split("\t", 1)[0])
    return ids


def main():
    scenes = vocab_scenes()
    exempt = two_hooks() | KEEP_WITHOUT_VOCAB
    problems = []
    checked = 0
    files = list((ROOT / "content" / "v2").glob("*/hooks.json"))
    files.append(ROOT / "content" / "v2" / "vocab_fixes.json")
    for path in files:
        raw = json.loads(path.read_text(encoding="utf-8"))
        rel = path.relative_to(ROOT)
        for wid, entry in raw.items():
            if not isinstance(entry, dict) or "hook" not in entry or str(wid).startswith("_"):
                continue
            if wid in exempt:
                continue
            checked += 1
            scene = scenes.get(wid)
            if scene is None:
                problems.append(f"{rel}: {wid} has a hook but no vocab.jsonl row")
            elif entry["hook"] != scene:
                problems.append(f"{rel}: {wid} hook does not match vocab.jsonl")
    if problems:
        print("\n".join(problems[:40]))
        print(f"{len(problems)} hook source problem(s)")
        return 1
    print(f"hook source: {checked} overrides match vocab.jsonl ({len(exempt)} exempt ids)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
