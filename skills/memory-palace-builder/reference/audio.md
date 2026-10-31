# Recorded audio (ElevenLabs)

**Status: planned, not deployed.** The playback code, the recording script and the voice list are written but not merged to main, and no recordings are in the repo. Until a recording exists, every 🔊 button uses the device's own French voice, as it always has. Do not start the bulk recording until the owner says so.

## How it works (no back-end)
- The site stays static. Recordings are mp3 files committed under `village/audio/` (one folder per voice), served by GitHub Pages like the paintings.
- `village/audio/index.js` lists which texts are recorded, per voice, as 12-character text hashes. It is rebuilt by the script; never edit it by hand.
- A text is found by a hash of its whitespace-normalized form: `akey()` in `village/app.js` and `akey()` in `scripts/audio/build_audio.py` must stay identical. Change one, change both, and re-check them against each other on a few hundred real texts.
- When 🔊 is pressed, the page plays the recording in the speaker's voice; failing that, the narrator's; failing that, any voice that recorded the text; and only then the browser voice. A missing or broken file falls back to the browser voice too.
- Conversation lines, listening sentences and prayer sentences are one file per line or sentence, because the page highlights them one at a time. A scene joined into one file is for review only; the site does not use it.
- The user's speed setting maps to playback rate (0.85 = normal speed).
- The service worker caches the list network-first and the mp3s on first play, so rooms already visited play offline.

## Voices (`data/source/voices.json`)
- `n` is the narrator: headwords, examples, expressions, verb patterns, alphabet and numbers, listening passages and prayers. Use one clear, calm, standard metropolitan French voice.
- Give every recurring speaker in the conversations (the cast in `village/data/talk/index.js`) a voice of their own. A speaker missing from the file is read by the narrator.
- Cast by the cast entry (gender, age, role). Use standard metropolitan French unless the character's role says otherwise. An English-speaking character gets an English voice of their own nationality.
- Child characters: use the youngest-sounding adult library voice that fits. Do not design child voices, and never clone a real person's voice.
- Two ways to get a voice:
  - **Pick from the library:** use the connector's voice list, filtered to French and the right gender and age. Library voices may have to be added to the account (Voice Library, then Add to my voices) before the API can use them. `build_audio.py --check` reports any the key cannot use.
  - **Design one:** best for main characters, so they sound like nobody else's product. The steps are below.
- Changing a voice id makes new files for that speaker. Run `--prune` afterwards to delete the old files.

### Designing a voice with the ElevenLabs connector
1. **Write the description** with this template: age, origin and accent, role in the village, temperament, pitch and timbre, pace. For example: "A young French man in his mid-twenties, the friendly waiter of a small village café in France. Standard metropolitan French accent, warm and upbeat, a smile in his voice, clear diction at a natural conversational pace. Light, bright tenor, attentive and polite with customers."
2. **Pick the preview text** from the character's own lines on the site: 100 to 1,000 characters, language `fr`. Join lines from several of their scenes if one scene is too short. Never invent the preview text.
3. **Make one design round per character.** It costs credits and gives three takes. Never call it again to retry: each call charges a new round.
4. **Choose a take.** The owner prefers that the agent chooses, so choose it yourself and say how. The agent cannot hear audio, so choose by what can be measured:
   - prefer the slower take, which is clearer for learners;
   - when a choice matters, transcribe the takes with Scribe and keep one whose transcript matches the text exactly.
   Say which take was chosen and why. The others stay in the account if the owner wants to swap.
5. **Save the voice** as "Le Village – Name (role)", for example "Le Village – Karim (serveur)". Give it the labels project, character, language, accent, gender and age. Pass the takes not chosen as discarded.
6. **Record it:** put the new voice id in `data/source/voices.json` under the speaker's exact cast name.

Designed so far, on 30 October 2026: Karim, Maman and Papa.

## Recording
- **Bulk:** `scripts/audio/build_audio.py` calls the ElevenLabs API with the key from `ELEVENLABS_API_KEY`. It never writes the key to a file, and the key never reaches the browser.
  - `--dry-run` shows what is left to record and how many characters it will take. It needs no key.
  - `--check` tests every voice; it costs nothing.
  - `--only <kinds>`, `--buildings ...` and `--budget <characters>` limit a run.
  - `--index` only rewrites the list of recordings. `--prune` deletes recordings whose text left the site.
