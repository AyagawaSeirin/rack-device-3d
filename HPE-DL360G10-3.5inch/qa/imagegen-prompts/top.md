# top.png

Production mode: `MULTI_REFERENCE_RECONSTRUCTION`

Input roles:

1. `source/third-party/era-4lff-01-900x2000.png`: PRIMARY BINDING EXACT 4LFF REAL TOP PHOTOGRAPH; highest authority for top layout, material, labels, wear and photographic style.
2. `source/third-party/etb-tech-4lff-angle.jpg`: BINDING exact 4LFF top/front/right geometry and folded edges.
3. `source/pdf-pages/quickspecs-p04.png`: OFFICIAL exact 4LFF top/front reference.
4. `source/pdf-pages/quickspecs-p05.png`: OFFICIAL top-down chassis footprint/orientation support; internal features must not appear through the closed cover.

Final prompt:

Use case: product-mockup
Asset type: exact website GLB TOP-face source
Primary request: Generate one new perfectly straight orthographic TOP view of the closed exact HPE ProLiant DL360 Gen10 1U 4LFF chassis. Image 1 is the binding exact real product photograph for factual layout and photographic style.
Scene/backdrop: flat uniform solid #00FFFF chroma-key background; no shadow, floor, reflection, gradient or texture; do not use #00FFFF on the device.
Style/medium: source-locked real galvanized sheet metal with the same subtle grain, stamping, minor scratches, discoloration, fastener darkness, contrast and soft highlights as Image 1. Do not clean, relight, smooth, denoise, recolor or convert to CGI/vector/illustration.
Composition/framing: one complete top only, perfectly orthographic, front at the bottom and rear at the top; no front/rear/side face visible; physical body width:depth 434.6:749.8; portrait footprint centered with safe padding and no stretching.
Verified structure: two-piece closed top; fixed front LFF cover section across full width with the exact transverse seam, stamped dimples/fasteners and two dark factory label fields; separate large removable access cover behind it; one central recessed black release latch in the source position; one smaller rectangular vent group left-of-center and two long rear vent groups in the exact non-mirrored locations; folded perimeter returns and seam structure. Keep any unreadable compliance/service label copy as physically plausible blank/blurred factory print rather than invented pseudo-text; no extra branding beyond verified HPE label marks.
Constraints: preserve asymmetric vent and latch locations from Image 1. Closed opaque chassis; no transparent vent pixels and no visible internals. No rails, bezel, cables, callouts or seller marks.
Avoid: mirrored vent layout, top copied from another generation, SFF-short footprint, open cover, motherboard/fans, invented vents/handles/feet/holes, readable fake serial/QR text, clean CGI, game asset look, artificial symmetry, flat vector surfaces or beautification.

Method: built-in `image_gen`, one dedicated call; chroma-key removal follows locally.
