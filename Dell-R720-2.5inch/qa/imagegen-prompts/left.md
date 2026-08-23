# left — built-in imagegen

Production mode: MULTI_REFERENCE_RECONSTRUCTION

Input roles:

1. `source/third-party/ebay394100550218-04-internal.jpg`: PRIMARY BINDING REAL EXACT-R720 PHOTOGRAPH — independent left chassis edge, rear-riser relationship and real metal character.
2. `source/third-party/ebay394100550218-01-front-top.jpg`: BINDING EXACT 16-SFF TOP/FRONT PHOTOGRAPH — left cover edge, front ear and front fixed strip.
3. `source/pdf-pages/owners-manual-system-cover-p02.png`: OFFICIAL EXACT-R720 DIAGRAM — cover and side-hook relationship.
4. `source/pdf-pages/readyrails-b6-p01.png`: OFFICIAL B6 MECHANICAL SUPPORT — four side J-slot engagements; rails must not appear.

Final prompt:

Use case: product-mockup
Asset type: exact physical-left orthographic texture for a website GLB
Primary request: Reconstruct a new perfectly straight orthographic view of the PHYSICAL LEFT SIDE of the exact Dell PowerEdge R720 2U chassis from the jointly binding exact-model references. Front must be at screen RIGHT and rear at screen LEFT. This is an independently authored left side, never a flip or mirror of the right output.
Scene/backdrop: perfectly flat uniform #FF00FF chroma-key background; no floor/shadow/reflection/gradient.
Style/medium: source-locked real used-server photography matching Images 1-2: genuine galvanized sheet metal, fine grain, mild handling marks, stamped hems and restrained highlights; no CGI cleanup.
Composition/framing: one complete extremely long thin 2U side only, no visible top/front/rear/bottom and no perspective; exact physical ratio 684:87.3 = 7.835:1; chassis height must be only 12.76% of its body length; product nearly fills canvas width while occupying no more than 24% of canvas height; full front ear and rear protrusion silhouette present. Do not shorten or thicken the chassis.
Constraints: front-only black ear at screen RIGHT; independently place the verified folded top/bottom hems, cover seam, stamped side hooks/J-slots, rail studs and fasteners using Images 1-4; preserve left-side edge differences indicated by the real chassis/riser photos; no rails, labels, vents, feet or unsupported holes. Product pixels must not use #FF00FF.
Avoid: horizontally flipping Image 1 or the right-side output, generic blank rectangle, top face, full-depth ear, rear ear, R720xd/R730 features, invented markings, CGI/vector/toon style.

## Production record

- Generated as an independent physical-left face with the built-in image generator; the physical front remains at screen right and no right-face pixels were mirrored or reused.
- Successive correction passes removed perspective/top-face leakage and restored the complete front/rear silhouette while retaining the independently placed left-side J-slots, fasteners and folded edges.
- Selected imagegen cutout before dimensional rectification: `qa/imagegen-staging/left-selected-pre-dimension-rectification.png` (2400×276).
- Official installed-envelope audit uses the complete 723 mm silhouette rather than only the 684 mm flange-to-rear body span. To preserve every generated device pixel without nonuniform scaling, seven copies of the original top edge row and seven copies of the original bottom edge row were added as dimension-anchored edge strips. The strips are preserved at `qa/imagegen-staging/left-top-edge-extension.png` and `qa/imagegen-staging/left-bottom-edge-extension.png`.
- Final canonical file: `views/left.png` (2400×290, ratio 8.2759:1 versus official 723/87.3 = 8.2818:1; error under 0.1%).
