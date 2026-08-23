# rear.png generation record

- method: built-in `image_gen`, one dedicated call
- production_mode: `SOURCE_LOCKED_GENERATION`
- raw_output: `qa/work/imagegen-raw/rear.png`
- final_output: `views/rear.png`
- transparency: raw output's non-key white bands were cropped outside the product/key field; installed chroma helper used border auto-key, soft matte, thresholds 30/120, and despill; alpha validated
- input_roles:
  1. `source/originals/qfx5110-48s-rear-high-afi-ac.jpg` — PRIMARY BINDING REAL OFFICIAL AFI AC REAR; exact layout, identity, material, branding and style
  2. `source/third-party/nwkoubou-qfx5110-48s-afi-rear.jpg` — supporting exact real rear/top depth and handle relief
  3. `source/third-party/nwkoubou-qfx5110-48s-afi-fan.jpg` — supporting exact AFI handle geometry/material; damage excluded
  4. `source/pdf-pages/qfx5110-hardware-guide-p041.png` — official technical component order

## Final prompt

Generate a new perfectly straight orthographic REAR view of the exact Juniper Networks QFX5110-48S-AFI with two 650 W JPSU-650W-AC-AFI PSUs and five QFX5110-48S-FANAFI modules. Image 1 is binding for identity and photographic style. From device-left to device-right preserve: one management panel with Juniper and QFX5110-48S/RUNNING JUNOS markings, four ALM/SYS/MST/ID LEDs, C1 cage, CON over C0 RJ-45, reset and USB; exactly five equal azure AIR IN fans numbered 0–4 with black honeycomb and molded handle relief; exactly two black AC AFI PSUs with IEC inlets, AC/DC/fault indicators, AFI markings, black handles and silver cord retainers. No rear ears. Physical body ratio 440.944:43.688. Match the primary real photo's gray metal, azure plastic, grain, wear, highlights, color and recess shadows; no cleanup, relight, smoothing, denoising, vectorization or restyle. Preserve real readable factory branding; exclude seller/serial/QR labels and damage. One rear face only on flat uniform `#FF00FF`; all product pixels opaque. No DC blocks, gold/orange AFO, missing PSU, cable, rail, watermark, shadow, fake ports/LEDs or mirroring.
