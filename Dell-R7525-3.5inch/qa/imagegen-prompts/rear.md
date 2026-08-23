# Rear face generation record

- Record type: reconstructed acceptance prompt; original verbatim tool payload unavailable because the source task is `notLoaded`.
- Generation path: built-in `image_gen`, one dedicated call, flat chroma background, local alpha extraction, then aspect-locked final sizing.
- Production mode: `MULTI_REFERENCE_RECONSTRUCTION`.
- Primary binding configuration: `source/originals/user-row08-rear.png`, SHA-256 `42ab109f70f5b66f56d1466ce2177722b8440700d0ed03636491c3ad19d1971a`.
- Input roles: Image 1 configuration lock (`user-row08-rear.png`); Image 2 official Figure 9 geometry (`source/pdf-pages/ism-p006.png`); Image 3 enlarged Figure 9 detail (`source/third-party/ecs-r7525-rear-diagram.jpg`).
- Preserved selected chain: `rear-chroma.png` SHA-256 `1e8a403c5e849e2daae7f3bc2fcb1c1edca3a80b067a3c9319f55f350de4003b`; `rear-alpha.png` `fe10c62d47bb3ea8ad52c7833541710ae44704e929b3155e4bc19eecad46dbd3`; `rear-trim.png` `9f12791b9551d6e0a5c0c38eb3a29b08bc18c8af21b6cb39a18a895526230506`.
- Final: `views/rear.png`, 2400 × 480 RGBA, SHA-256 `c9db97688f75a50bf65f16a28fabb8fa143e0fcfaa168d226b01bba01a414f1f`.

## Reconstructed final acceptance prompt

Use case: product-mockup. Generate one perfectly straight orthographic rear face of the exact Dell PowerEdge R7525 no-rear-drive configuration in Image 1 and Dell Figure 9. Preserve four riser groups with eight PCIe slot positions; vented Dell filler pattern; one BOSS S2 cartridge; three rear retention/handle brackets; no optional DB9 serial card; no 2 × or 4 × rear-drive module. Preserve two matching 2400 W AC hot-plug PSUs at the lower rear corners, each with a fan, orange release and IEC C20 inlet. Between them preserve, in the evidence-locked physical order, two embedded NIC ports, OCP 3.0 area, system-ID control, dedicated iDRAC RJ45, USB 3.0, rear VGA and USB 2.0. Retain real stamped zinc-plated metal, black port cavities, blue service accents, real wear/grain and source-like shadows. Do not add DC connectors, mix PSU types, copy front ears onto the rear plane, mirror ports, create family-generic fillers or invent labels. Output one complete face on a perfectly flat removable chroma background with no perspective, top/side, cables, rail, shadow, floor, watermark, annotation or pseudo-text. Preserve physical ratio 434.0:86.8 and make every visible server pixel opaque.

Acceptance result: selected output preserves the locked no-rear-drive Figure 9 layout, eight PCIe positions, management-port order and dual AC PSU identity; PASS for the rear face.
