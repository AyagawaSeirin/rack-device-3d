# Evidence, lineage and interpretation

Initial access date: 2026-08-23  
Final checkpoint re-audit: 2026-08-24

## Primary official sources

1. Dell, *PowerEdge R720 and R720xd Technical Guide* — https://downloads.dell.com/manuals/all-products/esuprt_ser_stor_net/esuprt_poweredge/poweredge-r720_reference-guide_en-us.pdf
   - Original: `source/originals/dell-poweredge-r720-r720xd-technical-guide.pdf`
   - SHA-256: `2ef98db5274d10aa9cd47f6f6f20f139055fbe49fe4c35dc97cded6de47ac04d`
   - Printed pages 13-18 rendered under `source/pdf-pages/technical-guide-p001.png` through `p006.png`; page 14 Figure 5 proves the standard R720 rear and separates it from the R720xd rear.
   - Printed page 56 rendered as `source/pdf-pages/technical-dimensions-p001.png`; Figure 18 gives Xa 482.4 mm, Xb 444.0 mm, Y 87.3 mm, Za 32/18 mm, Zb 684 mm, Zc 723 mm.
   - Text proves R720 supports up to eight 3.5-inch drives, an LCD control panel, two front USB, VGA, vFlash, up to seven PCIe slots and two hot-plug PSUs.

2. Dell, *PowerEdge R720 and R720xd Owner's Manual* — https://dl.dell.com/topicspdf/poweredge-r720_owners-manual_en-us.pdf
   - Original: `source/originals/dell-poweredge-r720-r720xd-owners-manual.pdf`
   - SHA-256: `f3a938634a46a9d7567f5c194caf3826cc914c03090e4532844f495abe683278`
   - Printed page 8 Figure 1 (`source/pdf-pages/owners-manual-p001.png`) proves the R720 3.5-inch 2 x 4 carrier layout and control ordering.
   - Printed pages 16-17 (`owners-manual-p009.png`, `p010.png`) enumerate the standard R720 rear: system ID, iDRAC, three low-profile slots, serial, VGA, two USB, four Ethernet connectors, four full-height slots, two PSUs.
   - Printed pages 95-96 document the `3.5 Inch (x8) SAS/SATA Backplane—PowerEdge R720`, distinguishing it from the R720xd x12 backplane.

## User configuration lock

- Original: `source/originals/user-configuration-lock.png`
- SHA-256: `00861cf47eb85ee4f20fc3dc3fc850820368df4e3db7b2721b3226dfca8c1921`
- First row only. Crops are stored under `source/crops/` and are not treated as new source originals.
- Front: no security bezel, eight 3.5-inch carriers present, R720 LCD/control area and optical bay.
- Rear: standard seven-slot R720 rear, all slot covers installed, quad RJ45 NDC, dedicated iDRAC, DB9 serial, VGA, dual USB and two installed AC PSU modules.

## Inspected secondary photographs

- `flagship-r720-8lff.jpg` — https://cdn11.bigcommerce.com/s-017c0/images/stencil/2560w/products/12196/55018/R720_8bay2__25089.1578343171.1280.1280__67008.1584378162.jpg?c=2 — exact R720 8-LFF front three-quarter, no bezel; proves LFF carrier form, right-side shell and top.
- `ecs-r720-8lff-front.jpg` — https://expresscomputersystems.com/cdn/shop/files/dell-power-edge-r720-8-hdd_2000x.jpg?v=1708629536 — exact R720 8-LFF front three-quarter; proves top cover, latch, front label band and side shell.
- `itinstock-r720-8lff-angle.jpg` — exact R720 8-LFF front with bezel; bezel is excluded but top material and chassis identity support the top reconstruction.
- `innercomm-r720-8lff-rear.jpg` — https://www.innercomm.eu/wp-content/uploads/2022/10/DellR7208LFF_Back.jpg — exact R720 8-LFF rear elevated photograph; proves top latch/cover, standard rear, two 750 W AC PSUs.
- `suredone-r720-rear.jpg` — https://assets.suredone.com/1797/media-photos/cl7x042514-dell-poweredge-r720-intel-xeon-e5-2620-6-core-200ghz-no-ram-2x300gb-sas-6g-2.jpg — exact R720 standard rear real photograph; proves rear relief, PSU fan/inlet construction and port material.
- `storagereview-r720-side.jpg` — https://www.storagereview.com/wp-content/uploads/2013/02/StorageReview-Dell-PowerEdge-R720-Side.jpg — direct R720 left-side product photograph; front is at image right; proves non-mirrored side seams, labels and rail points.
- `storagereview-r720-rails.jpg` — https://www.storagereview.com/wp-content/uploads/2013/02/StorageReview-Dell-PowerEdge-R720-Rails.jpg — left-side/top close perspective; proves hook tabs, screws and label material.
- `walmart-r720-angle.jpg` — https://i5.walmartimages.com/asr/8b2aaf7b-25b9-4361-a49e-1100a27a901a.2e59a3be8696a665d867da6aa718de1a.jpeg — direct opposite-side R720 photograph; front is at image left; proves the right side independently and shows that it is not a mirrored copy of the labeled left side.
- `generic-bottom-dell-r210ii.jpg` — inspected generic Dell underside reference used for material character only under the documented bottom fallback.

All raster files above were opened at original detail before their role was accepted. Seller surroundings, rails, cables, stickers, handwritten labels, inventory labels and drive-capacity stickers are excluded from generated deliverables. Exact Dell/PowerEdge factory branding remains required.

The six selected generated outputs, their exact source locks and SHA-256 values are recorded in `source/face-source-lock.csv`. Final source/render/overlay/difference sheets are under `qa/comparisons/`; authoritative three-quarter photographs are paired with the actual Three.js standard renders in `qa/comparisons/oblique-reference-render.png`.

## Dimension interpretation

The delivered appliance has no front bezel. Therefore the authoritative overall depth is derived as `Za without bezel + Zc = 18 + 723 = 741 mm`. The main chassis shell ends at `Za without bezel + Zb = 702 mm`; PSU handles/inlets and rear projecting detail account for the remaining 39 mm. Width with front rack latches is 482.4 mm; body width is 444 mm. Height is 87.3 mm. Model bounds are therefore 482.4 x 87.3 x 741 mm including front ears and rear protrusions.

## Controlled exclusions

- No R720xd twelve-drive face or rear two-drive flex-bay.
- No 2.5-inch SFF front.
- No R730/R730xd controls or rear board.
- No security bezel.
- No DC terminal block or DC PSU.
- No expansion-card connectors: all seven PCIe positions stay blanked as in the user lock.
- No rear rack ears inferred from a perspective view.
- No unsupported underside mechanics; bottom is the disclosed conservative fallback.
