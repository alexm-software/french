#!/usr/bin/env python3
"""skills_paths.py - every repo path or script the skills name in `backticks` must exist.

  python3 tools/skills_paths.py        # exit 1 and list the missing ones

It checks backticked strings in skills/**/*.md that look like repo paths (contain a "/" or end in .py, .json,
.md, .tsv, .jsonl). Placeholders and globs are skipped. A bare file name is found anywhere in the repo.
"""
import re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TICK = re.compile(r"`([^`\s]+)`")
EXT = (".py", ".json", ".md", ".tsv", ".jsonl", ".js", ".yml")
# Written at run time by a tool or on another machine, so not in the repo
GENERATED = {"manifest.json", "review.json", "precheck.json", "contact.png", "out.json", "m.json", "continuity.json"}


def main():
    files = set(subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=ROOT, capture_output=True, text=True).stdout.split())
    names = {Path(f).name for f in files}
    dirs = {str(p) for f in files for p in Path(f).parents}
    missing = []
    for md in sorted((ROOT / "skills").rglob("*.md")):
        for n, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            for m in TICK.finditer(line):
                t = m.group(1).rstrip(".,:;)").lstrip("(")
                if re.search(r"[<>{}*?$]|^https?:|^#|^-", t) or t.startswith("/"):
                    continue
                if not ("/" in t or t.endswith(EXT)):
                    continue
                t2 = t.split(":")[0].split("#")[0].rstrip("/")
                if Path(t2).name in GENERATED:
                    continue
                ok = t2 in files or t2 in dirs or ("/" not in t2 and t2 in names) \
                    or any(f.endswith("/" + t2) for f in files) or any(d.endswith("/" + t2) for d in dirs)
                if not ok:
                    missing.append(f"{md.relative_to(ROOT)}:{n}: `{t}`")
    for x in missing:
        print("MISSING", x)
    print(f"skills paths: {len(missing)} missing")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
