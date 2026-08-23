# Front imagegen prompt

Production mode: SOURCE_LOCKED_GENERATION

Input roles:

- Image 1: PRIMARY BINDING REAL FRONT PHOTOGRAPH from the user screenshot. Authority for real black-plastic/metal photographic character, red accents, color balance and highlight softness.
- Image 2: BINDING EXACT OFFICIAL 24x2.5 FRONT RENDER. Authority for geometry, complete silhouette, component count/order, Lenovo/ThinkSystem and SR655 markings.
- Image 3: OFFICIAL PDF COLOR/TECHNICAL PAGE. Confirms 24 SFF positions and I/O.
- Image 4: OFFICIAL FRONT-RIGHT GEOMETRY VIEW. Confirms latch depth and top/front silhouette.

Use case: product-mockup
Asset type: exact rack-device front texture for GLB
Primary request: generate a new exact orthographic front of the original Lenovo ThinkSystem SR655 B5VJ 24x2.5-inch chassis, PCIe-rich dual-750W-AC delivery subject.
Scene/backdrop: perfectly flat solid #FF00FF chroma background; no floor, shadow, reflection, gradient or texture.
Style/medium: same real catalog-product photographic character as Image 1; black textured plastic and real dark metal, subtle wear and soft highlights; not cleaner CGI or illustration.
Composition/framing: one complete straight-on 2U face, both latch assemblies visible, physical width:height 482:86.5, at least 3000 pixels long after project rectification.
Verified inventory: exactly 24 narrow 2.5-inch carrier fronts in one horizontal row positions 0-23; red upper accents; left latch with VGA and vertical ThinkSystem; pull tag near positions 12-15; right latch with status controls, two blue USB ports and SR655 badge.
Constraints: preserve normal-readable factory branding; all product pixels opaque; no adjacent face, cables, rails, seller stickers, watermark, captions or callouts; no security bezel; no mirroring or repeated AI pattern; no invented ports/screens/LEDs/pseudo-text.
Avoid: 12 LFF carriers, 8/16 SFF layouts, SR655 V3, SR650/SR665 substitution, stylization, relighting, beautification, symmetry correction, material smoothing.

Selected raw output: qa/imagegen-output/front-chroma.png

Final output: views/front.png

Generation record: one built-in imagegen call. Unsupported generated protocol/serial microtext was blurred; real SR655 and ThinkSystem branding, positions 0-23, 24 carriers and the red accents were retained. Chroma extraction was repeated without despill to preserve red factory accents.
