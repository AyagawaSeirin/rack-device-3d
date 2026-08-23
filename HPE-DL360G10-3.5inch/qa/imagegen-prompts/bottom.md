# bottom.png

Production mode: `GENERIC_BOTTOM_FALLBACK`

Input roles:

1. `source/third-party/era-4lff-01-900x2000.png`: INSPECTED SAME EXACT 4LFF CHASSIS material, perimeter and edge-treatment reference only; it does not show the underside.
2. `source/third-party/etb-tech-4lff-angle.jpg`: INSPECTED SAME EXACT 4LFF right/edge material reference only.
3. `source/pdf-pages/user-guide-p074.png`: OFFICIAL side-wall/rail-spool silhouette constraint.
4. `source/pdf-pages/user-guide-p083.png`: OFFICIAL rear-side edge constraint.

Final prompt:

Use case: product-mockup
Asset type: conservative bottom-face source for exact-device GLB pipeline
Primary request: Generate a new conservative non-identifying orthographic BOTTOM view for the HPE ProLiant DL360 Gen10 1U 4LFF chassis under the documented `GENERIC_BOTTOM_FALLBACK`. Exact underside imagery was not found after official documents, dynamic browser pages, reseller, used-equipment, marketplace, auction and multilingual searches. Do not infer identity-bearing underside detail.
Scene/backdrop: flat uniform solid #00FFFF chroma-key background, no floor, shadow, reflection, gradient or texture; no #00FFFF device pixels.
Style/medium: real galvanized HPE sheet-metal appearance matching Images 1 and 2 in color, grain, roughness, edge treatment and subtle wear; not clean CGI, vector art or illustration.
Composition/framing: one complete perfectly orthographic bottom only, front at the bottom and rear at the top, no adjacent face; physical body width:depth 434.6:749.8; centered portrait footprint with safe padding.
Verified constraints: closed opaque conservative sheet-metal underside; preserve only the verified rectangular LFF footprint, side-wall folded edge silhouette and front/rear perimeter relationship. Keep the surface intentionally plain and non-identifying.
Do not include: HPE/ProLiant logo, model badge, regulatory/service labels, QR/serial text, vents, holes, feet, rails, seams, fasteners, handles, latches, protrusions, ports, access panels or any copied top-cover pattern. Never mirror or reuse the top.
Constraints: all product pixels opaque; no transparent vents; no unsupported detail. Final status remains PASS_WITH_BOTTOM_FALLBACK.

Method: built-in `image_gen`, one dedicated call; chroma-key removal follows locally.