- **Kinds,** in recording order: words, phrases, examples, talk, listening, prayers. Each text is recorded once per voice; a file whose text is unchanged is never paid for twice; an edited text is simply recorded again.
- **Models:**
  - `eleven_multilingual_v2` for bulk (1 credit per character); it does not read bracketed tags.
  - `eleven_v4` for single scenes made in the connector, where tags such as [warmly] help. It cost about the same per character in the test scene.
  - Flash and Turbo v2.5 are cheaper but less natural. The script sends `language_code: fr` only to models that accept it.
- **Output** is mp3 at 22,050 Hz and 32 kbps, which is plenty for speech. All of it comes to roughly 100 MB in the repo.
- **Text** is exactly the text on the site, never rewritten for the voice, because the hash must match. If a short headword is read as English, fix it in the voice or the model, not in the text.
- **In the connector,** generating spends credits: one take per line when the agent chooses, and never repeat a call to retry. Put all lines of a scene on one flow. A composition node (free) can join them in order with about 0.6 s between lines, for review.
- **The cloud workspace cannot reach `api.elevenlabs.io` or the ElevenLabs file storage.** So bulk recording runs in GitHub Actions or on the owner's computer, and a clip made in the connector cannot be downloaded into the repo from there. To keep a connector recording, the owner downloads it and attaches it.

## Size and cost
Dry run on 29 October 2026, 12,321 texts in all:

| Kind | Texts | Characters |
|---|---|---|
| words | 3,901 | 36,101 |
| phrases | 503 | 9,386 |
| examples | 3,879 | 127,447 |
| talk | 3,529 | 164,524 |
| listening | 428 | 21,966 |
| prayers | 81 | 9,189 |

That is about 369,000 characters, roughly 369,000 credits on multilingual v2: more than a month on most plans. Record in stages, in the order above, and cap each run with `--budget`.

## Checking
- Before a kind goes live, transcribe a sample of about 20 recordings with Scribe and compare each to its text. Misread short words, English pronunciations and cut-off endings show up there.
- Play one conversation of each voice in the browser and check that each line uses the speaker's voice and that the highlight follows.
- Re-run `--dry-run` after a run: "already recorded" should have grown by the number recorded.
- License: check the ElevenLabs plan's terms for publishing generated audio (some plans need attribution or forbid commercial use). Name the voices and the service in `data/source/CREDITS.md` when the audio ships.

## Deployment plan (not started)
1. **Merge the code first.** Merge the claude/audio branch: the script, the voice list and the playback with fallback. With no recordings the site behaves exactly as before.
2. **Key:** the owner adds the repository secret `ELEVENLABS_API_KEY` (GitHub repository Settings, then Secrets and variables, then Actions).
3. **Workflow:** add an "Audio" workflow (.github/workflows/audio.yml, not yet written), run by hand only, with these inputs:
   - `only`: the kinds to record (default words);
   - `budget`: the most characters to spend (default 20,000);
   - `buildings`: optional.

   Its steps:
   - check out the repo and set up Python 3.12;
   - run `build_audio.py` with the inputs, passing them through environment variables, never pasted into the shell line;
   - commit `village/audio/` even when the run stopped early (out of credits), so nothing paid for is lost;
   - push to main;
   - start "Deploy GitHub Pages" with workflow_dispatch, because a push by the workflow's own token does not trigger it.

   Permissions are contents: write and actions: write, with one run at a time.
4. **Record in stages:**
   - words, then check them;
   - talk, one building at a time at first;
   - examples;
   - listening and prayers.
5. **After each stage:** run the checks above, then `--prune` if texts changed. Update CREDITS.md once, at the first stage.
6. **Afterwards, new content:** after new rooms or conversations are built, run the workflow again with the same kinds. Only the new or edited texts are recorded.

## Open items
- Write the workflow, the CREDITS entry and the README notes.
- The test scene "Le menu du jour" (café) exists only in the ElevenLabs account, as a flow and seven clips. Recording it with the script costs about 320 credits again, unless the owner downloads and attaches the seven clips.
- Voices for the remaining cast are library picks chosen from their descriptions, not heard. Design voices for the main recurring characters (Léa, Tom, Papi Henri, Mme Roux, Père Antoine) before recording talk.
- A native-speaker spot check of the recordings.
