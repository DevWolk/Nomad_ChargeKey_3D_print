# Nomad ChargeKey 240W cap: knowledge base

Status 2026-10-27: v6 checked in CAD, not yet printed. All dimensions in mm.

## Goal and constraints
- Tight double cap for the two USB-C plugs of the Nomad ChargeKey 240W keychain cable (USB-C to USB-C, 12 cm). This model ships without a cap.
- Printer: Bambu Lab A1 mini, 0.4 mm nozzle, black PLA. A friend prints; the owner has the cable.
- The owner has no calipers. Measurements use objects of known thickness.

## Current state
- Print `Nomad_ChargeKey_cap_black_v6.stl`. Put `Nomad_ChargeKey_cap_black_v5_1.stl` on the same plate as a backup.
- Sources: `build_cap.py` (CadQuery) and `Nomad_ChargeKey_cap.scad` (OpenSCAD). Same model; both default to v6.

| Parameter | v6 | v5.1 |
|---|---|---|
| Plug pitch in the model | **6.8** | 6.9 |
| Channel, width × thickness | 8.45 × 2.60 | 8.45 × 2.60 |
| Clearance per side, width / thickness | 0.10 / 0.10 | 0.10 / 0.10 |
| Leaf grip | 0.36 | 0.36 |
| Leaf width | **3.0** | 2.4 |
| Real pitch accepted by the rigid walls | 6.6–7.0 | 6.7–7.1 |
| Leaf bend on the ChargeKey, real pitch 6.75–6.95 | 0.34–0.44 | 0.29–0.39 |
| Front recess | 11.85 × 14.2 × 0.6 | same |
| Body | 13.4 × 15.8 × 11.5 | same |
| PLA mass | ~2.2 g | ~2.2 g |

Files:
- `KNOWLEDGE_BASE.md`, `README.md`
- `build_cap.py`, `Nomad_ChargeKey_cap.scad`
- `Nomad_ChargeKey_cap_black_v6.stl`, `Nomad_ChargeKey_cap_v6.step`
- `Nomad_ChargeKey_cap_black_v5_1.stl`, `Nomad_ChargeKey_cap_v5_1.step`
- `parameters.json`, `validation.json`: output of the last build (v6)

