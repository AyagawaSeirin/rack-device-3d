# right — built-in imagegen

Production mode: SOURCE_LOCKED_GENERATION

Input roles:

1. `source/third-party/walmart-r720-side-angle.jpg`: PRIMARY BINDING REAL RIGHT-SIDE PHOTOGRAPH — exact R720 sheet-metal side, cover seam, fastener and ear material/style.
2. `source/third-party/serverlama-08-r720-overview.jpg`: BINDING EXACT R720 THREE-QUARTER — right-side depth, top steps and front/rear relationships.
3. `source/pdf-pages/owners-manual-system-cover-p02.png`: OFFICIAL EXACT R720 COVER/CHASSIS DIAGRAM — top seam and cover relationship.
4. `source/pdf-pages/readyrails-b6-p02.png`: OFFICIAL B6 MECHANICAL SUPPORT — rail attachment engagement; no rails are to be shown.

Final prompt:

Use case: product-mockup
Asset type: exact physical-right orthographic texture for a website GLB
Primary request: Generate a new perfectly straight orthographic view of the PHYSICAL RIGHT SIDE of a Dell PowerEdge R720 2U chassis. Image 1 is binding for real material and independent side details. Front must be at screen LEFT and rear at screen RIGHT.
Scene/backdrop: perfectly flat uniform #FF00FF chroma-key background; no floor/shadow/reflection/gradient.
Style/medium: preserve Image 1's real galvanized sheet-metal grain, subtle scuffs, stamped edges, neutral color and soft photographic highlights; not CGI or a stylized clean render.
Composition/framing: one complete extremely long thin 2U side only, no visible top/front/rear/bottom and no perspective; exact physical ratio 684:87.3 = 7.835:1; chassis height must be only 12.76% of its body length; product nearly fills canvas width while occupying no more than 24% of canvas height; full front ear and rear protrusion silhouette present. Do not shorten or thicken the chassis.
Constraints: black front ear exists only at front; independently preserve right wall's stepped upper cover seam, folded lower hem, two-height sheet-metal bands, specific rivets/fasteners and four rail-engagement/stud positions supported by the references; rear upper cover steps and small PSU/connector protrusion silhouettes only where evidenced. Do not show rails. Do not mirror another side, add labels, vents, feet, holes or service stickers not shown. Product pixels must not use #FF00FF.
Avoid: mirrored left output, top face, featureless generic rectangle, full-depth rack ear, rear ear, R720xd/R730 details, invented ventilation, CGI/vector/toon style.

## Production record

- Generated as an independent physical-right face with the built-in image generator; physical front remains at screen left and no left-face pixels were mirrored or reused.
- Successive correction passes removed excessive chassis height and top-face leakage while preserving the separately evidenced right-wall seam, studs, hooks and fasteners.
- Selected output: `qa/imagegen-staging/right-overall-final-alpha.png`; canonical transparent cutout: `views/right.png` (2400×283).
- The final six-face dimensional audit accepts this complete installed silhouette within the configured 3% tolerance; no nonuniform scaling was applied.
