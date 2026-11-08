#!/usr/bin/env python3
"""Check published comparison quotes against the recorded source text.

A support item is a quote, a paraphrase, or uncertain.
A quote must occur in the text recorded for its URL, and that URL must be a
page for one of the two words. Being a substring does not prove the sense.
kind uncertain means the line was not confirmed and is not a verification.

  python3 scripts/qa/quote_check.py            # fail if a quote is missing or off-page
  python3 scripts/qa/quote_check.py --fetch    # record source text for every quote URL
  python3 scripts/qa/quote_check.py --label    # mark excerpts that are not in the recording as paraphrases
"""
import html, json, re, sys, time, unicodedata, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EDGES = ROOT / "data" / "source" / "sense_compares.json"
VOCAB = ROOT / "data" / "source" / "vocab.jsonl"
CORPUS = ROOT / "data" / "source" / "sense_quote_corpus.jsonl"

# Sense the note does not use. Present on the page, so a substring check would still pass.
REJECT = {
    ("fr_voir_verb", "fr_regarder_verb"): ("écouter", "cf. regarder et voir"),
    ("fr_judiciaire_adj", "fr_juridique_adj"): ("Vieilli. Qui se fait devant la justice",),
    ("fr_concurrence_noun", "fr_competition_noun"): ("agir de concert", "Fait d'être ensemble"),
    ("fr_ici_adv", "fr_la_bas_adv"): ("séjour des morts", "au-delà"),
    ("fr_la_adv", "fr_la_bas_adv"): ("séjour des morts", "au-delà"),
    ("fr_ton_det", "fr_votre_det"): ("rénitence", "tissu organique"),
    ("fr_cahier_noun", "fr_carnet_noun"): ("après pliage",),
    ("fr_bagnole_noun", "fr_voiture_noun"): ("par tête", "taudis", "Mansarde"),
    ("fr_deces_noun", "fr_mort_noun_f"): ("Ce n'est pas grave",),
    ("fr_demission_noun", "fr_resignation_noun"): ("bénéfice ecclésiastique",),
    ("fr_figurer_verb", "fr_paraitre_verb"): ("Donner une forme",),
    ("fr_apparaitre_verb", "fr_figurer_verb"): ("Donner une forme",),
}


def fold(s):
    s = s.replace("œ", "oe").replace("æ", "ae")
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


def norm(s):
    s = html.unescape(s or "")
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u00a0", " ")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def plain_wiki(s):
    s = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", r"\1", s)
    s = re.sub(r"\{\{[^{}]*\}\}", " ", s)
    s = s.replace("''", "")
    return norm(s)


def load_vocab():
    out = {}
    for line in VOCAB.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            out[row["id"]] = row
    return out


def load_edges():
    return json.loads(EDGES.read_text(encoding="utf-8"))["edges"]


def load_corpus():
    out = {}
    if not CORPUS.exists():
        return out
    for line in CORPUS.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            out[row["url"]] = row["text"]
    return out


def excerpt_in(excerpt, text):
    n, t = norm(excerpt), norm(text)
    if n and n in t:
        return True
    return bool(n) and norm(plain_wiki(excerpt)) in plain_wiki(text)


def page_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": "french-vocab-quote-check/1.0"})
    raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    if "wiktionary.org" in url:
        # action=raw is the recorded page. A definition URL is fetched as raw too.
        if "action=raw" not in url:
            title = urllib.parse.unquote(url.rstrip("/").rsplit("/", 1)[-1])
            raw_url = "https://fr.wiktionary.org/w/index.php?title=" + urllib.parse.quote(title) + "&action=raw"
            req = urllib.request.Request(raw_url, headers={"User-Agent": "french-vocab-quote-check/1.0"})
            raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
        return raw
    raw = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), raw)
    defs = []
    for d in re.findall(r"s-definition'>(.*?)</span>", raw):
        d = re.sub(r"<[^>]+>", "", d)
        d = norm(d)
        if d and d not in defs:
            defs.append(d)
    return "\n".join(defs)


