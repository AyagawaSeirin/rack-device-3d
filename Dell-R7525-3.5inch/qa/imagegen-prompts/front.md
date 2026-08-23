# Front face generation record

- Record type: reconstructed acceptance prompt; original verbatim tool payload unavailable because the source task is `notLoaded`.
- Generation path: built-in `image_gen`, one dedicated call, flat chroma background, local alpha extraction, then aspect-locked final sizing.
- Production mode: `MULTI_REFERENCE_RECONSTRUCTION` (the direct configuration-lock crop is too small to be the sole style source).
- Primary binding configuration: `source/originals/user-row08-front.png`, SHA-256 `237f3df3e32f910391d2cc56039972c346faa83681d4f6dc8e14c9154ec22570`.
- Input roles: Image 1 configuration lock (`user-row08-front.png`); Image 2 exact 12-LFF geometry (`source/pdf-pages/ism-p002.png`); Image 3 bezel geometry (`source/pdf-pages/ism-bezel-p001.png`); Image 4 real 12-LFF carrier/material source (`source/third-party/ebay-365655196804-main.jpg`); Image 5 exact R7525 bezel/style source (`source/third-party/touchpoint-r7525.jpg`); Image 6 exact official service-video material/geometry (`source/originals/official-video-frames/12lff-backplane/frame-000s.jpg`).
- Preserved selected chain: `front-chroma.png` SHA-256 `ca9e2d3ad32d4117c8ee42d14450e1e9367e8a1d86365b75d30cfc43246ab372`; `front-alpha.png` `df87fce4f058d78ed60e0dbb27af80bef7a56f1b4b28aeb6c4102c0578fdf1d9`; `front-trim.png` `c3861e7ec6c98648502130a56cd1dfb96eb927acb64adacda13dfe0d8ad96c41`.
- Final: `views/front.png`, 2400 × 432 RGBA, SHA-256 `bb0026756e1b6fed61fd312850bf4d468091443d0623d72ee7fd2ff0033ff63c`.

## Reconstructed final acceptance prompt

Use case: product-mockup. Generate one perfectly straight orthographic front face of the exact Dell PowerEdge R7525 2U installed configuration locked by Image 1: 12 × 3.5-inch/LFF carriers in four columns by three rows behind the installed Dell EMC LCD/security bezel. Preserve two separate full-height control/rack-ear housings; left health/system-ID/Quick-Sync strip; right power, VGA, USB 2.0 and iDRAC Direct Micro-AB strip; eleven large Dell bezel openings arranged six upper and five staggered lower; one upper-left lock cylinder; centered factory `DELL EMC` mark; and the upper-right LCD/navigation area. Keep genuine dark graphite metal/plastic, silver carrier handles, orange release rings, real grille depth, source-like surface grain, contrast, highlight softness and recess shadows. Do not substitute an SFF front, R7515, XE9680 honeycomb, generic server, bare-drive face, or invented display/ports/text. Do not mirror or restyle. Output one complete face on a perfectly flat removable chroma background with no perspective, top/side, floor, cast shadow, cable, rail, seller sticker, watermark, callout, pseudo-text, detached fragment or clipping. Preserve physical ratio 482.0:86.8 and make all product pixels opaque.

Acceptance result: selected output preserves the 4 × 3 LFF configuration, bezel/control order, centered readable factory brand and photographic metal/plastic character; PASS for the front face.
