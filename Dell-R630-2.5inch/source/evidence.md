# Dell PowerEdge R630 10×2.5-inch evidence record

Access/inspection date: 2026-08-23 to 2026-08-24 (Asia/Singapore). All files listed in `source/image-inspection.csv` were opened at original/high detail before use. Original downloads were preserved unchanged; generated assets and diagnostic crops are kept under `qa/` or `source/config-lock/`.

## Locked delivery subject

- Dell PowerEdge R630, 13G, 1U, long chassis, bezel absent.
- Front: exact 10×2.5-inch SFF arrangement, five columns by two rows, ten carrier/handle assemblies, left Dell/PowerEdge control wing, right Intel Xeon badge wing.
- Rear: three-riser chassis, three low-profile PCIe blanks, standard ID/iDRAC/DB9/VGA/2×USB group, quad-RJ45 NDC, two matching Dell EPP 1100W hot-plug AC PSUs. DC supplies, mixed supplies, empty PSU bays, fabric retention straps, cables and rear ears are excluded.
- Coordinate convention: +X device right as seen from the front, +Y up, +Z front. The physical left and right textures were generated independently and have different canonical image directions; neither is mirrored from the other.

The binding user configuration crop is `source/config-lock/row-3-r630-2.5inch.png`, SHA-256 `f16c31c90bcb9b26abacf665800525e5b83cff192a57a35821418b479270e2b5`.

## Official Dell evidence

1. Dell PowerEdge R630 Owner's Manual, chassis dimensions and three-riser diagrams:
   - https://www.dell.com/support/manuals/en-us/poweredge-r630/r630_om_pub/chassis-dimensions?guid=guid-60c95c46-c086-419b-8c1a-45a7e1b3d518&lang=en-us
   - https://www.dell.com/support/manuals/en-us/poweredge-r630/r630_om_pub/three-riser-chassis?guid=guid-599100d8-eff9-4961-a285-accba372257d
   - Local original: `source/originals/poweredge-r630-owners-manual-en-us-180912.pdf`; relevant renders: `source/pdf-pages/owners-dimensions-page-01.png` and `owners-manual-page-01.png` through `owners-manual-page-07.png`.
2. Dell PowerEdge R630 Technical Guide v1.6:
   - https://i.dell.com/sites/doccontent/shared-content/data-sheets/en/Documents/Dell-PowerEdge-R630-Technical-Guide-v1-6.pdf
   - Local original and extracted text: `source/originals/Dell-PowerEdge-R630-Technical-Guide-v1-6.pdf` / `.txt`; exact 10-drive front and rear renders: `source/pdf-pages/technical-guide-page-01.png` and `technical-guide-page-02.png`.
3. Dell PowerEdge R630 specification sheet:
   - https://si.cdn.dell.com/sites/doccontent/shared-content/data-sheets/en/Documents/Dell-PowerEdge-R630-Spec-Sheet.pdf
   - Local original and text: `source/originals/Dell-PowerEdge-R630-Spec-Sheet.pdf` / `.txt`; relevant renders: `source/pdf-pages/spec-sheet-page-01.png` and `spec-sheet-page-02.png`.

The Owner's Manual explicit datums control the GLB: overall width 482.4 mm, body width 434.0 mm, height 42.8 mm, no-bezel front projection 20.4 mm, body-front to rear-outermost datum 731.0 mm and total no-bezel depth 752.1 mm. The rounded 75.51 cm marketing depth in the specification sheet is recorded but does not override the explicit diagram/table.

## Exact-device photographic evidence

- TechMikeNY exact 10-bay listing: https://techmikeny.com/products/dell-poweredge-r630-server-10-bay-sff-3-20ghz-16-core-128gb-ram-7-2tb-storage. The front and closed front-right photographs bind the 10-carrier face, black wing housings, Dell/PowerEdge markings, Intel badge, top material and front-quarter silhouette.
- OneClick Servers exact quad-RJ45 rear image: https://oneclickservers.com/cdn/shop/files/7345579589720_d04c196f-0141-4cd4-aa47-e81edb716cdc.png?v=1692832724. It binds rear I/O order and the two matching EPP 1100W AC PSU faces. Seller fabric straps were treated as removable shipping accessories and were excluded; the rigid molded PSU handles remain.
- UsedServers.ca 10-bay page: https://usedservers.ca/r630-10bay.html. Its front and front-elevation images corroborate the exact 10-bay chassis and bezel-absent silhouette.
- Server360 exact 10SFF gallery: https://server360.ru/. Four preserved gallery images corroborate the 10-bay front/top material, cover, label layout and long-chassis proportions.
- eBay item 257483086393: https://www.ebay.com/itm/257483086393. Sixteen preserved gallery images prove side rail channels/studs, top cover, internal seven-fan row, rear chassis frame and PSU construction. This listing's front state, 2×SFP+ + 2×RJ45 NDC, 750W labels, fabric straps and seller cables/stickers are alternate configuration/accessory evidence only and never bind the target face.

## Variant exclusions

- 8×2.5-inch, 24×1.8-inch, LFF, R620 and R640 imagery was rejected for identity.
- Photos with a front bezel, empty drive openings, optical bay, two-riser rear, installed add-in-card ports, 2×SFP+ + 2×RJ45 NDC, 750W/mixed/DC PSU, missing PSU, rear rails, cable-management arm or seller cables were restricted to the specific chassis/material feature they prove.
- The TechMike rear photograph uses an alternate NDC and therefore is non-binding for the network block.
- The eBay rear photographs use the alternate NDC and 750W strapped PSUs; only frame, fan/inlet/rigid-handle construction and material evidence was used.

## Official public 3D search

Dell support/manual/download pages plus official-domain and general searches for `PowerEdge R630 3D`, `R630 CAD`, `R630 STEP`, `R630 GLB/glTF`, `R630 AR`, `site:dell.com R630 3D/CAD/STEP`, and exact 10-bay variants were inspected, including script-rendered galleries where available. No official public file or official interactive model matching the exact 10×2.5-inch, three-riser, quad-RJ45, dual-AC configuration was found. `source/optional-3d/README.md` records the result; no third-party mesh was substituted for the required self-built models.

## Bottom evidence exception

Official manuals/downloads, dynamic product galleries, reseller/marketplace galleries, auction images, video results, and English/Chinese searches were exhausted without a usable exact underside photograph. `source/bottom-search-log.md` records the search. The bottom therefore uses the skill's only permitted exception, `GENERIC_BOTTOM_FALLBACK`: a deliberately conservative closed galvanized plate preserving only side-proven edge folds, rail-stud silhouette and the official 434:731 body ratio. It contains no invented holes, labels, vents, feet, seams or branding. This limits the maximum final status to `PASS_WITH_BOTTOM_FALLBACK`.

## Source-to-output routing

- Face production mode, binding reference, SHA-256, support set and final view hash: `source/face-source-lock.csv`.
- Every raster's inspection/classification: `source/image-inspection.csv`.
- Exact dimensions: `source/dimension-ledger.csv`.
- Visible feature counts/order/relief: `source/feature-inventory.csv`.
- Image generation prompts and accepted correction passes: `qa/imagegen-prompts/` and `qa/imagegen-generation-record.json`.
