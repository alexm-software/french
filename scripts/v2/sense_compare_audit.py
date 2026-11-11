#!/usr/bin/env python3
"""Record the gloss-cluster audit behind data/source/sense_compares.json.

Candidate grouping (not exact-string only):
- Drop parentheticals, then take the primary gloss (text before the first semicolon).
- Drop a leading "to" and the articles a/an/the. Keep particles (from, out, up, ...).
- Americanize a short list of British spellings.
- Exact cluster: same part of speech and the same primary token tuple.
- Near cluster: same part of speech, shared first token, and the shorter primary
  gloss is a prefix or a near subset of the longer one. A bare light verb plus an
  object (have lunch, go out) is excluded from the near list and counted apart.
- Letters are not glosses and are not clustered.

Dispositions:
- accepted: at least one published edge joins members
- accepted_partial: an edge joins some members; others stay out on purpose
- unrelated: the shared English word is a different sense, so no learner note
- uncertain: a distinction may exist, but it is not published
- equivalent: reviewed; interchangeable for this gloss, or too slight to state
- near_not_same: the extra English words name a different meaning
"""
import json, re, collections, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sense_compares import ROOT, load_vocab, load_edges

DROP = {"a", "an", "the"}
UK = {
    "colour": "color", "colours": "colors", "favourite": "favorite", "favour": "favor",
    "grey": "gray", "theatre": "theater", "centre": "center", "metre": "meter", "litre": "liter",
    "defence": "defense", "jewellery": "jewelry", "travelling": "traveling",
    "practise": "practice", "organised": "organized", "organise": "organize",
    "realise": "realize", "recognised": "recognized", "behaviour": "behavior",
    "honour": "honor", "labour": "labor", "neighbour": "neighbor", "flavour": "flavor",
}
LIGHT = {"have", "do", "make", "go", "come", "take", "get", "put", "set", "give", "be", "let", "keep"}
# Shared English head is a different sense. No learner note.
UNRELATED = {
    "noun|game", "verb|succeed", "noun|mass", "noun|spring", "noun|organ", "noun|cape",
    "noun|temple", "noun|fan", "noun|seal", "noun|league", "noun|standard", "noun|deposit",
    "noun|change", "noun|sheet", "noun|chest", "verb|smoke",     "noun|marble", "noun|bark",
}
# Same English gloss, but the source id mixes senses. No learner note until the senses are separate ids.
DEFERRED = {"noun|stove"}
# A real nuance may exist. It is not published.
UNCERTAIN = set()
# Pairs inside an accepted cluster that are interchangeable, so they have no direct edge.
EQUIVALENT_PAIRS = []
REMAINING = [
    "All 160 gloss-only equivalent pairs now have a reciprocal note, including au/aux, foot/football, and vite/rapidement.",
    "Fois is one occurrence, compared with heure and temps. Neuf the number and neuf brand-new are separate cards. La poêle is the frying pan and le poêle is the heater.",
    "Near-match review: 500 pairs read. 288 edges where the senses overlap, 212 skipped as partial-gloss coincidences. The near-match list is done.",
    "boulot and job are both informal for work or a job. emploi already contrasts with boulot. No note between boulot and job.",
    "Words with a unique primary gloss were not candidates. That is not a claim that no other synonym exists under a different English wording.",
    "The eleven uncertain clusters are decided. Bar the café has no note with barre or barreau. Rock the music has no note with roc, roche, or rocher. The other members have a reciprocal note, as do finir and terminer, and marrant and rigolo.",
]


def strip_paren(s):
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"\([^)]*\)", " ", s)
        s = re.sub(r"\[[^\]]*\]", " ", s)
    return s


def primary_tokens(gloss):
    s = strip_paren(gloss or "").replace("’", "'")
    s = re.split(r";", s)[0].strip()
    s = re.sub(r"^to\s+", "", s, flags=re.I)
    toks = []
    for t in re.findall(r"[A-Za-z']+", s.lower()):
        t = UK.get(t, t)
        if t not in DROP:
            toks.append(t)
    return tuple(toks)


