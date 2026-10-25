import json, re, unicodedata
from pathlib import Path
# English gloss words with two common senses, and the theme cues (English + French, accent-free) of the sense a room
# could be built around. A word whose gloss contains the token, placed in a room whose theme shows a cue for it, is
# flagged: it may be tied to the room only by the shared English word (riverbank in the bank, "to fire" with firemen).
AMBIG = {
 "bank": r"bank|banque|guichet|coffre", "stock": r"stock|bourse|stocks?|reserve|entrepot|soupe", "firm": r"firm|entreprise|bureau|office",
 "coach": r"coach|bus|car\b|gare|diligence|sport|stade|entraineur", "fire": r"fire|feu|pompier|incendie|camp", "party": r"party|fete|celebration|politi|parti",
 "star": r"star|etoile|ciel|sky|cinema|vedette|astro", "band": r"band|music|musique|groupe|concert|orchestre", "scale": r"scale|balance|pesee|weigh|gamme|music|poisson|fish",
 "lead": r"lead|plomb|chemi|metal|chef|leader", "shot": r"shot|tir|photo|camera|medecin|vaccin", "stage": r"stage|theatre|scene|etape|route|road",
 "league": r"league|ligue|sport|lieue|distance|measure", "race": r"race|course|sport|stade|circuit|ethni|society",
 "pitch": r"pitch|terrain|stade|music|ton", "ring": r"ring|bague|bijou|boxe|cirque|piste", "match": r"match|allumette|sport|stade",
 "spring": r"spring|printemps|saison|ressort|source|fontaine", "fall": r"fall|automne|chute|saison", "seal": r"seal|phoque|sceau|tampon|admin|zoo|mer",
 "plot": r"plot|parcelle|jardin|champ|field|intrigue|theatre|roman", "deposit": r"deposit|banque|bank|caution|geolog",
 "record": r"record|disque|music|sport|archive", "trunk": r"trunk|malle|coffre|arbre|tree|elephant|voiture", "bill": r"bill|facture|addition|billet|bec|bird|oiseau",
 "check": r"check|cheque|banque|echec|controle", "court": r"court|tribunal|justice|tennis|cour\b|sport", "fair": r"fair|foire|marche|fete|juste|justice",
 "board": r"board|planche|conseil|tableau|bureau|jeu", "change": r"change|monnaie|banque|caisse|serre|transform", "post": r"post|poste|courrier|lettre|poteau|emploi",
 "train": r"train|gare|station|rail|entrain", "light": r"light|lumiere|lampe|leger|phare", "mine": r"mine|mineur|charbon|coal",
 "safe": r"safe|coffre|banque|bank|securite", "fine": r"fine|amende|police|beau", "port": r"port|harbour|navire|bateau",
 "bar": r"bar\b|cafe|comptoir|barre", "box": r"box|boite|boxe|carton", "case": r"case|valise|bagage|affaire|police|tribunal",
}
def plain(s): return unicodedata.normalize("NFKD", s.lower()).encode("ascii", "ignore").decode()
def theme_of(L, key, R, rooms_json):
    p = (L.get("planned") or {}).get(key) or {}
    rj = rooms_json.get(p.get("vocabRoom", ""), {})
    return plain(" ".join([L.get("building", ""), L.get("name", ""), key, R.get("name", ""), rj.get("name", ""), rj.get("setting", "") or ""]))
def flags(L, key, R, rooms_json, ok):
    th = theme_of(L, key, R, rooms_json)
    out = []
    for it in R["items"]:
        g = plain(it.get("en", ""))
        for tok, cue in AMBIG.items():
            if re.search(rf"\b{tok}(s|es|d|ing)?\b", g) and re.search(cue, th) and (it["id"], key) not in ok and (it["id"], "*") not in ok:
                out.append((it["id"], tok, it.get("en", "")))
    return out
def load_ok(path):
    ok = set()
    if Path(path).exists():
        for l in open(path, encoding="utf-8"):
            if l.strip() and not l.startswith("#"):
                c = l.rstrip("\n").split("\t"); ok.add((c[0], c[1]))
    return ok


def plan_report(root):
    """Print plan-room words (data/source/rooms.json) whose gloss shares an ambiguous English word with the room name."""
    V = {}
    for l in open(root / "data" / "source" / "vocab.jsonl", encoding="utf-8"):
        if l.strip(): d = json.loads(l); V[d["id"]] = d
    ok = load_ok(root / "data" / "hooks" / "qa" / "placement_ok.tsv")
    for r in json.load(open(root / "data" / "source" / "rooms.json", encoding="utf-8"))["rooms"]:
        th = plain(r["name"] + " " + (r.get("setting") or "") + " " + r["building_id"])
        for w in r["words"]:
            wid = w if isinstance(w, str) else w.get("id")
            if (wid, "*") in ok or (wid, r["id"]) in ok: continue
            g = plain(V.get(wid, {}).get("gloss", ""))
            for tok, cue in AMBIG.items():
                if re.search(rf"\b{tok}(s|es|d|ing)?\b", g) and re.search(cue, th):
                    print(f"PLAN-PLACE {r['id']} ({r['name'][:40]}): {wid} '{g[:60]}' via '{tok}'")


if __name__ == "__main__":
    plan_report(Path(__file__).resolve().parents[2])