def fetch():
    urls = []
    for e in load_edges():
        for s in e.get("support") or []:
            if s.get("url") and s["url"] not in urls:
                urls.append(s["url"])
    have = load_corpus()
    mode = "a" if CORPUS.exists() else "w"
    with CORPUS.open(mode, encoding="utf-8") as fh:
        for i, url in enumerate(urls):
            if url in have and have[url]:
                continue
            try:
                text = page_text(url)
            except Exception as exc:
                print(f"ERR {url} {exc}", file=sys.stderr)
                time.sleep(0.4)
                continue
            fh.write(json.dumps({"url": url, "text": text}, ensure_ascii=False) + "\n")
            fh.flush()
            have[url] = text
            print(f"{i:03d} {len(text)} {url}")
            time.sleep(0.2)
    print(f"recorded {len(have)}")


def problems(edges=None, corpus=None, vocab=None):
    edges = edges if edges is not None else load_edges()
    corpus = corpus if corpus is not None else load_corpus()
    vocab = vocab if vocab is not None else load_vocab()
    out = []
    for e in edges:
        pair = tuple(sorted((e["a"], e["b"])))
        lemmas = [fold(vocab[e["a"]]["lemma"]), fold(vocab[e["b"]]["lemma"])]
        notes = (e.get("a_note") or "") + " " + (e.get("b_note") or "")
        for s in e.get("support") or []:
            excerpt, url = s.get("excerpt") or "", s.get("url") or ""
            kind = s.get("kind") or "quote"
            if kind not in ("quote", "paraphrase", "uncertain"):
                out.append(f"{pair}: kind must be quote, paraphrase, or uncertain")
                continue
            for bad in REJECT.get(pair, ()):
                if bad.lower() in excerpt.lower() or bad.lower() in url.lower():
                    out.append(f"{pair}: rejected sense or page ({bad})")
            if kind in ("paraphrase", "uncertain"):
                continue
            path = fold(urllib.parse.unquote(url)).replace("’", "'").replace("_", " ")
            if not any(lem and lem.replace("’", "'") in path for lem in lemmas):
                out.append(f"{pair}: quote URL is not a page for either word ({url})")
            text = corpus.get(url)
            if text is None:
                out.append(f"{pair}: no recorded source text for {url}")
            elif not excerpt_in(excerpt, text):
                out.append(f"{pair}: excerpt is not in the recorded page {url}: {excerpt[:80]}")
            if re.search(r"\b(vieilli|vx ou)\b", excerpt, re.I) and not re.search(r"old|older|dated|regional|vieilli", notes, re.I):
                out.append(f"{pair}: old-sense quote without saying so")
        kinds = [(s.get("kind") or "quote") for s in e.get("support") or []]
        if e.get("verified") and any(k != "quote" for k in kinds):
            out.append(f"{pair}: verified but a support line is not a confirmed quote")
        if pair == ("fr_fac_noun", "fr_universite_noun"):
            if not any("fac" in fold(urllib.parse.unquote(s.get("url") or "")) for s in e.get("support") or []):
                out.append(f"{pair}: fac has no quote of its own")
    return out


def label():
    doc = json.loads(EDGES.read_text(encoding="utf-8"))
    corpus = load_corpus()
    vocab = load_vocab()
    n = 0
    for e in doc["edges"]:
        lemmas = [fold(vocab[e["a"]]["lemma"]), fold(vocab[e["b"]]["lemma"])]
        for s in e.get("support") or []:
            if s.get("kind") in ("paraphrase", "uncertain"):
                continue
            url, excerpt = s.get("url") or "", s.get("excerpt") or ""
            path = fold(urllib.parse.unquote(url))
            text = corpus.get(url)
            ok = text is not None and excerpt_in(excerpt, text) and any(lem and lem in path for lem in lemmas)
            if not ok:
                s["kind"] = "paraphrase"
                n += 1
    EDGES.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"labeled {n} paraphrases")


def main():
    if "--fetch" in sys.argv:
        fetch()
        return
    if "--label" in sys.argv:
        label()
        return
    found = problems()
    if found:
        print("\n".join(found[:40]))
        raise SystemExit(f"{len(found)} quote problem(s)")
    print(f"quotes ok ({len(load_edges())} edges)")


if __name__ == "__main__":
    main()
