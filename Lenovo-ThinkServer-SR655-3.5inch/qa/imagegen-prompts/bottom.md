# Bottom imagegen record

method: built-in `image_gen`, exactly one call for this face

production_mode: MULTI_REFERENCE_RECONSTRUCTION (exact official bottom; not fallback)

input_roles:

- Image 1: PRIMARY BINDING EXACT OFFICIAL BOTTOM — `qa/reference/official-viewer-bottom-full.png`; exact SR655 public interactive-viewer underside.
- Image 2: RECTIFIED BOTTOM GEOMETRY — `qa/reference/official-viewer-bottom-rectified.png`.
- Image 3: EXACT SIDE-EDGE SUPPORT — `qa/reference/official-viewer-left-crop.png` and `qa/reference/official-viewer-right-crop.png`.
- Image 4: PRIMARY REAL MATERIAL/STYLE SUPPORT — `source/third-party/ebay-206238343567-3.jpg`; exact SR655 galvanized metal/color/grain only, not bottom geometry.

final_prompt:

Use case: product-mockup

Asset type: exact bottom orthographic rack-device texture for a website GLB

Primary request: generate one new perfectly bottom-up orthographic underside of the original-generation Lenovo ThinkSystem SR655, following the exact official bottom in Images 1-2. This is exact-model evidence, not a generic fallback.

Scene/backdrop: perfectly flat solid #ff00ff chroma-key background, uniform and shadowless, no floor/reflection/gradient; do not use #ff00ff in the device.

Style/medium: real plain galvanized sheet metal matching Image 4's grain, color balance and subtle wear, while Images 1-3 bind geometry. No stylized or cleaner CGI appearance.

Composition/framing: one complete bottom only, exactly perpendicular, no side/front/rear face visible; body width:depth ratio 444.6:764.7; portrait with front edge at image top and rear edge at image bottom; at least 1800 px long-edge intent.

Verified invariants: one opaque plain sheet-metal plate; exactly two long stamped seam/crease paths matching the official viewer; conservative edge folds and front/rear projections proven by side views. No branding, service label, vent, feet, rails, ports or unsupported holes.

Opacity intent: entire bottom fully opaque; external canvas only is chroma key.

Avoid: copying the top; top vent or latch; labels; logos; feet; rails; extra fasteners; invented perforations; pseudo-text; shadow; floor; reflection; CGI smoothing or dramatic lighting.

selected_output: `views/bottom.png`

chroma_source: `qa/imagegen-output/bottom-chroma.png`

output_record: one built-in imagegen call; magenta removed with the installed imagegen chroma helper; final 1512x2600 bottom composites the generated galvanized grain with the exact official viewer underside mask/seam geometry. This is exact-model MULTI_REFERENCE_RECONSTRUCTION, not a generic fallback.
