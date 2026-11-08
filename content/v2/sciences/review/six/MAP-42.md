# Campus map edit, not integrated

Call 42. For review before it replaces `village/map/university.jpg`.

## Why call 41 lost the camera

Call 41 edited the detached faculty crop, 320×255, and also followed the eye-level Cour. The generator returned 1136×912, a new frame near that crop, not the campus 16:9. This call uses only `university.jpg` and asks for the same isometric camera.

## Files

- Prompt `e529f7426595e624eb25cad5ad29f505af6a27ee8b14fcbcb53bf531323351f9` `map-edit-42.txt`
- Original map `fd1d0c93ded43ab8173cc372095336aa07a2c58d1f222064c6e74b473ec36d1b` `village/map/university.jpg` (unchanged, 1280×720)
- Changed map `6109d9788c277d568f2d6d6becbea3bb6bbb001097a8c9d6ad005f9c70df36fa` `map-candidate-42.jpg` (1280×720)
- Original parent crop `e5212a33bc34f13892e042cce5d3e35bfcf31ecf04fc991d90fd7b30f40eb33a` `sciences-faculty-crop.png`, rect `[950, 245, 320, 255]`
- Changed parent crop `12e2a9c662eeee4d062bfef1cb6fdaac3ea15622ac5a93705b1f17e13d4ee4b8` `parent-changed.png`, same rect

## Self-screen

The isometric camera and the 1280×720 frame hold. The lycée and the Faculté des Lettres stay the same buildings in the same places. On the science faculty the roof telescope is gone, the blue glass roof remains, and a small white telescope stands on a round plinth in the front court behind a low wall and an open gate. There is no separate west wing and no east stair tower. The generator repainted the whole sheet, so pixels outside the faculty also differ, while those other schools stay recognizable. Not integrated.

The Cour's west door, west arcade, and east door are painted and have no hit targets. The live controls are the gate to Campus and the glass doors to the hall.
