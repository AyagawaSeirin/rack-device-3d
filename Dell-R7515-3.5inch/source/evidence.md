# Evidence and inclusion rules

Access date: 2026-08-23

## Configuration lock

The user-provided row 10 is preserved unchanged at `source/originals/user-configuration-lock.png`; its isolated row is `source/originals/user-row10-lock.png`. It fixes `DELL R7515/3.5英寸`, 12 exposed LFF carriers, no security bezel, the no-rear-drive/four-expansion-position rear, system I/O, and two installed AC PSUs. R7525, 2.5-inch/SFF, 8-LFF, rear-2-LFF, and DC/HVDC variants are excluded.

## Official Dell documents and pages

- Installation and Service Manual: https://dl.dell.com/topicspdf/poweredge-r7515_owners-manual_en-us.pdf. Unchanged 144-page PDF, SHA-256 `4db00bda83ff0b608464b6c653eeabb180eb2833944f7573962b535ac3407695`. Relevant pages were text-extracted, rendered, and visually inspected. Pages 9-15 prove the 12-LFF front, control panels, no-rear-drive rear, ports, risers, PCIe slots, and dual PSU locations. Pages 29-31 prove the top cover, latch, seams, finish, and rear vent strip. Pages 42-46 prove LFF carrier/handle construction. Pages 113-115 prove hot-plug PSU geometry. Pages 124-127 prove independent left/right control-wing and side-wall routes.
- Technical Guide: https://i.dell.com/sites/csdocuments/product_docs/en/poweredge-r7515-technical-guide.pdf. SHA-256 `689d66eaf2b1f9258dede5034a261d1b058e5536d89acf18ba15ca5c8dd71635`. Pages 9-13 visually confirm the 12-LFF face, both rear variants, and interior/fan count.
- Technical Specifications: https://dl.dell.com/topicspdf/poweredge-r7515_owners-manual2_en-us.pdf. SHA-256 `13d2ac25be91e6ef908729dad5c01b2a8743dba5a5e76bc4003f068b5e1594c5`. Page 5 fixes dimensions/weight; pages 6-10 fix AC PSU support, six fans, risers, drives, LOM, serial, VGA, USB, and iDRAC.
- Spec sheet: https://i.dell.com/sites/csdocuments/Product_Docs/en/poweredge-r7515-spec-sheet.pdf. SHA-256 `5be1fdf25f9817783cbc1c761d7edfdaf92226fcfc9ac42b72faee64346cb730`. It corroborates front/rear port counts and PowerEdge identity.
- Dell HTML 12-LFF front page: https://www.dell.com/support/manuals/en-us/poweredge-r7515/per7515_ism_pub/front-view-of-the-system?guid=guid-71b577eb-97f9-411e-b540-32506130e0bc&lang=en-us.
- Dell HTML rear page: https://www.dell.com/support/manuals/en-us/poweredge-r7515/per7515_ism_pub/rear-view-of-the-system?guid=guid-ece33925-e823-441f-b2be-65a868938bb4&lang=en-us. Figure 2 is the accepted no-rear-drive rear; Figure 1 is retained only as a rejected rear-2-LFF comparison.
- Dell dimension page: https://www.dell.com/support/manuals/en-uk/poweredge-r7515/per7515_ts_pub/system-dimensions?guid=guid-df3a2af4-e49c-4510-867a-ff62232ca974&lang=en-us. Published Xa/Xb/Y/Za/Zb/Zc are 482/434/86.8/22 without bezel/647.07/681.755 mm.

The environment did not expose a standalone PDF skill. The required equivalent workflow was performed with PyMuPDF: full text extraction, targeted 2.5x page rendering, and original/high-detail visual inspection. Contact sheets in `qa/reference/manual-contact-*.png` document the reviewed render set.

## Exact real photographs

- ServerLama exact 12-LFF product page: https://serverlama.com/en/products/dell-r7515-12x-lff. The unchanged HTML is retained. `serverlama-r7515-front.jpg` is the primary front photograph; `serverlama-r7515-back.jpg` is the primary exact no-rear-drive rear with two EPP 750W AC PSUs; diagonal images prove top/rear/side relief. SHA-256 values are recorded in `face-source-lock.csv`.
- ServersStorages exact-model gallery: https://www.serversstorages.com/sale-38159649-dell-poweredge-r7515-rack-dell-emc-storage-server-2-8ghz-amd-processor.html. The unchanged HTML is retained. The gallery supplies a direct side elevation and independent front-right/rear-left angles for non-mirrored side-wall geometry. It is used only for side/top/chassis evidence; its optional bezel and 1100W PSU labels do not override the row-10 front/rear lock.
- Express Computer Systems exact R7515 12x3.5 gallery: https://www.expresscomputersystems.com/products/dell-poweredge-r7515-rack-server-12x3-5. Used to cross-check the carrier face and no-rear-drive versus rear-drive rear diagrams.
- IT Creations review: https://blog.itcreations.com/dell-emc-poweredge-r7515-review/. Exact close-ups prove front controls, rear I/O, riser grilles, PSU construction, and real materials. Overlaid annotations/watermarks are supporting evidence only and must not appear in final assets.

## Inclusion and rejection rules

- The front model uses twelve separate carrier/bay/handle/latch assemblies and two separate front control/rack-wing assemblies. No optional security bezel is installed.
- The rear is the official `no rear drives` assembly: two horizontal Riser 1B covers, large exhaust grille, PCIe slots 4/5, system I/O/LOM-OCP region, and stacked twin AC PSUs. The rear-2-LFF image and every R7525 rear are rejected.
- Rack ears are front-only. A rear three-quarter photograph seeing the front wings does not create rear ears.
- Body width is 434 mm; 482 mm is the ear/flange overall width. The GLB full no-bezel depth target is 22 + 681.755 = 703.755 mm.
- The side and top surfaces use their exact galvanized finish and evidence-backed seams/holes/stamping. Left and right are built independently.
- Bottom is the sole controlled fallback described in `bottom-search-log.md`.

