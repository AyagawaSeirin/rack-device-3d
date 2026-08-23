# Top imagegen prompt

Production mode: SOURCE_LOCKED_GENERATION

Input roles:

- Image 1: PRIMARY BINDING REAL SR655 TOP PHOTOGRAPH. Authority for real galvanized grain, service-label character, wear and photographic style.
- Image 2: EXACT OFFICIAL TOP VIEW in the 24x2.5/PCIe-rich state. Authority for outline, seams, latch, vent and fasteners.
- Image 3: EXACT FRONT-RIGHT VIEW.
- Image 4: EXACT REAR-RIGHT VIEW.

Use case: product-mockup
Asset type: exact rack-device top texture for GLB
Primary request: generate a new perfectly orthographic top of original ThinkSystem SR655 B5VJ while preserving Image 1 real metal character and Image 2 exact geometry.
Scene/backdrop: perfectly flat solid #FF00FF chroma background; no shadow, floor, reflection or gradient.
Style/medium: same real galvanized product-photography style as Image 1, not a clean CGI render.
Composition/framing: complete top, front and rear orientation exactly as documented, physical body width:depth 444.6:764.7.
Verified inventory: stamped cover panels/seams; black/blue latch; rear ventilation field; factory service-label layout without readable serial/QR content; exact fastener groups and edge steps.
Constraints: all product opaque; preserve legitimate Lenovo service graphics but deidentify unit-specific codes; no adjacent side, rails, cables, seller plastic film or watermark; do not copy bottom.
Avoid: invented vents/labels, smoothing, relighting, vector/illustration look, mirrored orientation.

Selected raw output: qa/imagegen-output/top-chroma.png

Final output: views/top.png

Generation record: one built-in imagegen call. Unit-specific generated microtext, QR and barcode-like content was deidentified while the legitimate service-layout graphics, latch, vent, seams and real galvanized texture were retained.
