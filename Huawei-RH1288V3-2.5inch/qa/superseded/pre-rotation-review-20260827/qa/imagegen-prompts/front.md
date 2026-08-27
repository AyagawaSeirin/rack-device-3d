# front image-generation record

- Method: built-in image generation, one dedicated call for this selected face
- Production mode: `SOURCE_LOCKED_GENERATION`
- Original task item: `exec-c140acef-c723-426d-b12b-e5671943588b`
- Original generated path: `/root/.codex/generated_images/01a02d95-ea4b-7de3-bb6f-5e244ff42512/exec-c140acef-c723-426d-b12b-e5671943588b.png`
- Preserved selected raw output: `qa/work/imagegen-raw/front.png`
- Final transparent asset: `views/front.png`
- Notes: front-v1-rejected-6-bays.png and front-v2-rejected-6-bays.png retained outside views/

## Final revised prompt

```text
Use case: product-mockup
Asset type: exact rack-device FRONT texture for GLB, final factual correction
Production mode: SOURCE_LOCKED_GENERATION
Input images: Images 1 and 2 are the PRIMARY BINDING REAL STRAIGHT FRONT PHOTOGRAPH at native and nearest-neighbor inspection scale; Image 3 is the user row-11 exact configuration; Image 4 is Huawei Figure 4-1 technical elevation.
Primary request: produce one perfectly straight orthographic FRONT of Huawei FusionServer RH1288 V3 H12M-03, 1U, standard eight-bay 2.5-inch SFF chassis, matching Images 1 and 2 pixel-for-pixel in component layout and real photographic character.
CRITICAL ASYMMETRIC BAY LAYOUT: EXACTLY EIGHT carriers, NOT a 4x2 grid and NOT six. The upper row has EXACTLY THREE carriers. The lower row has EXACTLY FIVE carriers. At left, three columns each contain a top carrier and a bottom carrier (6 total). Then, beneath the right-side service panel, add EXACTLY TWO more lower-row carriers (making 8 total). The DVD/status/control panel occupies the upper-right area directly above those two extra lower carriers. Count visible carrier faces as 3 upper + 5 lower = 8. Preserve the source widths and gaps; do not merge carriers.
Each carrier has its own black honeycomb grille, its own gray release latch and thin vertical lime-green status accent. All eight are closed; no open bay; no security bezel; no NVMe-orange carrier substitution.
Right service area exactly as Image 1: slim DVD drive in upper-right, fault diagnosis and indicator strip, NMI/power/UID controls, exactly two USB 2.0 ports, one blue VGA DB15. Preserve left Huawei ear and right ear with readable "RH1288 V3" and Intel Xeon badge. Text orientation normal: "HUAWEI", "RH1288 V3", "Intel Xeon".
Scene/backdrop: perfectly flat solid #ff00ff chroma-key; no shadow, gradient, floor, reflection or texture; no #ff00ff device pixels.
Style: source-locked real product photography, not CGI. Preserve black plastic grain, real honeycomb edges, galvanized steel, lime accents, mild wear, restrained contrast, highlight softness and recess shadows.
Composition: complete front only, no top/side/perspective, physical ratio 482.6:43 including separate ears, centered with padding.
Constraints: all chassis pixels opaque including black grille cells. No seller label, cable, rail, watermark, pseudo-text, extra port, mirrored branding, redesign, beautification, smoothing, relighting, RH1288H, V5/V6/V7 or 3.5-inch chassis.
```