Files of older versions are deleted. Their parameters are in [Version history](#version-history). v4.1 and v5.1 rebuild with one command each; see [Rebuild](#rebuild).

## Cable facts
- USB-C plug shell (USB-IF Type-C Compliance Document Rev 2.1b, Table B-1): 8.25 × 2.40, length 6.65, width and thickness ±0.03.
- The ChargeKey tips are magnetic and snap together; the metal housings touch. The plugs cannot move closer. They can move apart only against the magnets.
- No published dimensions. Nomad and retailers list only 12 cm, 240 W, 10 Gbps and the magnetic tips.
- Metal housings, by ruler with the tips joined: ~11.4 wide, ~13.5 thick for both together.
- **Plug pitch ≈ 6.8–6.95** (gap between the plugs + 2.4). Measured with the tips joined:

| Method | Result | Gap | Pitch |
|---|---|---|---|
| 4 mm hex bit, flats to the plugs | loose | > 4.0 | > 6.4 |
| 5 mm hex bit, flats to the plugs | does not enter | < ~5.0 | < ~7.4 |
| Torx T27 bit (5.10 point to point), lobe gaps to the plugs | snug | ~4.4–4.55 | **~6.8–6.95** |
| Ruler | — | ~4.2–4.4 | ~6.6–6.8 |
| Notebook paper | 40 sheets fit | ~4.4 at 0.11 per sheet | — |
| Photo, by eye | pitch ≈ 2.8–2.9 × plug thickness | — | ~6.7–7 |
| Housing thickness by ruler | 13.5 / 2 | — | ~6.75 |

The T27 width with lobe gaps facing the plugs is estimated from the star geometry; the exact profile is unknown.

## Design
- Closed 1.2 floor on the bed, two blind stadium channels open upwards, entry chamfer.
- Front recess, 0.6 deep, for the ends of the metal housings; rim ≥ 0.75.
- Wave texture on four walls: grooves 0.30 deep, 0.55 wide.
- Retention: one spring leaf per channel, on the outer wall.
  - 0.8 thick; 3.0 wide in v6, 2.4 before.
  - Free length ~7.6 (z 2.0–9.6). Grip pad at z ≈ 8.0–8.7, ramps above and below.
  - The leaf presses the plug towards the middle of the cap. No pins enter the plugs.
- A hidden well behind each leaf, with a 0.75 ceiling under the front face. No slots show on the outside.
- Each channel is asymmetric by design: leaf, pad and well on the outer wall, plain inner wall. The two channels mirror each other.

Formulas, the same in both sources. p = pitch in the model, P = real pitch, clearances per side:
- channel = (8.25 + 2·width_clearance) × (2.40 + 2·height_clearance)
- leaf inner face: y = p/2 + channel_thickness/2
- grip pad: y = p/2 + 1.2 − grip_interference
- well: from (leaf face − 0.55) to (leaf face + 0.8 + 0.65); width = leaf width + 1.2
- rigid walls accept P within p ± 2·height_clearance
- leaf bend on the ChargeKey (plugs cannot move closer): grip + (P − p)/2
- leaf bend on one loose plug: grip − height_clearance (the plug moves away from the leaf)
- wall behind the well at the grooves ≥ 0.75 → body height ≥ 2·(well edge + 0.3 + 0.75)
- rim ≥ 0.75 → body ≥ recess + 1.5 on each axis

Leaf loads:
- force F ≈ 3·E·I·δ / L³, with I = width · 0.8³ / 12 and L ≈ 6.35 to the pad
- root strain ε ≈ 0.03·δ (δ in mm): 1.2 % at δ = 0.4, 1.35 % at δ = 0.45. That is near the limit for PLA bending across layers.

## Conclusions
1. **v2 was loose** because the plug could move 0.25 away from a pad that pressed 0.20. A leaf grips only when the plug has nowhere to go.
2. **Felt play is larger than real play.** 0.5 of clearance over the 6.65 plug tilts the cap ~4°, which is ~1 at its edge.
3. **Do not test with a single plug from another cable.** It does not test the pitch and understates the grip. Test on the ChargeKey with the tips joined.
4. **Do not scale in the slicer.** It shrinks pitch, leaves and recess together. The −0.6 mm print (~95.5 %, pitch ~5.73) held only by squeezing the plugs together. PLA creeps under constant load, faster when warm, so that fit will loosen.
5. **The early pitch of 6.0, estimated from photos, was wrong.** The real pitch is ~6.8–6.95. Measure on the cable first; screwdriver bits work without calipers.
6. **Add grip with leaf width, not bend.** Force scales with width at the same strain. Bend above ~0.4 risks a crack at the leaf root.
7. **The 8.45 channel width is not confirmed.** The −0.6 print was tight only on both ChargeKey plugs, through squeezing; a single plug in its 8.45 × 2.77 channel wobbled and fell out.
8. **STL export from CadQuery/OCCT is not byte-reproducible.** A rebuild gives the same geometry with a different triangle order. Compare geometry, not checksums.

## Version history

| Version | Pitch | Clearance w / t | Grip | Leaf width | Channel | Recess | Body | Outcome |
|---|---|---|---|---|---|---|---|---|
| v2 (earlier agent) | 6.0 | 0.30 / 0.25 | 0.20 | 2.4 | 8.85 × 2.90 | 11.6 × 12.6 | 13.4 × 14.2 | Printed. Very loose on one plug of another cable. |
| tight (another agent) | 6.0 | 0.22 / 0.18 | 0.32 | 2.4 | 8.69 × 2.76 | 11.6 × 12.6 | 13.4 × 14.2 | Not printed. Effective grip ~0.14. |
| v3 | 6.0 | 0.10 / 0.12 | 0.38 | 2.4 | 8.45 × 2.64 | 11.6 × 12.6 | 13.4 × 14.2 | Not printed. Wrong pitch. |
| v2 scaled −0.6 in the slicer | ~5.73 | — | — | ~2.3 | ~8.45 × 2.77 | ~11.1 × 12.0 | ~12.8 × 13.6 | Printed. Very tight on the ChargeKey (squeeze); one plug falls out; housings rest on the rim. |
| v4 | 6.9 | 0.10 / 0.12 | 0.32 | 2.4 | 8.45 × 2.64 | 11.6 × 14.2 | 13.4 × 15.8 | Not printed. Recess too narrow for 11.4 housings. |
| v5 (owner) | 6.9 | 0.10 / 0.10 | 0.36 | 2.4 | 8.45 × 2.60 | 11.6 × 14.2 | 13.4 × 15.8 | Not printed. v4 with two values changed. |
| v4.1 | 6.9 | 0.10 / 0.12 | 0.32 | 2.4 | 8.45 × 2.64 | 11.85 × 14.2 | 13.4 × 15.8 | Not printed. |
| v5.1 | 6.9 | 0.10 / 0.10 | 0.36 | 2.4 | 8.45 × 2.60 | 11.85 × 14.2 | 13.4 × 15.8 | Backup. |
| **v6** | **6.8** | 0.10 / 0.10 | 0.36 | **3.0** | 8.45 × 2.60 | 11.85 × 14.2 | 13.4 × 15.8 | **Current.** |

## v6 checks
- `validate()` in `build_cap.py`:
  - one connected solid;
  - standard plugs at pitch 6.6 / 6.8 / 7.0 clear the rigid walls;
  - 11.4 × 6.75 housings clear the recess.
- STL: closed (0 open edges), 174,996 triangles, 1796 mm³.
- Cross-sections of the STL:
  - y: channel walls ±2.1 / ±4.7, pad ±4.24, leaf to ±5.5, well to ±6.15, recess ±7.1;
  - x: leaf and pad ±1.5, well ±2.1, recess ±5.925.
- `.scad` rendered in OpenSCAD 2021.01 (~30 s): all asserts pass; cross-sections match the CadQuery STL.

## Next steps
1. Print v6 and v5.1 on one plate: 100 % scale, PLA, floor on the bed, openings up, no supports, 0.12–0.16 layers, 3 walls, 100 % infill. Well ceilings are short bridges, 2.0 × 4.2. Mark the parts after printing; they look identical.
2. Fit each on the ChargeKey with the tips joined.
3. Check: goes on fully; holds when shaken and hung upside down; housings enter the recess; leaves intact.
4. Adjust and rebuild if needed.

## If the fit is wrong
| Symptom | Change |
|---|---|
| Too tight, or a leaf cracked | Use v5.1, or grip_interference 0.32, or pitch_estimated 6.85–6.9 |
| Does not go on | Check the pitch; height_clearance 0.15 (accepts ±0.3) |
| Tight across the width | width_clearance +0.03…0.05 |
| Loose | pitch_estimated 6.75 (bend +0.025), or width_clearance 0.06–0.08. Do not raise grip above 0.36 at pitch 6.8. |
| Housings do not enter the recess | Grip is unaffected: the cap sits 0.6 higher and the pads still cover the plugs. Optional: front_recess = 0. |

Bambu Studio "X-Y hole compensation" (Quality → Precision; positive values enlarge holes; the Bambu wiki suggests ~0.05 for PLA) can adjust holes without a rebuild. Unverified for slot-shaped holes.

## Rebuild
OpenSCAD:
- Open `Nomad_ChargeKey_cap.scad`. Edit parameters in the Customizer, F6 to render, F7 to export STL. No libraries needed.
- Command line: `"C:\Program Files\OpenSCAD\openscad.com" -o out.stl Nomad_ChargeKey_cap.scad` (~30 s). Override a value with `-D grip_interference=0.32`.
- Hidden constants (not in the Customizer): `finger_w`, `well_w`, `recess_w`, `recess_h`.

CadQuery 2.8:
- Setup: `uv venv venv && uv pip install --python venv/bin/python cadquery`
- `venv/bin/python build_cap.py` builds v6.
- `venv/bin/python build_cap.py v5_1 pitch_estimated=6.9 grip_interference=0.36 finger_width=2.4 relief_width=3.6`
- `venv/bin/python build_cap.py v4_1 pitch_estimated=6.9 height_clearance=0.12 grip_interference=0.32 finger_width=2.4 relief_width=3.6`
- General form: `build_cap.py NAME key=value ...` with keys from `P`.
- Output: `Nomad_ChargeKey_cap_black_NAME.stl`, `Nomad_ChargeKey_cap_NAME.step`, plus `parameters.json` and `validation.json` for the last build. ~7 s.

After a change:
- check that the STL is closed;
- check cross-sections at z ≈ 5.0 / 8.35 / 11.2 (channel, pad, recess);
- render the `.scad` and compare.

WSL memory:
- trimesh `contains()` on an 8 MB STL without Embree once used all WSL RAM.
- Take dimensions from the sources. Run heavy jobs under `systemd-run --user --scope -p MemoryMax=4G ...`.
- For STL cross-sections, numpy is enough: read the binary STL and intersect the triangles with a plane.

## Open questions
- How v6 and v5.1 fit on the ChargeKey.
- Exact pitch: 6.8–6.95 by bits, ~6.75 by ruler.
- Whether an 8.45 channel holds a plug on this printer without the leaves.
- Leaf life over repeated fitting.

## Sources
- USB Type-C Connectors and Cable Assemblies Compliance Document Rev 2.1b, Table B-1, p. 49: https://www.usb.org/sites/default/files/USB%20Type-C_Compliance%20Document_Rev_2_1b_June_2021.pdf
- Nomad ChargeKey V2 (240 W, magnetic tips): https://nomadgoods.com/products/chargekey-v2
- Length 12 cm: https://www.dq-solutions.ch/en/nomad-chargekey-magnetic-usb-c-auf-usb-c-charging-cable-0-12-m-black-ipk236
- Torx sizes (T27 = 5.10 point to point): https://en.wikipedia.org/wiki/Torx
- Bambu Wiki, X-Y hole/contour compensation: https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation
