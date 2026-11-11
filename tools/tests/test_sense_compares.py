"""Sense comparisons: reciprocal targets, generation, and card markup."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "v2"))
from sense_compares import (  # noqa: E402
    attach_compares, compares_index, load_edges, load_placements, load_vocab, validate,
)

VILLAGE = ROOT / "village"


def card_compare_html(compares):
    """The contract extras.js renders. Kept here so markup rules have a unit check."""
    if not compares:
        return ""
    parts = ['<div class="sec cmp"><h3>Not the same</h3>']
    for c in compares:
        name = c.get("hw") or c.get("fr")
        parts.append('<div class="cmp1">')
        if c.get("at"):
            b, room = c["at"]
            href = f"#/{b}" + ("" if room == b else f"/{room}") + f"?w={c['to']}"
            parts.append(f'<p><a class="goto" href="{href}"><b lang="fr">{name}</b></a></p>')
        else:
            parts.append(f'<p><b lang="fr">{name}</b> <span class="small">Not in a room yet.</span></p>')
        parts.append(f'<p>{c["note"]}</p>')
        for ex in c.get("examples") or []:
            parts.append(f'<p class="exlab">Example of {ex["who"]}</p>')
            parts.append(f'<p class="fr"><i lang="fr">{ex["fr"]}</i> '
                         f'<button class="say" aria-label="Listen: {ex["fr"]}">🔊</button></p>')
            parts.append(f'<p class="tr">{ex["en"]}</p>')
        parts.append("</div>")
    parts.append("</div>")
    return "".join(parts)


class SenseCompares(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vocab = load_vocab()
        cls.edges = load_edges()
        cls.index = compares_index(cls.edges)
        cls.placements = load_placements()

    def test_authored_file_is_valid(self):
        self.assertEqual(validate(self.vocab, self.edges), [])

    def test_reciprocal_valid_targets_and_no_self_or_duplicate(self):
        seen = set()
        for e in self.edges:
            self.assertNotEqual(e["a"], e["b"])
            self.assertIn(e["a"], self.vocab)
            self.assertIn(e["b"], self.vocab)
            key = tuple(sorted((e["a"], e["b"])))
            self.assertNotIn(key, seen)
            seen.add(key)
            back = {row["to"] for row in self.index[e["b"]]}
            forth = {row["to"] for row in self.index[e["a"]]}
            self.assertIn(e["a"], back)
            self.assertIn(e["b"], forth)
            self.assertNotIn("http", e["a_note"])
            self.assertNotIn("http", e["b_note"])

    def test_generation_keeps_compare_when_note_is_overridden(self):
        it = {"id": "fr_an_noun", "note": "from the verb table", "en": "year"}
        attach_compares(it, self.vocab, self.placements, self.index)
        self.assertEqual(it["note"], "from the verb table")
        targets = {row["to"] for row in it["compares"]}
        self.assertIn("fr_annee_noun", targets)
        annee = next(row for row in it["compares"] if row["to"] == "fr_annee_noun")
        self.assertEqual(annee["fr"], "année")
        self.assertNotIn("sources", annee)
        self.assertTrue(annee["at"] is None or (isinstance(annee["at"], list) and len(annee["at"]) == 2))

    def test_unpainted_target_has_no_fabricated_room(self):
        missing = "fr_sense_compare_unpainted_test"
        index = {"fr_an_noun": [{"to": missing, "note": "Année is elsewhere."}]}
        vocab = dict(self.vocab)
        vocab[missing] = {"id": missing, "lemma": "année", "gloss": "year"}
        it = {"id": "fr_an_noun"}
        attach_compares(it, vocab, {}, index)
        self.assertIsNone(it["compares"][0]["at"])
        self.assertIn("Not in a room yet", card_compare_html(it["compares"]))
        self.assertNotIn("<a ", card_compare_html(it["compares"]))

    def test_painted_link_uses_existing_room_route(self):
        it = {"id": "fr_savoir_verb"}
        attach_compares(it, self.vocab, self.placements, self.index)
        row = next(r for r in it["compares"] if r["to"] == "fr_connaitre_verb")
        if row["at"] is None:
            html = card_compare_html([row])
            self.assertIn("Not in a room yet", html)
            self.assertNotIn("href=", html)
        else:
            building, room = row["at"]
            self.assertTrue((VILLAGE / "data" / f"{building}.js").exists())
            html = card_compare_html([row])
            self.assertIn(f"?w={row['to']}", html)
            self.assertIn('class="goto"', html)
            self.assertIn('aria-label="Listen:', html)
            self.assertIn("<h3>Not the same</h3>", html)

    def test_audit_covers_every_exact_cluster(self):
        audit = json.loads((ROOT / "data" / "source" / "sense_compare_audit.json").read_text(encoding="utf-8"))
        totals = audit["totals"]
        self.assertEqual(totals["vocab_entries"], len(self.vocab))
        self.assertEqual(
            totals["exact_accepted"] + totals["exact_accepted_partial"] + totals["exact_unrelated"]
            + totals["exact_uncertain"] + totals["exact_equivalent"] + totals["exact_deferred_homograph"],
            totals["exact_clusters"],
        )
        bark = next(r for r in audit["exact_clusters"] if r["key"] == "noun|bark")
        self.assertEqual(bark["disposition"], "unrelated")
        stove = next(r for r in audit["exact_clusters"] if r["key"] == "noun|stove")
        self.assertEqual(stove["disposition"], "deferred_homograph")
        ids = {e["a"] for e in self.edges} | {e["b"] for e in self.edges}
        self.assertIn("fr_neuf_num", ids)
        self.assertIn("fr_neuf_adj", ids)
        self.assertIn("fr_poele_noun", ids)
        self.assertIn("fr_poele_noun_f", ids)
        self.assertIn("fr_fois_noun", ids)
        verified = [e for e in self.edges if e.get("verified")]
        self.assertTrue(verified)
        for e in verified:
            self.assertTrue(e["support"][0]["excerpt"])
            self.assertTrue(e["support"][0]["url"].startswith("https://"))
        i18n = json.loads((ROOT / "archive" / "data" / "i18n.json").read_text(encoding="utf-8"))
        extras = (ROOT / "village" / "extras.js").read_text(encoding="utf-8")
        for key in ("notTheSame", "notInARoom", "exampleOf", "noPainting"):
            self.assertIn(i18n["en"]["card"][key], extras if key != "noPainting" else (ROOT / "village" / "app.js").read_text(encoding="utf-8") + extras)
        for e in self.edges:
            self.assertTrue(e.get("support"))
            kinds = [(s.get("kind") or "quote") for s in e["support"]]
            if e.get("verified"):
                self.assertTrue(all(k == "quote" for k in kinds))
            else:
                self.assertTrue(any(k == "uncertain" for k in kinds))
        deferred = json.loads((ROOT / "data" / "source" / "sense_compare_deferred.json").read_text(encoding="utf-8"))
        self.assertEqual(deferred["deferred_unsupported"], [])
        self.assertNotIn("fr_au_det", ids)
        self.assertNotIn("fr_foot_noun", ids)
        self.assertEqual(i18n["fr"]["card"]["notTheSame"], "Pas la même chose")
        self.assertEqual(totals["published_edges"], len(self.edges))
        self.assertGreater(totals["entries_outside_candidate_clusters"], 0)
        self.assertGreater(totals["exact_clusters"], 300)

    def test_unpainted_lexicon_is_reciprocal_and_has_no_room(self):
        from sense_compares import choose_placement, write_lexicon
        self.assertGreater(write_lexicon(), 0)
        raw = (ROOT / "village" / "data" / "lexicon.js").read_text(encoding="utf-8")
        items = json.loads(raw.split("window.V2_LEXICON=", 1)[1].split(";\nwindow.V2_LEXICON_INDEX=", 1)[0])
        live = (ROOT / "village" / "data" / "live.js").read_text(encoding="utf-8")
        self.assertNotIn('"lexicon":', live)
        extras = (ROOT / "village" / "extras.js").read_text(encoding="utf-8")
        self.assertIn("#/lex?w=", extras)
        self.assertIn("lexicon.js", (ROOT / "tools" / "hook_lint.py").read_text(encoding="utf-8"))
        for it in items.values():
            self.assertTrue(it["lex"])
            self.assertNotIn("cardSrc", it)
            self.assertIsNone(choose_placement(it["id"], self.placements, self.vocab))
            if it.get("g"):
                self.assertTrue(it["art"])
            for c in it.get("compares") or []:
                self.assertTrue(c.get("at") or c.get("lex"))
                if c.get("at") is None:
                    self.assertIn(c["to"], items)
                back = next(x for x in items[c["to"]]["compares"] if x["to"] == it["id"]) if c["to"] in items else None
                if c["to"] in items:
                    self.assertIsNotNone(back)

    def test_lexicon_verbs_keep_real_groups_and_hide_hooks(self):
        from sense_compares import verb_marker, write_lexicon
        write_lexicon()
        raw = (ROOT / "village" / "data" / "lexicon.js").read_text(encoding="utf-8")
        items = json.loads(raw.split("window.V2_LEXICON=", 1)[1].split(";\nwindow.V2_LEXICON_INDEX=", 1)[0])
        verbs = [it for it in items.values() if it.get("verb")]
        self.assertGreater(len(verbs), 0)
        red = 0
        for it in items.values():
            self.assertTrue(it.get("noMnemonic"))
            self.assertNotIn("hook", it)
            w = self.vocab[it["id"]]
            scene = ((w.get("mnemonic_hook") or {}).get("scene") or "")
            if scene:
                self.assertNotIn(scene, json.dumps(it, ensure_ascii=False))
        for it in verbs:
            group, beret = verb_marker(self.vocab[it["id"]])
            self.assertEqual(it["beret"], beret)
            self.assertEqual(it["group"], group)
            if beret == "red":
                red += 1
        self.assertGreater(red, 0)
        extras = (ROOT / "village" / "extras.js").read_text(encoding="utf-8")
        self.assertIn("r[3]==='lex'", extras)
        self.assertIn("lexHash(r[0])", extras)
        self.assertIn("roomHref", extras)
        hook = (ROOT / "tools" / "hook_lint.py").read_text(encoding="utf-8")
        self.assertIn('"lexicon.js"', hook)

    def test_named_quotes_are_the_sense_the_note_uses(self):
        by = {tuple(sorted((e["a"], e["b"]))): e for e in self.edges}
        voir = by[("fr_regarder_verb", "fr_voir_verb")]
        blob = json.dumps(voir["support"], ensure_ascii=False)
        self.assertNotIn("ecouter", blob.lower())
        self.assertNotIn("écouter", blob.lower())
        self.assertIn("sans intention préalable", blob)
        self.assertIn("fixer les yeux", blob)
        jur = by[("fr_judiciaire_adj", "fr_juridique_adj")]
        jblob = json.dumps(jur["support"], ensure_ascii=False)
        self.assertNotIn("Vieilli", jblob)
        self.assertIn("tribunaux", jblob)
        self.assertIn("conforme au droit", jblob)
        con = by[("fr_competition_noun", "fr_concurrence_noun")]
        self.assertNotIn("agir de concert", json.dumps(con["support"]))
        self.assertIn("fabricants", json.dumps(con["support"], ensure_ascii=False))
        lab = by[("fr_ici_adv", "fr_la_bas_adv")]
        self.assertNotIn("morts", json.dumps(lab["support"], ensure_ascii=False))
        self.assertIn("lieu éloigné", json.dumps(lab["support"], ensure_ascii=False))
        fac = by[("fr_fac_noun", "fr_universite_noun")]
        self.assertTrue(any("wiktionary.org/wiki/fac" in s["url"] for s in fac["support"]))
        beaucoup = by[("fr_beaucoup_adv", "fr_tres_adv")]
        self.assertIn("beaucoup plus", beaucoup["a_note"] + beaucoup["b_note"])
        tantot = by[("fr_parfois_adv", "fr_tantot_adv")]
        self.assertIn("regional", (tantot["a_note"] + tantot["b_note"]).lower())
        import importlib.util
        spec = importlib.util.spec_from_file_location("quote_check", ROOT / "scripts" / "qa" / "quote_check.py")
        qc = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(qc)
        self.assertEqual(qc.problems(), [])
        for key in (
            ("fr_regarder_verb", "fr_voir_verb"),
            ("fr_judiciaire_adj", "fr_juridique_adj"),
            ("fr_competition_noun", "fr_concurrence_noun"),
            ("fr_ici_adv", "fr_la_bas_adv"),
            ("fr_fac_noun", "fr_universite_noun"),
        ):
            for s in by[key]["support"]:
                self.assertNotEqual(s.get("kind"), "paraphrase")

    def test_eight_wrong_sense_records_now_quote_the_note(self):
        by = {tuple(sorted((e["a"], e["b"]))): e for e in self.edges}
        expect = {
            ("fr_ton_det", "fr_votre_det"): "pronom personnel Tu",
            ("fr_cahier_noun", "fr_carnet_noun"): "cahier d'écolier",
            ("fr_bagnole_noun", "fr_voiture_noun"): "Véhicule automobile",
            ("fr_deces_noun", "fr_mort_noun_f"): "Cessation de la vie",
            ("fr_demission_noun", "fr_resignation_noun"): "sans se révolter",
            ("fr_figurer_verb", "fr_paraitre_verb"): "nom inscrit sur une liste",
            ("fr_apparaitre_verb", "fr_figurer_verb"): "nom inscrit sur une liste",
        }
        for key, needle in expect.items():
            blob = json.dumps(by[key]["support"], ensure_ascii=False)
            self.assertIn(needle, blob)
            self.assertNotIn("rénitence", blob)
            self.assertNotIn("après pliage", blob)
            self.assertNotIn("taudis", blob)
            self.assertNotIn("Ce n'est pas grave", blob)
            self.assertNotIn("bénéfice ecclésiastique", blob)
            self.assertNotIn("Donner une forme", blob)
            self.assertTrue(by[key]["verified"])
        car = json.dumps(by[("fr_bagnole_noun", "fr_voiture_noun")]["support"], ensure_ascii=False)
        self.assertIn("Toute voiture, toute automobile", car)

    def test_entendre_text_card_is_regular_re(self):
        from sense_compares import verb_marker, write_lexicon
        w = self.vocab["fr_entendre_verb"]
        self.assertEqual(w.get("verb_group"), 3)
        self.assertFalse(w.get("irregular"))
        self.assertEqual(verb_marker(w), ("-re", "purple"))
        write_lexicon()
        raw = (ROOT / "village" / "data" / "lexicon.js").read_text(encoding="utf-8")
        items = json.loads(raw.split("window.V2_LEXICON=", 1)[1].split(";\nwindow.V2_LEXICON_INDEX=", 1)[0])
        it = items["fr_entendre_verb"]
        self.assertEqual(it["group"], "-re")
        self.assertEqual(it["beret"], "purple")
        self.assertNotEqual(it["beret"], "gold")


if __name__ == "__main__":
    unittest.main()
