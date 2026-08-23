# right image-generation record

- Method: built-in image generation, one dedicated call for this selected face
- Production mode: `MULTI_REFERENCE_RECONSTRUCTION`
- Original task item: `exec-de1006db-4777-42e0-a6e7-2c9e28451562`
- Original generated path: `/root/.codex/generated_images/01a02d95-ea4b-7de3-bb6f-5e244ff42512/exec-de1006db-4777-42e0-a6e7-2c9e28451562.png`
- Preserved selected raw output: `qa/work/imagegen-raw/right.png`
- Final transparent asset: `views/right.png`
- Notes: selected first physical-right generation

## Final revised prompt

```text
Use case: product-mockup
Asset type: exact rack-device PHYSICAL RIGHT SIDE texture for website GLB
Production mode: MULTI_REFERENCE_RECONSTRUCTION
Input images: Image 1 is Huawei's exact official RH1288 V3 front-right three-quarter photograph and PRIMARY BINDING authority for the physical right-side shell, real galvanized metal, side landmarks and photographic style. Image 2 is an exact H12M-03 front-right photograph supporting the same side. Image 3 is a supporting exact 1U RH1288 V3 geometry render. Image 4 is Huawei's rear three-quarter photograph for top/edge continuity only.
Primary request: reconstruct a new perfectly orthographic isolated PHYSICAL RIGHT SIDE elevation of the closed Huawei FusionServer RH1288 V3 H12M-03 2.5-inch chassis, front at image LEFT and rear at image RIGHT.
Verified right-side traits from Images 1-3: 708 mm long by 43 mm high silver galvanized/brushed sheet-metal side; front mounting ear only at the far left front plane; long shallow dark rail-mount strip/channel along the lower side; independently placed circular fasteners/rail attachment points; folded upper and lower seams; a small rectangular perforated ventilation area near the rear-right end; rear termination follows the PSU/chassis edge but no rear ear. Preserve asymmetry and exact observed positions. Do not reuse or mirror the physical left side.
Scene/backdrop: perfectly flat solid #ff00ff chroma-key background with no shadow, gradient, floor, reflection or texture; no #ff00ff in device pixels.
Style: same real photographic metal character as Image 1: mild horizontal brushing, subtle grain and wear, restrained contrast, soft highlights and dark recesses. No CGI cleanup, invented label, vectorization or artificial symmetry.
Composition: one complete straight side face only, no top, front or rear visible, physical content ratio 708:43, front-left/rear-right orientation, centered with padding.
Constraints: all side pixels fully opaque; no rails attached, no cables, no floor, no watermark, no detached fragments, no extra vents/handles/feet/holes, no top face, no mirror, no RH1288H or V5/V6/V7 side.
```

