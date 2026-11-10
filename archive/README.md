# Archive

These files are not read by the site or by `scripts/v2/build_v2.py`, `build_map.py`, or `build_extras.py`. They stay in git so the history is not rewritten.

| Path | What it was |
|---|---|
| `archive/data/i18n.json` | English and French UI strings for a retired shell. The painted site's labels live in `content/v2/map.json` and `village/`. |
| `archive/data/guide.json` | A guide page for that shell. |
| `archive/data/adj_forms.json` | Adjective forms produced by `scripts/build_adj_forms.py` and `scripts/finalize.py`, which are no longer in the tree. Shipped forms are on the rows in `data/source/vocab.jsonl`. |

`data/source/sectors.json` and `data/source/map.json` stay in place because older notes name those paths. Each file's `_archive` field says the same thing: the painted map is `content/v2/map.json`. Their street names and `word_count` values are a snapshot, not a live tally.
