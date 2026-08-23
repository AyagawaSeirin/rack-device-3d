# right.png

Production mode: `MULTI_REFERENCE_RECONSTRUCTION`

Input roles:

1. `source/third-party/etb-tech-4lff-angle.jpg`: PRIMARY BINDING EXACT 4LFF REAL PHOTOGRAPH; right-side geometry, ear, material and photographic style.
2. `source/third-party/era-4lff-01-900x2000.png`: BINDING exact 4LFF top/edge real photograph.
3. `source/pdf-pages/user-guide-p074.png`: OFFICIAL SIDE/RAIL DIAGRAM showing four side engagement spools.
4. `source/pdf-pages/user-guide-p075.png`: OFFICIAL installed side silhouette and rail relationship.
5. `source/pdf-pages/user-guide-p083.png`: OFFICIAL rear-side spool relation.

Final prompt:

Use case: product-mockup
Asset type: exact website GLB physical RIGHT-face source
Primary request: Generate one new perfectly straight orthographic view of the device’s physical RIGHT side for the exact HPE ProLiant DL360 Gen10 1U 4LFF chassis. The right side is the side visible beside the ProLiant-branded right front ear in Image 1. This is not a mirrored left face and not a SFF-depth chassis.
Scene/backdrop: flat uniform #00FFFF chroma-key background only; no floor, shadow, reflection, gradient or texture; no #00FFFF device pixels.
Style/medium: same real used-enterprise-server photography as Image 1, preserving galvanized sheet-metal grain, subtle scratches, folded seams, fastener/stud darkness and natural highlight softness. No CGI/vector/illustration cleanup.
Composition/framing: one complete physical right side from front ear to rear edge, perfectly orthographic; no front/rear/top/bottom face visible; physical depth:height 749.8:42.9; long thin device centered with safe padding and no squeezing.
Verified structure: separate front ear/endcap only at the front, including the black ProLiant DL360 Gen10 ear body and the two vertical mounting-flange openings seen in Image 1; long closed silver right side wall; upper top-cover return/lip; long horizontal side seam; exactly four rail engagement spool/stud positions along the side as constrained by the official pages; source-placed small stamped recesses/holes and front/rear folded returns. The wall is mostly plain—do not decorate it.
Constraints: preserve front-versus-rear direction from Image 1. Build an independent right-side asset; do not copy or flip the left face. HPE/ProLiant text reads normally only on the right front ear where visible from the side. All device pixels opaque; no rails or cable-management arm installed.
Avoid: 707 mm SFF depth, mirror transforms, rear ears, full-depth rack ear extrusion, invented vents, labels, feet, handles or perforations, generic server side panels, seller stickers, perspective, adjacent faces, pseudo-text, artificial symmetry, smoothing or restyling.

Method: built-in `image_gen`, one dedicated call; chroma-key removal follows locally.
