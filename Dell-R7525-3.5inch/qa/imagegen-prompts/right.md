# Right face generation record

- Record type: reconstructed acceptance prompt; original verbatim tool payload unavailable because the source task is `notLoaded`.
- Generation path: built-in `image_gen`, one dedicated call, flat chroma background, local alpha extraction, then aspect-locked final sizing.
- Production mode: `MULTI_REFERENCE_RECONSTRUCTION`.
- Primary binding real frame: `source/originals/official-video-frames/12lff-backplane/frame-020s.jpg`, SHA-256 `421a43dce9097bc5443b2559afbdb1acc789a458262fb9ba87bcb5851eb1070d`.
- Input roles: Image 1 exact official 12-LFF service-video frame (`frame-020s.jpg`), binding material, side geometry and photographic character; Image 2 independent exact frame (`frame-000s.jpg`); Image 3 official front/edge diagram (`source/pdf-pages/ism-p002.png`).
- Preserved selected chain: `right-chroma.png` SHA-256 `18e6f52902ee87c29f333ba3039cc7ef6206581da9d489f8667708234a5b964e`; `right-alpha.png` `9589b02cf5cc02dbea62adba5164874b9d364fdcfda7bec9d718d789051f8e87`; `right-trim.png` `df50cf535922edacbcd75eea71c749a1125af8836d65666a02f9c56891775bb0`.
- Final: `views/right.png`, 2400 × 270 RGBA, SHA-256 `cc886e47ba8fb1c523f1195bc6cbcbd008c070d0cdfa0a2e501f6402604de0f5`.

## Reconstructed final acceptance prompt

Use case: product-mockup. Generate one exact physical-right orthographic face of the Dell PowerEdge R7525 12-LFF chassis, using the official service-video real frames as binding identity, material and photographic-style references. Preserve the right front control protrusion, sheet-metal height/depth, top and rear seams, fasteners, stamped recesses, and six verified right-specific rail/keyhole features. This is the physical right face and must not be copied or mirrored from the left. Match the real galvanized grain, slightly uneven highlights, wear, color balance and recess shadows. Do not clean it into CGI, smooth the metal, symmetrize features, or invent vents, labels, feet, rails, handles, ports or holes. Output one complete straight side on a perfectly flat removable chroma background with no adjacent face, perspective, floor, cable, rail, shadow, watermark, callout or detached fragment. Preserve physical ratio 772.13:86.8 and make all product pixels opaque.

Acceptance result: selected output retains the right control extrusion and six-feature non-mirrored side layout; PASS for the right face.
