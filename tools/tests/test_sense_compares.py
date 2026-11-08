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
        self.assertNotIn("fr_neuf_num", ids)
        self.assertNotIn("fr_poele_noun", ids)
        verified = [e for e in self.edges if e.get("verified")]
        self.assertTrue(verified)
        for e in verified:
            self.assertTrue(e["support"][0]["excerpt"])
            self.assertTrue(e["support"][0]["url"].startswith("https://"))
        i18n = json.loads((ROOT / "data" / "i18n.json").read_text(encoding="utf-8"))
        extras = (ROOT / "village" / "extras.js").read_text(encoding="utf-8")
        for key in ("notTheSame", "notInARoom", "exampleOf"):
            self.assertIn(i18n["en"]["card"][key], extras)
            self.assertIn(i18n["fr"]["card"][key], (ROOT / "data" / "i18n.json").read_text(encoding="utf-8"))
        self.assertEqual(totals["published_edges"], len(self.edges))
        self.assertGreater(totals["entries_outside_candidate_clusters"], 0)
        self.assertGreater(totals["exact_clusters"], 300)


if __name__ == "__main__":
    unittest.main()
