# Raster inspection record

All local raster references were opened with original/high-detail image inspection before use.

## Binding images

| Path | Classification | Inspection result | Input role |
|---|---|---|---|
| `user-row12-r730-lff.png` | USER LOCK | Row text is `DELL R730/3.5英寸`; front has 2 × 4 LFF carriers and no bezel; rear has standard seven-slot R730 layout and two PSUs. | highest assembly-configuration lock |
| `ebay-387258968614-2.webp` | REAL_PHOTO | 1500 × 1000, straight near-orthographic 8LFF front, all eight Dell carriers, optical drive, normal Dell/PowerEdge text; white background and repeated Compan watermark. | front primary binding identity/style |
| `ebay-387258968614-4.webp` | REAL_PHOTO | 1500 × 1000, straight rear, seven blanked PCIe positions, iDRAC/serial/VGA/two USB/four RJ45, rear handle, two EPP 750 W AC PSUs; watermark. | rear primary binding identity/style |
| `ebay-387258968614-5.webp` | REAL_PHOTO | 1500 × 1000, exact top, lid latch, rib, stamped DELL area, label strip and rear steps; rotated portrait orientation and watermark. | top primary binding identity/style |
| `amazon-B08D2B1NK7-4.jpg` | REAL_PHOTO | 1467 × 533 front-right exact 8LFF angle; right side is fully visible with upper rail seam, discrete holes and green-tinted studs; no rails. | right multi-reference primary |
| `youtube-CVg_X-OO9Kc-t420.png` | REAL_PHOTO VIDEO FRAME | Same 8LFF server identified earlier at t=90; top removed; standard rear and both side walls visible. | left multi-reference primary and rear geometry support |

## Supporting groups

- `amazon-B08D2B1NK7-1.jpg` is an exploded exact 8LFF view: six fan modules and front cage visible; useful only for fan geometry.
- `amazon-B08D2B1NK7-2.jpg` and `-3.jpg` are packaging views; they do not prove a face and are not generation inputs.
- `amazon-B08D2B1NK7-5.jpg` is a straight standard rear; it corroborates the port and dual-PSU layout.
- `ebay-387258968614-1.webp` is a bezel-on preview with explicit illustration disclaimer; rejected as a binding source because the delivery is bezel-off.
- `ebay-387258968614-3.webp` shows the empty LFF cage; it proves aperture depth but not installed appearance.
- `ebay-387258968614-6.webp` through `-10.webp` are seller promotional graphics unrelated to device faces; inspected and excluded.
- `ebay-387258968614-video-poster.webp` is a generic eBay promotional poster; inspected and excluded.
- `ebay-182270992348-1.webp` is a bezel-on shipping photo; excluded from the final face lock. `-2.webp` shows the exact 8LFF top under foam and only corroborates material.
- `official-video-thumb-*.jpg` are title cards. One control-panel thumbnail explicitly says R730xd and is rejected; the other title cards contain no useful device pixels.
- `youtube-OSV3PdYySjM-t060` through `t260` were inspected. The video explicitly labels the three chassis and isolates 8LFF at t200/t210; rear frames t230-t250 show 1100 W PSU option, so they constrain only common rear geometry.
- `youtube-CVg_X-OO9Kc-t030` through `t540` were inspected. Frames at t90 identify the physical 8LFF chassis; t420/t450 expose both side walls and rear; t510 gives a straight rear with 750 W AC PSUs. Frames focused only on the presenter or drive carrier are not generation inputs.
- PDF page renders `owners-p10`, `owners-p16`, `owners-p27`, `owners-p71`, `owners-p72`, `tech-p13`, `tech-p14`, `tech-p15`, `tech-p57`, `tech-p58`, `tech-p59` were inspected. R730xd and SFF figures are treated solely as explicit exclusion evidence and never as visual inputs for the target front.

No AI-generated derivative is used as a source. Generated final views remain subordinate to these real-photo locks.

## Continuation audit

The original attachment at `source/originals/user-original-screenshot.png` (SHA-256 `00861cf47eb85ee4f20fc3dc3fc850820368df4e3db7b2721b3226dfca8c1921`) was opened at original detail after takeover. It contains adjacent rows such as R720/R630/R620/R240/C6420/C6320 and does not contain the R730 row. It is preserved as user context only; the target configuration remains locked to `user-second-screenshot.png` and its unchanged row crop `user-row12-r730-lff.png`.

All six selected generated chroma images, their alpha conversions, the rejected top/bottom variants, and the six final `views/*.png` files were also opened at original detail. The rejected top showed an adjacent front face; the rejected bottom invented edge tabs. Neither is used by the GLBs. Final left/right assets were compared side by side and are independently oriented rather than mirrored.
