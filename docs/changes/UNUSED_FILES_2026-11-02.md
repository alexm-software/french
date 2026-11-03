# Unused-file cleanup — 2026-11-02

Base: `73c86bebb8d600023eb0b8366c716ae862afd654`.

Removed **103 files / 11,220,672 bytes (10.70 MiB)** from the current tree:
- 58 obsolete card crops, whose words have current crops in different live rooms.
- 35 files belonging to the retired sprite-based garage pipeline: `content/assignment.json`, `content/rooms/garage/`, `scripts/build_garage.py`, and `scripts/qa/check_garage.py`.
- 9 files belonging to the retired original site: `content/examples/eglise/`, `content/rooms/eglise/`, `scripts/build_data.py`, `scripts/hotspots.py`, and `scripts/test_site.py`.
- The rejected `docs/room-trials/ferme-nourrir/candidate-01.png`. Its README/review now link to the historical image; the prompt, manifest and written reviews remain.

Current v2 artwork, layouts, data, vocabulary, navigation and word assignments are unchanged. The 15 unreferenced crops whose words remain in source plans are retained. Donor scenes for pending verb integrations, the v1 card-text payloads, and the conjugation cache are retained.

Validation: checked all current layout paintings and computed crop paths plus generated building/map asset references against the post-cleanup tracked-file inventory; no referenced asset is deleted. Each of the 58 removed crops has a retained live replacement. Verified the skill path check and existing planning/prompt regression fixtures. The active v2 builder changes only two comments pointing at retired code.

This is an ordinary deletion commit: historical binaries remain in Git history. No history rewrite or artwork recompression.

## Removed crop paths

- `village/ciel/cards/fr_espace_noun_f.webp`
- `village/ciel/cards/fr_lunette_noun.webp`
- `village/ciel/cards/fr_sphere_noun.webp`
- `village/foret/cards/fr_baril_noun.webp`
- `village/foret/cards/fr_broche_noun.webp`
- `village/foret/cards/fr_lame_noun.webp`
- `village/foret/cards/fr_vampire_noun.webp`
- `village/montagne/cards/fr_tombe_noun.webp`
- `village/st_bagages/cards/fr_entonner_verb.webp`
- `village/st_bricoleurs/cards/fr_costumer_verb.webp`
- `village/st_bricoleurs/cards/fr_poudrer_verb.webp`
- `village/st_brocante/cards/fr_distribuer_verb.webp`
- `village/st_brocante/cards/fr_equilibrer_verb.webp`
- `village/st_campeur/cards/fr_hisser_verb.webp`
- `village/st_campeur/cards/fr_projeter_verb.webp`
- `village/st_ciel/cards/fr_enrouler_verb.webp`
- `village/st_croissance/cards/fr_repeter_verb.webp`
- `village/st_croissance/cards/fr_reussir_verb.webp`
- `village/st_departs/cards/fr_accelerer_verb.webp`
- `village/st_departs/cards/fr_escalader_verb.webp`
- `village/st_departs/cards/fr_grimper_verb.webp`
- `village/st_flaneurs/cards/fr_pedaler_verb.webp`
- `village/st_habitudes/cards/fr_emballer_verb.webp`
- `village/st_habitudes/cards/fr_tricher_verb.webp`
- `village/st_lavoir/cards/fr_maquiller_verb.webp`
- `village/st_marees/cards/fr_piocher_verb.webp`
- `village/st_metamorphoses/cards/fr_reciter_verb.webp`
- `village/st_navigateurs/cards/fr_elancer_verb.webp`
- `village/st_navigateurs/cards/fr_rebondir_verb.webp`
- `village/st_poignees/cards/fr_accrocher_verb.webp`
- `village/st_poignees/cards/fr_allumer_verb.webp`
- `village/st_poignees/cards/fr_eteindre_verb.webp`
- `village/st_poignees/cards/fr_glisser_verb.webp`
- `village/st_poignees/cards/fr_tirer_verb.webp`
- `village/st_poignees/cards/fr_tourner_verb.webp`
- `village/st_porteurs/cards/fr_attraper_verb.webp`
- `village/st_porteurs/cards/fr_frissonner_verb.webp`
- `village/st_porteurs/cards/fr_lancer_verb.webp`
- `village/st_porteurs/cards/fr_placer_verb.webp`
- `village/st_porteurs/cards/fr_rougir_verb.webp`
- `village/st_reflets/cards/fr_feindre_verb.webp`
- `village/st_reflets/cards/fr_surgir_verb.webp`
- `village/st_reflets/cards/fr_vibrer_verb.webp`
- `village/st_remedes/cards/fr_buter_verb.webp`
- `village/st_remedes/cards/fr_gonfler_verb.webp`
- `village/st_renouveau/cards/fr_encourager_verb.webp`
- `village/st_renouveau/cards/fr_etirer_verb.webp`
- `village/st_sommeil/cards/fr_attendre_verb.webp`
- `village/st_souffle/cards/fr_coiffer_verb.webp`
- `village/st_souffle/cards/fr_couronner_verb.webp`
- `village/st_souffle/cards/fr_souffler_verb.webp`
- `village/st_soupirs/cards/fr_applaudir_verb.webp`
- `village/st_soupirs/cards/fr_crier_verb.webp`
- `village/st_soupirs/cards/fr_pleurer_verb.webp`
- `village/st_soupirs/cards/fr_rater_verb.webp`
- `village/st_soupirs/cards/fr_rire_verb.webp`
- `village/st_soupirs/cards/fr_sourire_verb.webp`
- `village/st_trouvailles/cards/fr_reserver_verb.webp`
