# Evidence ledger — Lenovo ThinkSystem SR655 24x2.5

Initial access date: 2026-08-23 (Asia/Singapore)
Rotation-review official refresh: 2026-08-27

## PDF workflow

No dedicated PDF skill is installed. The explicit fallback was used: preserve official PDFs unchanged, extract text with Ghostscript txtwrite, render relevant pages at 220 dpi, and inspect every rendered page at original detail.

Official PDFs:

- Lenovo Press Product Guide: https://lenovopress.lenovo.com/lp1161.pdf
- Lenovo Quick Start and Setup Guide: https://pubs.lenovo.com/sr655/

Inspected page evidence:

- SR655-quick-start-p001.png: Figures 1-3 distinguish 8, 16 and 24 front 2.5-inch configurations and show positions 0-23.
- SR655-quick-start-p002.png: Figure 6 proves the eight-slot PCIe-rich rear and the official 482.0 x 86.5 x 764.7 mm envelope.
- lp1161-p005.png: official color front/rear reference; 24x2.5 carrier layout, 8-slot rear and dual 750W AC PSU.
- lp1161-p027.png: official front drive-bay matrix including 24x2.5 SAS/SATA, 24x2.5 NVMe and mixed configurations.
- setup-guide pages 21, 23 and 28: common front I/O, rear choices and chassis construction; geometry/documentation sources rather than color authorities.

The Product Guide proves B5VJ is the original ThinkSystem SR655 24x2.5-inch chassis. SAS/SATA, NVMe and mixed backplanes occupy the same 24-carrier front envelope. The delivery subject locks that visible exterior without asserting hidden media.

## User screenshot

Path: source/originals/user-device-list.png

SHA-256: 8ee991db9af36f19c3c3bff7a4c73dcd8df47f8a844e8e6febf5601dda095be1

The fifth readable row proves the requested Lenovo/SR655/2.5-inch label, one row of 24 black SFF carrier fronts with red upper accents, both front latches, and the PCIe-rich rear with two AC PSU faces. The thumbnails are too small to prove protocol labels or hidden media. They are the primary real-photo style/identity locks for front and rear, not final textures.

## Public official 3D viewer

Viewer page: https://lenovopress.lenovo.com/3dtours/sr655/

The public InfinityRT viewer was inspected with Playwright. The default 12x3.5 group was hidden and exact 24x2.5 groups hdd_2_5_, HDD_2_5 and HDD_2_5_ were enabled. The PCIe-rich group was enabled; rear-drive groups were disabled; two 750W AC PSUs remained installed. Auto-rotation was stopped.

Captured exact-state views:

- front: positions 0-23, VGA/ThinkSystem latch left, USB/operator/SR655 latch right
- rear: 3+3+2 PCIe slots, OCP/BMC/VGA/USB/serial, two 750W AC/C14 PSUs
- physical right: front at screen left, yellow warning label and right-side boss/fastener pattern
- physical left: front at screen right, no yellow label and distinct holes/bosses
- top: panels, latch, vent, seams and fasteners
- bottom: exact stamped underside silhouette and central seam
- front-right and rear-right authoritative three-quarter views

Every capture was inspected at original detail. These are official renders and geometry/color evidence, not real-photo style authorities where a real image exists.

The public Lenovo 3D tour was reopened in real Chromium on 2026-08-27 and still identifies the withdrawn original ThinkSystem SR655 and exposes the same configuration viewer. The selected PCIe-rich, no-rear-drive, dual-750W-AC rear is physically identical for B5VJ and B5VK. The prior 2.5-inch rear asset had been generated at the front-ear width and failed the rear body ratio by 8.32%; it was therefore replaced byte-for-byte with the already validated 2400x467 paired rear used by the 3.5-inch variant, as required by the elevation pairing rule. No face was regenerated.

The public raw geometry/texture package is retained unchanged at source/optional-3d/Lenovo-ThinkSystem-SR655-official-viewer-original-files.tar.gz.

Archive SHA-256: 2d99c8fe4bc86f0ed28575421e76630a356cb69360e1dcb09b44c2c81af24a3e

It is a backup/evidence source only. Its mesh is not imported, copied or substituted into the new GLBs.

## Third-party real photographs

Source listing: https://www.ebay.com/itm/206238343567

The preserved photos are original-generation SR655 12x3.5 appliances, not the requested front. They are used only after official documentation proves B5VJ/B5VK share dimensions and the closed top/side/rear shell:

- shared-chassis-top.jpg, SHA-256 ac4bc8b5b3f941b5baaadd6c73c95d8d57d026fe958095b14031bb017332ac89, proves galvanized top-cover grain, service-label style, latch and vent appearance.
- shared-chassis-front-top.jpg, SHA-256 b74ef6df1163cf7d66e221ee3281432cff38a6d762eb4c8a16bd98146b0a1b13, supplies real black plastic/red accent and galvanized metal character only; its 3.5-inch front is excluded from identity/layout.
- shared-chassis-rear-top.jpg, SHA-256 a597a009259e1681a2febd6ec485284452992cca40abc442c9cff042a22e5cc7, corroborates real PCIe-rich materials and AC PSU construction but shows 1100W PSUs; exact wattage/layout authority remains the official 750W reference.

Seller wrapping, inventory stickers, plastic film and unit-specific serial/QR labels are excluded.

## Dimension ledger

body_width_mm: 444.6
overall_width_mm: 482.0
height_mm: 86.5
body_depth_mm: not separately published
overall_depth_mm: 764.7
front_projection_mm: included in overall depth; latch projection not separately published
rear_projection_mm: installed PSU and connector projection included in the official envelope
rack_ear_left_extension_mm: overall minus body span distributed by verified latch silhouette
rack_ear_right_extension_mm: overall minus body span distributed by verified latch silhouette
published_dimension_includes: rack latches; excludes security bezel
source_url: https://pubs.lenovo.com/sr655/

## Completion of evidence gate

Front, rear, physical left, physical right, top and bottom have exact original-SR655 evidence. Bottom has exact official-viewer evidence, so GENERIC_BOTTOM_FALLBACK is not required. There are no unresolved non-bottom evidence gaps.
