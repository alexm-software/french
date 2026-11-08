# Final release-readiness review: sciences hall, PR 274 head abb996dadb48643a8ea436a9488ae478b7bb5f5e

- Reviewer: Grok Bot independent reviewer
- Written: 2026-11-07, about 11:58 PM CST

## VERDICT: RELEASE-READY (not live, not merged)

## Evidence
- **Art:** d1d59540… is unchanged and holds my independent ART PASS (EDIT4_ACCEPTANCE.md, fcf14c29…).
- **Mine fix**, read remotely at the head:
  - sciences.js mine boxPx is [82,148,386,177] (x 82-468), so it encloses the ore cart.
  - The recropped card d5df09f6… was viewed. It shows the whole mound, tunnel, rails, lantern and the complete ore cart.
  - The card matches the store copy.
- **Cache:**
  - The head sw.js has V='village-v53'.
  - check_v2 --strict --placement --cache-base reports "1 changed existing image … v52 -> v53". That is required, because the mine card was recropped under the same name.
- **Evidence zip:** sciences-hall-evidence.zip, sha 51c410f9329043b102750b64b021be68c5188a371b8504f1b294a701a739f7fc, taken from cloud store artifacts and inspected.
- **Logs:**
  - check_v2_strict_placement_cache: 89 buildings, 5816 words, 642 dialogues. PASS, exit 0.
  - precheck: 0 fail / 0 warn / 0 OCR flags; 6 labels + 2 fixed rects.
  - test_sciences_hall: 7/7 OK.
  - unittest discover: 30 OK.
  - Also ran: ci_build_v2, ci_build_map, ci_build_extras.
  - ci_data_diff: only sciences.js changed after the rebuild, i.e. the committed data equals the build (exit 0).
  - copyright: 0 problems.
  - skills paths: 0 missing.
  - hook_lint: 886 findings across 5790 hooks. This is an informational global count, not a gate.
- **Click journeys** (browser_clicks.json plus screenshots), desktop and phone:
  1. #/quartier/university → #/sciences
  2. door → #/quartier/university
  3. re-enter → #/sciences
  4. Back "‹ Campus" → #/quartier/university
  - Hub hidden everywhere. The data has one mapExit and no doors, so there is one destination control.
  - The JSON lists that element under both the mapexit and doorway selectors (same href, empty id). This is a selector overlap, not two controls; the screenshot shows one door hotspot.
  - All 6 cards plus a 2-dialogue menu were captured.
- **Dialogue C_R_geology:**
  - Pre-existing: commit 446c4190, 2026-10-21, "Publish all 721 written dialogues", on main.
  - Placed by the existing 3-word rule. Respectful and all-ages. Retained correctly.
- **Previously verified at 93a6c781 and unchanged:** labels, sides, adjective forms, dialogue spans, campus identity.

## Caveats (not blocking)
- The logs are not stamped with a commit hash. Their content agrees with the head data and sw.js I read remotely.
- I did not see a GitHub Actions run on the PR. Parent: confirm the PR checks are green on abb996da before merge.
