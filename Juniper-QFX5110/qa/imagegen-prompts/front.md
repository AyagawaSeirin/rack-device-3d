# front.png generation record

- method: built-in `image_gen`, one dedicated call
- production_mode: `SOURCE_LOCKED_GENERATION`
- raw_output: `qa/work/imagegen-raw/front.png`
- final_output: `views/front.png`
- transparency: generated on flat `#FF00FF`, then the installed imagegen chroma helper was used with border auto-key, soft matte, thresholds 30/120, and despill; alpha was validated before dimensional rectification
- input_roles:
  1. `source/originals/qfx5110-48s-front-high.jpg` — PRIMARY BINDING REAL OFFICIAL FRONT; identity, layout, materials, color, texture, photographic style
  2. `source/originals/qfx5110-48s-frontwtop-high.jpg` — binding official front/top geometry and gray metal
  3. `source/third-party/everychina-qfx5110-48s-afi-04.jpg` — exact-model rack-ear geometry only
  4. `source/originals/user-screenshot.png` — requested ear/empty-port configuration clue only

## Final prompt

Generate a new perfectly straight orthographic FRONT view of the exact Juniper Networks QFX5110-48S-AFI complete switch, dual AC/AFI configuration, empty front cages, with two short front ears installed. Image 1 is the highest-authority binding identity-and-style source. Preserve exactly 48 empty SFP/SFP+ cages in two rows of 24, four banks of six per row, and exactly four larger QSFP28 cages in a 2×2 block at device-right. Preserve GM RJ-45, PPS OUT, 10M OUT, ESD terminal, two full-width hex vent bands, port numbering, and real gray metal. Each galvanized ear has two large true circular openings and one smaller centered opening. Perfect straight-on view; no top/side/perspective. Physical ratio 482.600:43.688. Same real product-photography grain, wear, color balance, contrast, highlights and recess shadows as Image 1; no CGI cleanup, relighting, smoothing, denoising, vectorization or restyle. Keep factory markings in their real readable orientation; do not invent a front logo, serial, QR or pseudo-text. One device only on perfectly flat uniform `#FF00FF`, no shadow/floor/reflection; all product pixels opaque and only ear holes expose key color. No optics, cables, rails, rear ears, watermark, fake ports/LEDs or family substitution.
