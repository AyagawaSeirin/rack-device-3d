# Evidence and configuration record

Access date: 2026-08-23. All source downloads are preserved unchanged under `source/originals/` or `source/third-party/`; PDF pages and crops are derivatives kept separately. Every raster listed in `source/source-inspection.csv` was opened at original detail before use.

## Delivery identity

The delivery subject is one complete Dell PowerEdge R720 2U server in the 16×2.5-inch SFF chassis, front bezel removed. It is not an R720xd, not an 8-SFF or LFF front, and not an R730-family enclosure. The user screenshot row 2 freezes one horizontal row of sixteen vertical Dell SFF carrier fronts, the R720 LCD/control/media zone, seven rear PCIe blanking plates, four RJ45 integrated Ethernet ports, dedicated iDRAC, serial, VGA, dual USB, a center handle and two matched hot-plug AC PSUs. The R720xd-only rear flex-bay and its six-slot rear are forbidden.

## Official sources

1. Dell PowerEdge R720 and R720xd Technical Guide: https://downloads.dell.com/manuals/all-products/esuprt_ser_stor_net/esuprt_poweredge/poweredge-r720_reference-guide_en-us.pdf
   - Page 13: R720 2.5-inch front with and without bezel; up to sixteen hot-plug 2.5-inch drives; LCD control, two USB, VGA, vFlash and optional optical drive.
   - Page 14: R720 rear photograph; redundant hot-plug PSUs, four Ethernet connectors and PCIe slots. The photographed layout matches the user rear lock and shows dual 750 W AC PSUs.
   - Pages 15-16: exact R720 versus R720xd internal top views; six hot-plug fan modules and different rear assemblies.
   - Page 56: Xa 482.4 mm, Xb 444.0 mm, Y 87.3 mm, Za 32.0 mm with bezel/18.0 mm without bezel, Zb 684.0 mm and Zc 723.0 mm.
2. Dell PowerEdge R720 and R720xd Owner's Manual: https://dl.dell.com/topicspdf/poweredge-r720_owners-manual_en-us.pdf
   - Front panel: R720 2.5-inch chassis supports sixteen drives and the named LCD/control/I/O components.
   - Pages 16-17: R720 rear has three low-profile PCIe slots, four full-height PCIe slots, serial, VGA, two USB, four integrated Ethernet ports, iDRAC7 Enterprise and two PSUs. Only R720xd can have two rear drives.
   - Pages 36-38: exact R720 cover latch, cover removal, chassis edges and internal installed fan/riser arrangement.
3. Dell B6 ReadyRails II sliding-rail installation: https://downloads.dell.com/manuals/common/rack-slidingrails_installation_guide_sg10_en-us.pdf
   - Both left and right rails engage four chassis-side J-slots; supports side-wall attachment geometry. This guide is mechanical supporting evidence, not color evidence.
4. Dell rendered manual topics:
   - Front: https://www.dell.com/support/manuals/en-us/poweredge-r720/720720xdom/front-panel-features-and-indicators
   - Rear: https://www.dell.com/support/manuals/en-us/poweredge-r720/720720xdom/back-panel-features-and-indicators

## Exact and supporting real photographs

- User configuration lock: `source/originals/user-config-lock.png`, row 2. Binding installed-state authority.
- eBay item 394100550218: https://www.ebay.com/itm/394100550218. Public listing identifies a 16-bay R720; all six public images were retrieved by their public image links. Images 1-3 prove populated carrier style, front controls and top-cover surface; image 4 supports side/top chassis edges; images 5-6 differ in NDC/PSU wattage and are supporting geometry only.
- ITinStock 16-SFF listing: https://www.itinstock.com/dell-poweredge-r720-2x-ten-core-e5-2660v2-256gb-ram-16x-25-bay-2u-rack-server-81034-p.asp. Views 1-2 prove empty 16-bay cage geometry and top silhouette; rear differs by an add-in card and is not the configuration lock.
- ServerLama R720 16×2.5 listing: https://serverlama.com/en/products/dell-poweredge-r720-16x-2-5-sff. Browser-inspected nine-image gallery; exact 16-SFF front/top and internal R720 evidence, plus right-side three-quarter evidence. Bezel-installed and unrelated marketing images were rejected for front configuration.
- Walmart public CDN image from https://www.walmart.com/ip/38673375: direct right-side real photograph; the interactive page presented a human-verification gate, so no access control was bypassed.
- Grays auction public image from https://www.grays.com/lot/0007-2578648/computers-and-it-equipment/dell-poweredge-r720-rack-server: top-cover material/latch and side-edge support; bezel state differs.
- SureDone/eBay rear: https://ebay.com/itm/dell-poweredge-r720-rack-server-xeon-e-2620-6-core-2ghz-2-300gb-sas-6gbps-/331215589609. Rear material, slot plates and PSU style support only; seller sticker/open slot details are excluded.

## Dimension interpretation

`Xa` is the 482.4 mm rack-flange outer width; `Xb` is the 444.0 mm sheet-metal body width. `Y` is the actual 87.3 mm chassis height. Figure 18 draws `Zb=684.0 mm` and `Zc=723.0 mm` from the EIA flange, and draws bezel-absent `Za=18.0 mm` forward from that flange. Therefore the real body depth is `Za+Zb=702.0 mm` and the installed front-to-rear envelope is `Za+Zc=741.0 mm`. The prior 723.0 mm GLB bound omitted the front projection and was corrected during the 2026-08-27 rotation review. Final construction uses a 444×87.3×702 mm body, 19.2 mm front-ear extension per side, an 18 mm front section, and 39 mm rear projection to the 741 mm installed bound.

## Face evidence decisions

- Front: `SOURCE_LOCKED_GENERATION`; direct exact 16-SFF real photograph plus user and official front references.
- Rear: `SOURCE_LOCKED_GENERATION`; exact official R720 product photograph is the primary appearance reference, with the user row fixing blank slots/4-RJ45/dual-AC installed state.
- Left: `MULTI_REFERENCE_RECONSTRUCTION`; exact R720 top-open photograph, exact owner-manual cover/chassis perspective, exact top/front photos and B6 mechanical diagram jointly prove both edges and the independent side attachment pattern. It is not derived by mirroring the right output.
- Right: `SOURCE_LOCKED_GENERATION`; direct side photograph with front at screen left plus exact three-quarter/manual support.
- Top: `SOURCE_LOCKED_GENERATION`; direct exact 16-SFF real photograph shows the full cover, latch, stamped Dell mark, fasteners, front label/vent strip and rear steps.
- Bottom: `GENERIC_BOTTOM_FALLBACK`; see `source/bottom-search-log.md`. The output is intentionally non-identifying and conservative.

## Orientation landmarks

- Front: Dell/control/media zone is physical left; all sixteen carriers are physical right; text reads normally.
- Rear: low-profile slots and management I/O are physical left; dual PSUs are physical right; four RJ45 ports read 1→4 from left to right in the rear camera.
- Top: with the front at the bottom of the image, the recessed black cover latch is in the rear-left quadrant and the stamped Dell mark is in the front-left quadrant.
- Right side: front is at screen left. Left side: front is at screen right. The assets are independently generated and never horizontally flipped.

## Optional official 3D

No exact official R720 CAD/GLB/glTF/STEP/AR download was found. The search record is preserved at `source/optional-3d/README.md`; no community file is labeled official.
