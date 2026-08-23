# left.png

Production mode: `MULTI_REFERENCE_RECONSTRUCTION`

Input roles:

1. `source/third-party/era-4lff-01-900x2000.png`: PRIMARY BINDING EXACT 4LFF REAL PHOTOGRAPH; top/left-edge material and photographic style.
2. `source/third-party/etb-tech-4lff-angle.jpg`: SUPPORTING exact 4LFF chassis depth/material; its right side must not be mirrored.
3. `source/pdf-pages/user-guide-p074.png`: OFFICIAL SIDE/RAIL DIAGRAM for four engagement-spool positions and side outline.
4. `source/pdf-pages/user-guide-p075.png`: OFFICIAL installed side silhouette.
5. `source/pdf-pages/user-guide-p082.png`: OFFICIAL J-slot orientation.
6. `source/pdf-pages/user-guide-p083.png`: OFFICIAL rear-side spool relationship.

Final prompt:

Use case: product-mockup
Asset type: exact website GLB physical LEFT-face source
Primary request: Generate one new perfectly straight orthographic view of the device’s physical LEFT side for the exact HPE ProLiant DL360 Gen10 1U 4LFF chassis. Reconstruct this side independently from the inspected exact chassis and official rail diagrams. Do not mirror Image 2 or a generated right face.
Scene/backdrop: flat uniform #00FFFF chroma-key background only; no floor, shadow, reflection, gradient or texture; no #00FFFF device pixels.
Style/medium: same real galvanized HPE server photography as Image 1, preserving subtle sheet-metal grain, scratches, folded seams, source contrast, highlight softness and dark rail-stud recesses. Not clean CGI, illustration or vector art.
Composition/framing: one complete physical left side from left Drive Bay ID front ear to rear edge, perfectly orthographic; no adjacent face visible; physical depth:height 749.8:42.9; long thin centered product with padding and no squeezing.
Verified structure: separate left front ear/endcap with Drive Bay ID panel and silver mounting flange; closed silver left side wall; top-cover return/lip; long horizontal seam; exactly four independently placed rail engagement spool/stud positions constrained by the official pages; source-supported small stamped recesses/holes and folded front/rear returns. Preserve the true front/rear direction. The left ear is not the right ProLiant-logo ear and must not acquire its text or control layout.
Constraints: independently authored left face, no negative scale and no horizontal flip. All device pixels opaque. No rail, cable-management arm or rear ear installed. Keep unverified fine label areas blank.
Avoid: mirrored right ear/logo, SFF depth, invented vents/feet/handles/labels, decorative holes, generic side panel, perspective, visible top/front/rear, pseudo-text, smoothing, artificial symmetry or restyling.

Method: built-in `image_gen`, one dedicated call; chroma-key removal follows locally.
