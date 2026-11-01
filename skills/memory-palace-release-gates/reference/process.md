# Review and release process

Independent art sign-off is required: the reviewer is someone other than the painter, inspects the actual images and open queue rows, and records pass/fail/pending with the input revision. Self-review remains pending. If review is unavailable, finish the reversible preparation and report the blocker; never fabricate approval.

Queued problems block the spaces they concern. Fix user-reported/P0/P1 issues promptly after review rather than waiting for unrelated rooms. Recheck on the combined build so a staged fix is not lost. Keep a small log: space, input commit/image hashes, check, verdict, reviewer and evidence path. Close only the queue rows verified fixed.

Use the change scope in builder `reference/validation.md`. Local changes get local checks and dependency review; preserve global CI and run global release checks once at integration. Shared renderer/style changes widen review. Periodic whole-site audits are separate tasks. Do not add unsolicited navigation experiments to a room-building task.

Show clean screenshots when presenting changed art, and address user feedback under the existing authorization. A reusable failure updates its canonical rule or regression fixture; consolidate and remove conflicting instructions, rather than appending every example to every prompt.
