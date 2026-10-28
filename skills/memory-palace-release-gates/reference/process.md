# Process gates

Read when organising review, sign-off, queues, checkpoints and UX experiments.

## D. Process gates

- Before painting, write the item layout with label room in mind. <!-- G45 -->
- After painting, run A to D, fix and re-run. Ship only on a full pass. <!-- G46 -->
- **Independent sign-off.** The crop review sign-off for a package is done by someone other than the worker who painted it. A self-certified review counts as pending, and a package whose crop review is pending never ships. The reviewer also re-checks every open repaint-queue row for the package's spaces. <!-- G47 -->
- **Queued problems block their space.** When a package contains a space with an open row in the repaint queue, its README says how each row was fixed, or the package fails. Fixed rows are closed in the queue with the package name. <!-- G48 -->
- **Staged fixes must survive the merge.** Before a combined build ships, run the text pre-screens (gates 5 and 6) and the gate scripts on the built public data, not only on the patches. Any staged fix the combined build leaves out is listed in its README with the reason and an owner. <!-- G49 -->
- **User-reported issues ship as hotfixes.** Every review lists each issue the user reported, whether it is still live, and the package that fixes it. A user-reported issue, or any P0/P1, whose fix has passed independent review ships as its own small hotfix in the next deploy window and never waits for an unrelated combined build. If a combined build leaves out the space that carries a fix (for an unrelated exit or dependency), its README says so and the fix is split out (once, a user-reported label overlap stayed live for hours behind a combined build, and a fixed painting was dropped from a build over an unrelated exit). <!-- G50 -->
- Every time a user reports a new kind of issue, add it here as a numbered gate with the example, and add an automated check where possible. Crop review covers what scripts can't. <!-- G51 -->
- At review checkpoints, re-run every gate over the whole live site plus everything in the deploy queue and in sectors/ that's about to ship, not just new work. Confirm earlier fixes haven't regressed, and put the counts in every release report. <!-- G52 -->
- Never skip a space because someone else is repainting it: run the gates on it, report it, and leave the fix to its owner. <!-- G53 -->
- Try one small navigation or UX improvement per checkpoint, using mockups first. Keep it if it passes the gates and makes the walk clearer, and note the result here. Round 1 result: a breadcrumb trail (Village > Sector > Building > Room) that replaces Back and the sector button won clearly; hover/first-tap destination previews on painted exits help; a mini-map belongs behind a "Plan" button outside the painting. Round 2 result: the breadcrumb and previews passed gate 8 with crumbs counted; mocked next are a short "you came from" glow on the exit you entered through and non-clickable progress dots for short streets ("place 3 of 5"). Any transient caption follows the preview rule: never over a figure or item box. <!-- G54 -->

## Process lessons from later rounds

- **Show before shipping.** Show the user clean screenshots of a redone space before it goes live, and fix what they flag before starting the next space. <!-- G105 -->
- **Re-audit what is already live.** When a new gate is added, audit the spaces already shipped against it and fix them in the next release. <!-- G112 -->
- **Integration mirror check:** on every combined build, check on the contact sheets that every reflexive verb (`reflexive: true` in the room data) shows the hand mirror, not only on each package. Once, a review missed 7 missing mirrors because it trusted the package verdicts. <!-- G64 -->
