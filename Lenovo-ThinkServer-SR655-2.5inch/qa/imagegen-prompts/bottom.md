# Bottom imagegen prompt

Production mode: MULTI_REFERENCE_RECONSTRUCTION

Input roles:

- Image 1: BINDING EXACT OFFICIAL SR655 UNDERSIDE VIEW from the 24x2.5 state.
- Image 2: EXACT RECTIFIED UNDERSIDE.
- Image 3: EXACT PHYSICAL-LEFT VIEW proving bottom-left edge.
- Image 4: EXACT PHYSICAL-RIGHT VIEW proving bottom-right edge.

Use case: product-mockup
Asset type: exact rack-device bottom texture for GLB
Primary request: generate a new orthographic underside matching the exact official SR655 underside silhouette and stamped seam geometry.
Scene/backdrop: perfectly flat solid #FF00FF chroma background; no shadow, floor, reflection or gradient.
Style/medium: conservative real galvanized sheet-metal product photography; same material family as the inspected real top photo, no CGI beautification.
Composition/framing: complete bottom, physical body width:depth 444.6:764.7.
Verified inventory: plain closed opaque bottom sheet; central kinked longitudinal stamped seam and proven edge steps; no logo, service label, vent, foot, rail or unsupported hole.
Constraints: all product pixels opaque; no text, watermark, adjacent side, cables or detached fragments; do not mirror/copy the top.
Avoid: invented mechanical detail, labels, vents, feet, rails, screws or seams not in Image 1.

Selected raw output: qa/imagegen-output/bottom-chroma.png

Final output: views/bottom.png

Generation record: one built-in imagegen call. This is exact-model multi-reference reconstruction from the official underside, not a generic fallback and not a mirrored top.
