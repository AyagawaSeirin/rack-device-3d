# Rotation and exact-appearance review — Huawei CE5850-48T4S2Q-EI / CE5850-EI-B00

Final status: **PASS_WITH_BOTTOM_FALLBACK**

## Frozen identity and authenticity

- Exact subject: Huawei CloudEngine `CE5850-48T4S2Q-EI`, complete bundle `02359104 / CE5850-EI-B00`, 1U.
- User/canonical front (+Z): 48 GE RJ45 in four 2×6 blocks, 4 SFP+ in 2×2, 2 QSFP+ vertical; no HI breakout indicator row.
- Power side: `PAC-150WA / FAN-40EA-F / Console+ETH+USB / FAN-40EA-F / PAC-150WA`, all installed; power-side intake / port-side exhaust.
- Body 442 × 43.6 × 420 mm; verified separate front mounting ears give a 482.6 mm rack span.
- Current Huawei Info-Finder PID recheck confirms the EI chassis. No public exact downloadable official 3D binary was exposed.
- All 22 inventory rows are mapped to final actual-GLB evidence in `feature-inventory-verification.csv`; 12 final matched-camera source/render/overlay/difference sets are under `matched-camera/`.

## Before/after hashes

| GLB | Pre-review SHA-256 | Final SHA-256 | Final bytes |
|---|---|---|---:|
| standard | `95b8405d072e9cbdcce30b78be723fa2baef75c68464ea4e05d6f7fd9e75db1c` | `8c8a4a78ca6bc022c55b70f884f1766a38b6817fe33e0fe7122b51feea683038` | 13,463,996 |
| web | `d64f0ec516b486631e64bd143e2be6ec1a3f5ec0f784add7cae675fd87b704d4` | `ea9b237307b6aaeeb1c1d3c1e90533edda737cdf33561cd06b82309bb47e1c09` | 7,444,112 |

The pre-review model, views, source builder and complete QA/load/report tree are preserved at `qa/superseded/pre-rotation-review-20260827/`; the existing forced-review checkpoint remains intact.

## Reproduction and root cause

- Visible full-surface dropout was not reproduced in the valid baseline 4×88 frame matrix.
- Structural precursor was present: side/bottom cards were only 0.2 mm from the broad shell, multiple ear/port/module faces were exactly tangent to source cards, and large solid port/power relief boxes obscured the locked Huawei photographs. These conditions are viewer-depth-sensitive and violate the required stable layer hierarchy even without a baseline flash.

## Repair

- Increased only the hidden closed-shell inset from 0.2 to 0.8 mm; external dimensions, cards, ports, modules and ears did not move.
- Rebuilt front port relief as thin, intersecting cage rails so the exact 48/4/2 source face remains visible; moved C14, fan-field and management backings behind the rear source card while retaining true seams/handles.
- Rebuilt the ear/body joint with a non-coplanar intersecting tongue while preserving the 482.6 mm span and real ear openings.
- Removed all exact source-card/relief and source-card/backing tangencies. Main faces remain OPAQUE, `[1,1,1,1]`, single-sided and unlit in both standard/web.

## Final gates

- `audit_views`: PASS, 0 errors / 0 warnings (front texture correctly audited at 442 mm because the ears are separate geometry).
- `audit_glb`: standard/web PASS, 0 errors / 0 warnings; exact 482.6 × 43.6 × 420 mm final bounds.
- Extra structure: 0 duplicate triangle groups, 0 opposite duplicate pairs, 0 negative transforms, 0 material-alpha violations, 0 exact critical coplanar pairs, 0 textured-card/backing risks, one watertight closed core per GLB.
- Static loads: 40/40 READY and WebGL2, 40 screenshots present, 0 loader errors.
- Rotation stress: 88 frames for each of Three standard/web and Babylon standard/web, 352 total; all four combinations cover 72×5° yaw and 16 multi-pitch dark-checker frames.
- No surface flicker, transparency jump, checkerboard leak, disappearing face, mirror, texture switch or gray/white exposure was found.
- Standard/web parity max normalized RMSE: 0.005346 (Three), 0.001915 (Babylon).

## Warning / residual risk

Only the documented conservative underside is `GENERIC_BOTTOM_FALLBACK`. It is blank, non-identifying and silhouette-neutral. No non-bottom identity gap remains.
