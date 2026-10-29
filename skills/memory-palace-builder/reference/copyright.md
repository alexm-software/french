# Copyright

Read before every public release and when adding any text, data, font or code.

3. No copyright problems: write your own definitions and explanations, or use openly licensed sources with the required attribution recorded in a credits file. Generate or draw all images yourself. <!-- B59 -->
Audit everything that ships: quoted texts (prayers, poems, liturgical translations; prefer public-domain versions and check modern official translations), definitions and glosses (dictionary sources such as Wiktionary are CC BY-SA, so either attribute and share-alike or rewrite in your own words), word lists and level data (check whether redistribution is allowed), fonts (ship OFL license files), and third-party code. Keep a COPYRIGHT_AUDIT file and a shipped CREDITS page. <!-- B116 -->

## Gate for quoted texts (prayers, scripture, sayings)

1. **Find a dated public-domain edition first.** Use a text printed before 1929 (catechisms, prayer books, the Douay-Rheims or Sacy Bible, Dom Guéranger), from Wikisource or a dated scan. Copy it exactly, and keep its old spelling unless you only modernize spelling (say so in the source line).
2. **If there is none, translate the original yourself** (Latin, Greek, Polish…) and label it "this project's own translation (CC BY-SA 4.0)". Translating from a modern French or English version is copying, not translating.
3. **Never use** the current French liturgical texts (AELF, Missel romain 2021), the current English ones (ICEL 2010/2011), modern Bible translations (TOB, Bible de Jérusalem, NRSV, NAB), the Marian Fathers' Divine Mercy Diary, song lyrics or recent poems. The French Notre Père is the one exception the French bishops' liturgy office has published as public domain; cite that statement.
4. **Record it in the data.** Each text's `source` names the edition, place, year and URL (or "own translation" and the original), and says how it may be used ("public domain", "CC BY-SA 4.0" or a named permission). CREDITS.md names every quoted text.
5. **Check it.** `tools/copyright_check.py` fails a text with no dated or own-translation source, no usage statement, a mention of a current liturgical translation without saying it is not copied, wording known only from the current liturgical texts, or a title missing from CREDITS.md. It runs on every pull request. Add new modern-only phrases to its MODERN list when you meet them.
6. **When unsure, leave it out** and list it in the release notes as waiting for a source.

Lessons from the first audit: <!-- B117 -->

- Modern official liturgical translations are often copyrighted and need permission (e.g. AELF in French, ICEL in English). Use dated public-domain editions (e.g. 19th or early 20th century catechisms and prayer books on Wikisource), record each text's edition and URL in its data, and translate from the original yourself when no PD version exists. <!-- B118 -->
- Watch for license clashes: a non-commercial (NC) dataset can't be mixed into share-alike (SA) public data. Keep NC values out of the shipped files and use them only internally, with credit. <!-- B119 -->
- Rewrite copied dictionary glosses in your own words sector by sector as each sector ships (it also improves quality), in a separate original-gloss file that takes precedence in the merge. <!-- B120 -->
- Credit AI image tools and disclose AI generation where their terms ask for it. <!-- B121 -->
- The public repo needs a LICENSE for the code and a data license file that matches its share-alike sources. <!-- B122 -->
- Run the copyright check above. Every shipped text, dataset, font, image and piece of code has a known license, and the credits page lists every attribution needed. <!-- B189 -->
