# Left face generation record

- Record type: reconstructed acceptance prompt; original verbatim tool payload unavailable because the source task is `notLoaded`.
- Generation path: built-in `image_gen`, one dedicated call, flat chroma background, local alpha extraction, then aspect-locked final sizing.
- Production mode: `MULTI_REFERENCE_RECONSTRUCTION`.
- Primary binding reference: `source/third-party/touchpoint-r7525.jpg`, SHA-256 `cd56fe8f9e6acd264d0baea02bfeb2119e0588bcca67eeb9ee9c01737f1175e4`.
- Input roles: Image 1 exact R7525 12-LFF front-left product photograph/render and photographic material reference (`touchpoint-r7525.jpg`, rear panel excluded); Image 2 official bezel/edge geometry (`source/pdf-pages/ism-bezel-p001.png`); Images 3–4 front/rear configuration locks for edge orientation (`user-row08-front.png`, `user-row08-rear.png`).
- Preserved selected chain: `left-chroma.png` SHA-256 `770f32e514960508f41867d3cd184a3ced7bd3cca7dfc61fd4b395570fc4e1a7`; `left-alpha.png` `1cd420e775165a78e64080b26f45812751431a24e3c36da1d34ad9de3d5cbf4d`; `left-trim.png` `ce6758a019d0082fe83559adeba2118ec7f1d9cb482cdc61bede1a7426a9730e`.
- Final: `views/left.png`, 2400 × 270 RGBA, SHA-256 `205f808a168e8cb9be9c3fcaff14395eb3b6dba61eed7b196b852bfa59557c61`.

## Reconstructed final acceptance prompt

Use case: product-mockup. Generate one exact physical-left orthographic face of the Dell PowerEdge R7525 12-LFF installed appliance. Lock the front/rear orientation to the provided configuration images. Preserve the real front bezel hook/control silhouette, galvanized sheet-metal tone and grain, top and rear seams, fasteners, stamped recesses, and five verified asymmetric rail/keyhole features. This is the physical left face and must not be copied or mirrored from the right. Keep source-like color balance, mild wear, edge highlights and shallow recess shadows; do not turn the sheet metal into smooth CGI. Do not invent vents, labels, feet, rails, handles, ports or holes. Output one complete straight side on a perfectly flat removable chroma background with no adjacent top/front/rear face, perspective, floor, cable, rail, shadow, watermark, callout or detached fragment. Preserve physical ratio 772.13:86.8 and make all product pixels opaque.

Acceptance result: selected output retains the left-specific hook, seams and five-feature asymmetric rail/keyhole layout; PASS for the left face.
