# C9336C-FX2 photographic authenticity review

Result: **PASS_WITH_BOTTOM_FALLBACK**  
Review date: 2026-08-28 (Asia/Singapore)

## Rejected predecessor

The predecessor frozen as standard `09f05222…2df49` / web `debdc3ee…2841` was rotation-stable but failed source appearance. Its front render replaced much of the source-locked 36-port photographic face with 18 broad gray cage frames and wide center bars. Its rear render replaced real fan honeycomb, PID labels, PSU inlet detail and handle material with large dark grille rectangles, vertical bridges and blocky handles. Counts alone were not accepted as authenticity.

The full rejected evidence is preserved under `qa/superseded/pre-photographic-skin-repair-20260828/`.

## Accepted layering

- Front and rear source-photo skins are the primary opaque visible layers.
- Broad cage, port, vent, PSU/fan installed-volume, honeycomb, PID plate, IEC and management support geometry is behind each skin by at least 0.25 mm.
- Only narrow source-aligned rims, latch openings, LEDs, burgundy release edges and silhouette-bearing handle rods remain in front.
- Handle crossbars/stems were reduced to narrow sections so the photographic honeycomb, labels, surfaces and factory handle character remain visible.
- Main skins remain RGB, `OPAQUE`, `[1,1,1,1]`, `doubleSided=false`; there is no chassis `BLEND`.

## Matched-camera result

All 12 final comparison sheets were inspected at original detail: `comparisons/{standard,web}/{front,rear,left,right,top,bottom}.png`.

| Profile | Face | Rejected mean abs RGB difference | Final difference |
|---|---|---:|---:|
| standard | front | 6.277329 | 1.824464 |
| standard | rear | 4.385823 | 1.615475 |
| web | front | 6.278727 | 1.799814 |
| web | rear | 4.390209 | 1.624491 |

Feature review:

- front: Cisco/Nexus/PID control zone remains photographic; all 18 cages preserve two real QSFP28 levels, factory latch/aperture texture and lower ventilation; no broad synthetic gray panel obscures them;
- rear: both real PI2 PSU faces retain dual inlet, grille, FAIL/OK and handle photography; all three fan trays retain exact honeycomb, `NXA-FAN-65CFM-PI` label, burgundy latches and central handle appearance; the management group remains source-locked;
- side/top: independent orientation and labels remain unchanged;
- bottom: conservative declared fallback only, with no invented detail.

## Browser visual review

The regenerated `contact-sheets/` sets cover all four Three.js/Babylon.js × standard/web combinations. The 288 yaw, 16 pitch, 12 same-angle stability and 40 independent-load screenshots show no flicker, alpha jump, checker leak, disappearing face, mirror, texture/gray transition or loading-overlay mixed frame. Standard/web geometry and appearance remain equivalent at the tested cameras; engine lighting differs only in the expected neutral PBR relief shading.

The same-angle frames in every combination are byte-identical. Final hash binding and machine gates are recorded in `final-validation.json` and `hash-freeze.json`.
