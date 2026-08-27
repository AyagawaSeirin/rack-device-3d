# Built-in ImageGen face log

Date: 2026-08-23  
Built-in `image_gen` calls retained: 24  
Key workflow: generated on uniform magenta, then converted to transparent RGBA with `qa/scripts/remove_magenta_gradient.py`; physical ratios were frozen by `qa/scripts/prepare_views.py`.

The six faces were prompted independently. Left and right were never produced by flip, mirror, copy or negative-scale reuse. The user table screenshot was configuration evidence only and was not cropped or keyed into a final texture.

## Front

Input roles:

- Identity/configuration: `source/third-party/kitairu-rh2288-v3-24sff.png` and Huawei whitepaper Figure 4-4.
- User screenshot: confirms the requested 24-SFF row only; excluded from final pixels.
- Immutable prompt contract: pure front orthographic; exactly 24 equal 2.5-inch carriers; Huawei/operator panel on physical left, diagnostic/VGA panel on physical right; no top/side plane; real logos only; 482.6:86.1 silhouette; magenta background.

Raw calls: `front.png`, `front-v2.png`, `front-v3.png`, `front-v4.png`, `front-v5.png`, `front-v6.png`.

All six initial calls were rejected from final pixels. Reasons included reversed ears, skipped/duplicated bay labels, wrong aspect, and—on the best-proportioned v6—27 generated carriers instead of the immutable 24. The temporary projectively rectified photograph and its GLBs/reports remain under `repair-imagegen-front/before/`; they are not the final front.

### Final front repair calls

Three additional built-in ImageGen calls were made with the exact 24-SFF photograph as the identity/configuration input and Huawei whitepaper Figure 4-4 as the control-layout authority:

1. Source-locked generation: preserve a pure front orthographic 2U appliance with exactly 24 equal carriers; retain Huawei identity; put one USB 2.0 and four Ethernet indicator groups on physical left; put the diagnostic display, health/UID/power/NMI controls, VGA and RH2288 V3 mark on physical right; no top or side plane; uniform magenta background. Retained as `repair-imagegen-front/staging/front-source-locked.png`.
2. Targeted control-layout edit: keep carrier count, order, grille, logo and overall identity fixed while correcting the two ears to Huawei Figure 4-4. Transparent derivative retained as `repair-imagegen-front/staging/front-alpha.png`.
3. Targeted aspect edit: keep all 24 carriers and every ear feature unchanged while increasing horizontal chassis proportion toward the official 482.6:86.1 silhouette. Retained as `repair-imagegen-front/staging/front-final-chroma.png`; keyed output is `front-final-alpha.png`.

The third result was 28 source pixels too shallow. `repair-imagegen-front/extend_face_rails.py` adds 14 pixels to each feature-free horizontal chassis edge rail before uniform resizing; it does not rescale carriers, ears, controls, logos, text or any horizontal feature span. The final content is 4096 x 730 pixels, ratio 5.610959 versus official 5.605110 (0.104% before alpha-bound audit; the final audit reports 0.0555%). Final output: `views/front.png`, SHA-256 `f05faeccd0dfe3fcaf59e930e60b0be309a9880c44914bb29bca89f520bbfbfc`.

## Rear

Input roles:

- Primary identity: `source/third-party/zol-rh2288-v3-rear.jpg`.
- Official topology: `source/pdf-pages/whitepaper-p16-opaque.png`.
- Immutable prompt contract: pure rear orthographic; no rear drives; two AC PSUs vertically stacked on one rear side; two-port flexible NIC A1/A2; standard PCIe/I/O module banks; USB/Mgmt/LAN/VGA/serial; no fictitious text; magenta background.

Accepted raw call: `rear.png`. It preserves the corrected official AC rear and is the source for `views/rear.png`.

## Physical left

Input roles:

- Primary shell evidence: `source/third-party/burrill-rh2288-v3-2.jpg`.
- Supporting top/side evidence: `source/third-party/burrill-rh2288-v3-4.jpg` and official chassis bounds.
- Immutable prompt contract: pure physical-left orthographic; rear tabs at image left, black front ear at image right; independent left vent and fastener pattern; no top plane; no identity-bearing H-variant reuse; no mirroring; magenta background.

Raw calls: `left.png`, `left-v2.png`, `left-v3.png`, `left-v4.png`, `left-v5.png`, `left-v6.png`, `left-v7.png`.

Accepted content: `left-v4.png`, physically rectified without flipping into `views/left.png`. Other versions were rejected for checkerboard background, visible top plane, or excessive silhouette-ratio error.

## Physical right

Input roles:

- Primary evidence: `source/third-party/qgserver-rh2288v3-3.jpg`.
- Supporting shell evidence: official image and exact-page `source/third-party/qgserver-rh2288v3-5.jpg`.
- Immutable prompt contract: pure physical-right orthographic; black front ear at image left, rear tabs at image right; independent mostly plain fastener pattern; explicitly no copied left vent; no mirroring; magenta background.

Raw calls: `right.png`, `right-v2.png`. The first reversed the front/rear direction. `right-v2.png` was accepted and rectified into `views/right.png`.

## Top

Input roles:

- Official top/chassis photographs: `source/originals/huawei-official-product-image.bin`, `source/third-party/qgserver-rh2288v3-5.jpg`, `source/third-party/burrill-rh2288-v3-3.jpg`, `source/third-party/burrill-rh2288-v3-5.jpg`.
- Immutable prompt contract: top plane only; front edge at image bottom; three sheet-metal cover sections, seams, two narrow vent rows and central recessed latch; no adjacent front face, unsupported label or invented component; 447:708 silhouette; magenta background.

Raw calls: `top.png`, `top-v2.png`, `top-v3.png`, `top-v4.png`. `top-v2` exposed the front face and `top-v4` was over-narrow. `top-v3.png` was accepted and rectified into `views/top.png`.

## Bottom

Input roles:

- Controlled fallback only after the exact underside search was exhausted.
- Immutable prompt contract: plain closed zinc-grey underside at 447:708; no vents, labels, feet, screws, ports or unsupported relief; top-down orthographic; magenta background.

Accepted raw call: `bottom.png`, delivered as `views/bottom.png` under `GENERIC_BOTTOM_FALLBACK`.

## Chroma-key fallback

The supplied ImageGen helper did not remove the generator's full magenta gradient on several calls. Per the ImageGen skill's local-helper fallback, `qa/scripts/remove_magenta_gradient.py` removes only pixels where red and blue are both strong and dominate green. This deliberately preserves the device's yellow-green Huawei accents. `qa/scripts/prepare_views.py` records the selected inputs, exact physical target ratios and output sizes.
