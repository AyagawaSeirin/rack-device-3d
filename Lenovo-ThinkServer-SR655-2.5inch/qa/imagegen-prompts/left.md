# Physical left imagegen prompt

Production mode: MULTI_REFERENCE_RECONSTRUCTION

Input roles:

- Image 1: BINDING EXACT OFFICIAL PHYSICAL-LEFT VIEW, front at screen right.
- Image 2: EXACT REAR-RIGHT/adjacent-shell geometry evidence for the rear edge only.
- Image 3: REAL SR655 TOP-COVER PHOTOGRAPH for galvanized material grain and real photographic character only.
- Image 4: EXACT FRONT-RIGHT overall chassis evidence, used only for shared body proportions.

Use case: product-mockup
Asset type: exact rack-device physical-left texture for GLB
Primary request: independently generate the physical left orthographic side of original SR655 B5VJ 24x2.5. Do not mirror, flip, rotate or copy the right image.
Scene/backdrop: perfectly flat solid #FF00FF chroma background; no floor, reflection, shadow or gradient.
Style/medium: real galvanized server photography matching Image 3, with physical-left geometry locked to Image 1.
Composition/framing: complete perfectly straight side, rear at screen left and front at screen right, physical depth:height 764.7:86.5.
Verified inventory: no yellow warning label; upper rail/lip seam; distinct left-side circular boss spacing; multiple small rear/front holes and fasteners in the exact Image 1 positions; black front latch at screen right.
Constraints: independently generated physical left; all product opaque; no adjacent face, invented labels, serial/QR text, rails, cables or generic side details.
Avoid: physical-right yellow label/pattern, mirroring, blank panel, stylized metal.

Selected raw output: qa/imagegen-output/left-chroma.png

Final output: views/left.png

Generation record: one built-in imagegen call dedicated to the physical left side. It was not mirrored, flipped or copied from right.png. It has no yellow warning label and keeps the distinct left hole/boss pattern.
