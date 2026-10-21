# Credits & licences

| Source | Used for | Licence | Notes |
|---|---|---|---|
| **Lexique 3.83** (New, Pallier et al., lexique.org) — `sources/Lexique383.tsv` | lemma list, POS, gender, frequency (film+book per million), syllables → respelling, phonology fallback | **CC BY-SA 4.0** | Fields `frequency`, `respelling` (derived), parts of `gender`/`pos` are derived from Lexique → share-alike applies to those fields. |
| **FLELex – TT Beacco** (François et al., CENTAL, UCLouvain) — `sources/FleLex_TT_Beacco.tsv` | first CEFR estimate, `cefr_flelex`, `flelex_freq`, part of the re-grade key | **CC BY-NC-SA 4.0** | ⚠ **Non-commercial.** If the site is commercial, drop `cefr_flelex`/`flelex_freq` and re-run `assign.py` with frequency-only grading (re-grade key then uses Lexique only), or obtain permission from CENTAL. |
| **Wiktionary** (French entries) via **kaikki.org** Wiktextract dump — `sources/kaikki-French.jsonl` | glosses (`gloss_source` = "Wiktionary via kaikki.org…"), IPA, topical categories, plurals, feminine forms, synonyms/antonyms (`related`, `opposites`) | **CC BY-SA 4.0** (and GFDL) | Attribution per field: any entry whose `gloss_source` starts with "Wiktionary" carries a shortened Wiktionary gloss and must be shown with attribution and shared alike. `ipa` is Wiktionary-derived unless listed in `curated/pron_fix.tsv`. Entries with `gloss_source: original` were written for this project. |
| **all-MiniLM-L6-v2** (sentence-transformers) | gloss embeddings used for room assignment only (no output text) | Apache-2.0 | Model files in `../models`, not redistributed with the data. |
| cmudict, google-10000-english | downloaded to `sources/`, **not used** in outputs | BSD / unclear | Can be deleted. |
| Project-original content | mnemonic hooks (`hooks/*.tsv` and templates in `finalize.py`), room/sector/street design, conversation premises, grammar rules, curated lemmas (`curated/extra_lemmas.txt`), phrases, idioms glosses, opposites | yours (suggest CC BY-SA 4.0 for the whole data set, compatible with the inputs) | Hooks are the author's own wording. |

## Prayers (`prayers.json`)
All eleven prayers are ancient/traditional texts in the public domain in their traditional French and English forms: Notre Père (2017 French missal wording), Je vous salue Marie, Gloire au Père, Symbole des Apôtres, Angélus, Divine Mercy short prayers, Souvenez-vous (Memorare), Bénédicité (French family grace; English is our translation), Requiem aeternam, Agnus Dei, Sanctus.
Caveats recorded per prayer in its `source` field:
- **Current official liturgical translations** of the Mass parts (Agnus Dei, Sanctus, and the modern Notre Père) are © **AELF** (French) and © **ICEL 2010** (English). The texts here are the traditional/common forms; verify with AELF/ICEL before commercial publication.
- Divine Mercy: the short prayers are public devotional texts; translations of St Faustina's *Diary* are © Marian Fathers and are not reproduced.

## Content policy notes
Vulgar and sexual/drug terms are excluded editorially (`curated/blocklist.txt`, `curated/excluded_sensitive.txt`); mature-but-necessary words (death, crime, medical) are kept with `display: "museum_text"`.
