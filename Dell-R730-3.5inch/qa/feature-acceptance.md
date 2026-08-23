# Visible-feature acceptance

## Identity and envelope

- Dell PowerEdge R730, regulatory E31S/E31S001, complete 2U appliance.
- Requested 8 × 3.5-inch LFF front, two rows × four columns, all carriers installed, security bezel absent.
- Standard R730 rear without R730xd flex bays; four-RJ45 NDC; two uniform EPP 750W AC hot-swap PSUs.
- Final world envelope: 482.4 × 87.3 × 741.0 mm. The 741.0 mm total combines the documented 18 mm bezel-absent front projection with the 723 mm EIA-flange-to-rearmost extent.
- Closed outward-facing body; all baked transforms are non-mirrored; no external GLB resources.

## Front

| Locked feature | GLB counterpart | Render evidence | Result |
|---|---|---|---|
| Two front-only rack ears | `front-left-rack-ear`, `front-right-rack-ear` and separate release blocks | `three-standard-front.png`, front obliques | PASS |
| Eight LFF carriers, 2 × 4 | eight `front-lff-carrier-*` bay, face, grille and swing-handle assemblies | both viewer front/oblique matrices | PASS |
| Dell and PowerEdge R730 branding | approved source-locked front texture on `front-photo-surface` and control block | front renders at 100% | PASS |
| Control/VGA/LCD/tag group | `front-control-branding-block-*` relief plus source-locked pixels | front renders | PASS |
| Two USB/iDRAC Direct | `front-idrac-direct-usb-block-*` | front renders | PASS |
| Upper ventilation and optical drive | separate ventilation and optical-drive depth blocks | front/oblique renders | PASS |
| Six internal fan modules where airflow path exposes them | six `internal-fan-*` and orange hub meshes behind front relief | front obliques | PASS |

## Rear

| Locked feature | GLB counterpart | Render evidence | Result |
|---|---|---|---|
| Slots 1–3 half height, 4–7 full height | seven independently named PCIe slot frame assemblies | rear renders | PASS |
| No false rear rack ears | no rear-ear node exists; side silhouettes only show the verified physical front ears | rear and side renders | PASS |
| iDRAC8, DB9, VGA, two USB 3.0 | four independent recessed/source-textured groups | rear renders | PASS |
| Four RJ45 NDC ports | `rear-four-rj45-ndc-*` | rear renders | PASS |
| Rear retention handle | independent cylinder and mounts | rear/oblique renders | PASS |
| Two EPP 750W AC PSUs | two module boxes and exact source-textured faces | rear renders | PASS |
| Two IEC C14 inlets, orange release tabs, axial fans and handles | independently named inlet/release/fan/hub/guard/handle meshes per PSU; exact photo face remains outermost | rear and rear obliques | PASS |

## Left, right, top and bottom

- Left and right use different source-locked textures and opposite physical orientations. The right includes an evidence-matched seam/hole pattern and three aligned green-zinc rail studs; the left does not copy that pattern.
- Separate left/right upper cover lips preserve the side seam/parallax.
- Top has its own source-locked texture plus separate front label band, stamped rib, latch pocket and lever relief. `DELL` embossing remains visible in its source position.
- Bottom is the documented `GENERIC_BOTTOM_FALLBACK`: one opaque conservative galvanized surface with no logo, label, vent, hole, foot, rail, seam, fastener or unsupported protrusion. It is not copied or mirrored from the top.

## Materials and web parity

- All 16 materials are `OPAQUE`, non-double-sided; the six face-photo materials use neutral factors and `KHR_materials_unlit`; solid relief uses restrained PBR metal/plastic materials.
- Both GLBs contain the same 148 nodes, 148 meshes/primitives, six textures and complete exterior geometry. Web optimization changes only embedded texture resolution.
- Standard/web and Three.js/Babylon.js matched-angle screenshots are reviewed as the final visible-feature authority; the structural helpers supplement but do not replace this review.