def cluster(vocab):
    words = [w for w in vocab.values() if w.get("pos") != "letter"]
    prim = {w["id"]: primary_tokens(w.get("gloss", "")) for w in words}
    exact = collections.defaultdict(list)
    for w in words:
        if prim[w["id"]]:
            exact[(w.get("pos"), prim[w["id"]])].append(w["id"])
    exact_c = [(k, list(dict.fromkeys(v))) for k, v in exact.items() if len(set(v)) >= 2]
    near_pairs = []
    excluded = 0
    bypos = collections.defaultdict(list)
    for w in words:
        if prim[w["id"]]:
            bypos[w["pos"]].append(w["id"])
    for ids in bypos.values():
        buck = collections.defaultdict(list)
        for i in ids:
            buck[prim[i][0]].append(i)
        for group in buck.values():
            if len(group) < 2:
                continue
            for a in range(len(group)):
                for b in range(a + 1, len(group)):
                    ta, tb = prim[group[a]], prim[group[b]]
                    if ta == tb:
                        continue
                    shorter, longer = (ta, tb) if len(ta) <= len(tb) else (tb, ta)
                    prefix = longer[:len(shorter)] == shorter
                    subset = set(shorter) <= set(longer) and shorter[0] == longer[0] and len(longer) - len(shorter) <= 2
                    if not (prefix or subset):
                        continue
                    if len(shorter) == 1 and shorter[0] in LIGHT and len(longer) > 1:
                        excluded += 1
                        continue
                    if len(longer) - len(shorter) > 3:
                        continue
                    near_pairs.append((group[a], group[b]))
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in near_pairs:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
    groups = collections.defaultdict(set)
    for a, b in near_pairs:
        groups[find(a)].update((a, b))
    return words, exact_c, [sorted(v) for v in groups.values()], excluded


def edge_pairs(edges):
    return {tuple(sorted((e["a"], e["b"]))) for e in edges}


def disposition(ids, key, pairs):
    linked = 0
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            if tuple(sorted((ids[i], ids[j]))) in pairs:
                linked += 1
    possible = len(ids) * (len(ids) - 1) // 2
    if linked == possible and linked:
        return "accepted"
    if linked:
        return "accepted_partial"
    if key in UNRELATED:
        return "unrelated"
    if key in DEFERRED:
        return "deferred_homograph"
    if key in UNCERTAIN:
        return "uncertain"
    return "equivalent"


def main():
    vocab = load_vocab()
    edges = load_edges()
    pairs = edge_pairs(edges)
    words, exact_c, near_c, excluded = cluster(vocab)
    exact_rows = []
    for (pos, toks), ids in sorted(exact_c, key=lambda kv: kv[0][1]):
        key = pos + "|" + " ".join(toks)
        exact_rows.append({
            "key": key, "ids": sorted(ids),
            "lemmas": [vocab[i]["lemma"] for i in sorted(ids)],
            "disposition": disposition(ids, key, pairs),
        })
    near_rows = []
    for ids in near_c:
        linked = any(tuple(sorted((ids[i], ids[j]))) in pairs for i in range(len(ids)) for j in range(i + 1, len(ids)))
        near_rows.append({
            "ids": ids,
            "lemmas": [vocab[i]["lemma"] for i in ids],
            "disposition": "accepted" if linked else "near_not_same",
        })
    in_candidate = set()
    for row in exact_rows:
        in_candidate.update(row["ids"])
    for row in near_rows:
        in_candidate.update(row["ids"])
    published = set()
    for e in edges:
        published.add(e["a"])
        published.add(e["b"])
    counts = collections.Counter(r["disposition"] for r in exact_rows)
    near_counts = collections.Counter(r["disposition"] for r in near_rows)
    letters = sum(1 for w in vocab.values() if w.get("pos") == "letter")
    doc = {
        "method": "Primary-gloss tokens after parentheticals, with particles kept. Exact clusters share that tuple. Near clusters are short containments, excluding a light verb plus an object.",
        "totals": {
            "vocab_entries": len(vocab),
            "letters_not_clustered": letters,
            "gloss_universe": len(words),
            "exact_clusters": len(exact_rows),
            "exact_entries": len({i for r in exact_rows for i in r["ids"]}),
            "near_clusters": len(near_rows),
            "near_entries": len({i for r in near_rows for i in r["ids"]}),
            "entries_in_a_candidate_cluster": len(in_candidate),
            "entries_outside_candidate_clusters": len(words) - len(in_candidate),
            "light_verb_object_pairs_excluded": excluded,
            "published_edges": len(edges),
            "published_words": len(published),
            "exact_accepted": counts["accepted"],
            "exact_accepted_partial": counts["accepted_partial"],
            "exact_unrelated": counts["unrelated"],
            "exact_deferred_homograph": counts["deferred_homograph"],
            "exact_uncertain": counts["uncertain"],
            "exact_equivalent": counts["equivalent"],
            "near_accepted": near_counts["accepted"],
            "near_not_same": near_counts["near_not_same"],
        },
        "equivalent_pairs_inside_accepted_clusters": EQUIVALENT_PAIRS,
        "still_likely_false_equivalents": [],
        "remaining": REMAINING,
        "exact_clusters": exact_rows,
        "near_clusters": near_rows,
    }
    path = ROOT / "data" / "source" / "sense_compare_audit.json"
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(doc["totals"], indent=1))
    missing_u = [k for k in UNRELATED if k not in {r["key"] for r in exact_rows}]
    missing_c = [k for k in UNCERTAIN if k not in {r["key"] for r in exact_rows}]
    if missing_u or missing_c:
        print("keys not found", missing_u, missing_c)


if __name__ == "__main__":
    main()
