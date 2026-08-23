# Top face generation record

- Record type: reconstructed acceptance prompt; original verbatim tool payload unavailable because the source task is `notLoaded`.
- Generation path: built-in `image_gen`, one dedicated call, flat chroma background, local alpha extraction, then aspect-locked final sizing.
- Production mode: `MULTI_REFERENCE_RECONSTRUCTION`.
- Primary binding real frame: `source/originals/official-video-frames/12lff-backplane/frame-000s.jpg`, SHA-256 `59ea12b3fe38f720b8d3e81abc17f2e1d35aee477a74be78b7cd7e3142950f8d`.
- Input roles: Image 1 exact official 12-LFF front-right/top frame (`frame-000s.jpg`), binding geometry/material/style; Image 2 independent exact top frame (`frame-020s.jpg`); Images 3–4 official cover/bezel figures (`source/pdf-pages/ism-bezel-p001.png`, `ism-bezel-p003.png`).
- Preserved selected chain: `top-chroma.png` SHA-256 `12fcb0455eb6b90699d5e01503345dcc0183abaa42dc99c4ec83bf3f278351fb`; `top-alpha.png` `6024b9595243536292712ac17a7bea76a9f85587e08d35308d0b3995a6f2c72b`; `top-trim.png` `f4ab8f05b0b7ce422e4e5b0b4113a3bb94abe8185225af7dccc7b3984ba0bd3c`.
- Final: `views/top.png`, 1349 × 2400 RGBA, SHA-256 `38ce14971de1e9bf3279940165155de26023fcf6c6f22c3d76f27738196d96ef`.

## Reconstructed final acceptance prompt

Use case: product-mockup. Generate one exact orthographic top face of the Dell PowerEdge R7525 exact 12 × 3.5-inch/LFF chassis. Preserve the plain galvanized-silver installed cover, real perimeter and panel seams, front information-label strips in their verified white/orange/black areas, centered cover-release latch in its recessed pocket, side-edge fasteners and front/rear edge treatment. Match the official service-video frames' real metal grain, mild wear, color balance, highlight softness and shallow seam shadows. Do not add vents, fans, windows, handles, feet, branding, decorative labels or generic server details; do not mirror or beautify. Output one complete top on a perfectly flat removable chroma background with no visible side/front/rear face, perspective, floor, cast shadow, cable, rail, watermark, annotation or detached fragment. Preserve physical ratio 434.0:772.13 and make all product pixels opaque.

Acceptance result: selected output preserves the exact cover, latch, label-strip region and source-like galvanized photographic character; PASS for the top face.
