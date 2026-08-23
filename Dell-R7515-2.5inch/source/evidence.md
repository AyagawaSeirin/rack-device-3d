# Evidence and source lineage

## Identity and configuration lock

The user-supplied row 11 crop (`source/originals/user-row11-lock.png`) explicitly names `DELL R7515/2.5英寸`. Its front thumbnail shows the Dell 2U security bezel and its rear thumbnail shows the no-rear-drive R7515 rear with two Riser-1B horizontal slots, two vertical PCIe slots and stacked dual PSUs. This is the authoritative installed-state lock.

## Official Dell sources

1. Dell PowerEdge R7515 Installation and Service Manual, August 2024 Rev. A13.
   - URL: https://dl.dell.com/content/manual22344309-dell-poweredge-r7515-installation-and-service-manual.pdf?language=en-us
   - Local: `source/originals/dell-r7515-installation-service-manual.pdf`
   - SHA-256: `4db00bda83ff0b608464b6c653eeabb180eb2833944f7573962b535ac3407695`
   - Visually inspected rendered pages: 8-16, 27-30, 88-91, 112-116.
   - Proves: R7515/E46S003 identity, 2U, 24 x 2.5 front, exact controls, exact no-rear-drive rear, bezel attachment and geometry, cover form, riser family, dual PSU form.

2. Dell EMC PowerEdge R7515 Technical Specifications, August 2022 Rev. A19.
   - URL: https://dl.dell.com/content/manual23687584-dell-emc-poweredge-r7515-technical-specifications.pdf?language=en-us
   - Local: `source/originals/dell-r7515-technical-specifications.pdf`
   - SHA-256: `13d2ac25be91e6ef908729dad5c01b2a8743dba5a5e76bc4003f068b5e1594c5`
   - Visually inspected rendered pages: 5-10.
   - Proves: exact dimensions, 24-SFF options, six fans, Riser 1B, AC PSU options, USB/LOM/serial/VGA counts.

3. Dell EMC PowerEdge R7515 Technical Guide, December 2021 Rev. A10 (official Dell document preserved from an unmodified public mirror because the current Dell CDN returned 403 to direct command-line download).
   - Official URL: https://i.dell.com/sites/csdocuments/product_docs/en/poweredge-r7515-technical-guide.pdf
   - Preserved mirror: https://26327232.fs1.hubspotusercontent-eu1.net/hubfs/26327232/Bytestock/Product%20Literature/Dell-EMC-PowerEdge-R7515-Technical-Guide.pdf
   - Local: `source/originals/dell-r7515-technical-guide.pdf`
   - SHA-256: `b543d27f306efe6c536b3332680edf3fcca9c27b151e97b4568e97bc037fb404`
   - Visually inspected rendered pages: 9-14 and 45-46.
   - Proves: chassis views, no-rear-drive port order, dimension inclusion note and 24-SFF mass.

4. Official direct front image (manual Figure 3).
   - URL: https://dl.dell.com/content/guides/public/Html/per7515_ism_pub/images/GUID-A8A900AD-B294-4DD3-91D4-DDBCDB86F55C-low.jpg
   - Local: `source/originals/official-front-24x2.5-manual.jpg`
   - SHA-256: `39cc223e0287f89289ae00becc260a842bec11bd9fa37b168b3f2940f806ad7f`
   - Origin: official color render.
   - Proves: 24 vertical carriers, left and right control areas, information tag.

5. Official direct no-rear-drive image (manual Figure 8).
   - URL: https://dl.dell.com/content/guides/public/Html/per7515_ism_pub/images/GUID-53472C08-B972-4BA6-B248-36BCF3C6A1AF-low.jpg
   - Local: `source/originals/official-rear-no-rear-drives-manual.jpg`
   - SHA-256: `db191572171d0503ec1787fbd625830c67cf4f9345e274fc5c2362c231e691ac`
   - Origin: official color render.
   - Proves: exact rear face, no rear drives, riser/PCIe/LOM/I/O/PSU order.

6. Official dimension figure.
   - URL: https://dl.dell.com/content/guides/public/Html/per7515_ts_pub/images/GUID-C7CC57AE-EAD0-4974-B1D9-2ED2E0FD6FA4-low.jpg
   - Local: `source/originals/official-dimensions.jpg`
   - SHA-256: `0749e371f56c398cbc8c12228685924c163b40814bf1bdb3b82aeda7ebec01c5`
   - Proves: dimension inclusion geometry and projection definitions.

## Exact-model real photographs

1. IT Creations R7515 review.
   - Page: https://blog.itcreations.com/dell-emc-poweredge-r7515-review/
   - Primary front URL: https://blog.itcreations.com/wp-content/uploads/2020/05/Dell-PowerEdge-R7515-front-bezel.png
   - Local: `source/third-party/itcreations-r7515-front-bezel.png`
   - SHA-256: `87298d553858c5e539915197c83431380da2fdeedddb37040fd2b1008f7bf530`
   - Inspection: exact R7515 review test unit, straight front, installed security bezel, factory DELL EMC emblem, real matte texture and recess shadows. Third-party ITCTV watermark and table background are excluded by imagegen.

2. Bytestock exact 24 x 2.5 R7515 gallery.
   - Page: https://shop.bytestock.com/dell-poweredge-r7515-24-x-2-5-2u-rack-server-configure-your-own-nvme
   - Six direct URLs: `https://shop.bytestock.com/media/catalog/product/r/7/r7515_24_x_2.5{1..6}_1.jpg`
   - Local: `source/third-party/bytestock-r7515-24sff-gallery-{1..6}.jpg`
   - SHA-256 values are recorded in `face-source-lock.csv` and the project manifest.
   - Inspection: exact 24-SFF chassis; gallery 1 is high front/top, 2 front-right, 3 rear-right, 4 near-straight rear, 5 rear-left, 6 front-left. The two physical sides are distinct and not mirrors. Gallery 4 shows dual EPP 750 W hot-plug PSU. White seller background is not device evidence.

## PDF visual inspection result

All retained raster sources and all listed PDF page renders were opened with the image-viewing capability at original detail. No R7525 raster or LFF front/rear was accepted as a binding source. Pages depicting the optional rear-drive cage were retained only to distinguish and exclude that configuration.

## Bottom and optional 3D

See `source/bottom-search-log.md` and `source/optional-3d/README.md`.

## Final evidence status

- front: VERIFIED exact model/configuration, direct real photo
- rear: VERIFIED exact model/configuration, direct real photo plus official elevation
- physical right: VERIFIED through two independent angles of the same exact 24-SFF real unit
- physical left: VERIFIED through two independent angles of the same exact 24-SFF real unit
- top: VERIFIED through five exact 24-SFF angles plus official cover diagram
- bottom: `GENERIC_BOTTOM_FALLBACK` after documented exhaustion
- final allowed status: `PASS_WITH_BOTTOM_FALLBACK`
