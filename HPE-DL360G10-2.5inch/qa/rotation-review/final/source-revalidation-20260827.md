# 2026-08-27 source revalidation

## Identity and exact installed configuration

- Product identity remains HPE ProLiant DL360 Gen10, 1U SFF chassis, standard 8SFF 2.5-inch 6+2 carrier arrangement with Universal Media Bay/control region; 4LFF, 8+2SFF, 10SFF NVMe and later generations are excluded.
- The locked rear remains no rear drive, three PCIe apertures blanked, FlexibleLOM aperture blanked, embedded 4x1GbE, dedicated iLO, DB9 serial, two USB 3.0, VGA and two 500 W HPE Flex Slot hot-plug AC PSUs. DC variants are excluded.
- HPE factory marks are retained.

## Current official source check

- HPE's currently indexed QuickSpecs page still identifies the DL360 Gen10 and gives SFF system-unit dimensions of 4.29 x 43.46 x 70.7 cm. Current indexed QuickSpecs variants continue to list 8SFF chassis configurations separately from 8+2SFF and 10SFF alternatives.
- The March 2026 HPE Maintenance and Service Guide preserved locally remains the strongest current component/order source; printed pages 189, 198 and 242 were rechecked against the front, rear and dimensions.
- The user configuration lock, current HPE QuickSpecs/maintenance material, official component images and exact-device photographs were reread against `identity-manifest.md`, `dimension-ledger.csv`, `face-source-lock.csv`, and all 31 rows in `feature-inventory.csv`.
- A real-browser visit on 2026-08-27 reached the HPE dynamic documentation shell but some authentication, font and telemetry resources failed. The browser log is preserved in `qa/playwright-research/`; those ancillary failures do not contradict the official PDF/component evidence.

Official URLs rechecked:

- https://www.hpe.com/psnow/doc/a00008159enw.pdf
- https://www.hpe.com/us/en/collaterals/collateral.a00008159enw.html
- https://support.hpe.com/hpesc/public/docDisplay?docId=a00115362en_us&page=GUID-A907F1AD-6041-4CD5-9C29-47DF3AC366A9.html
- https://support.hpe.com/hpesc/public/docDisplay?docId=a00115362en_us&page=GUID-CCF447DF-671D-4F37-9C1A-B88D67163C92.html
- https://support.hpe.com/hpesc/public/docDisplay?docId=a00115362en_us&page=GUID-CF51EA3E-8026-4357-92C2-E047EBE6F004.html

## Public exact 3D search

HPE Product Support, PSNow/QuickSpecs, product/media searches and exact identifiers `DL360 Gen10`, `867959-B21`, and `HSTNS-2154` were rechecked with GLB, glTF, STEP, CAD, OBJ, FBX, USDZ, AR and 3D terms. No public official exact-configured 8SFF 3D/CAD/AR binary was found. Public exact-model Visio stencil references are 2D and are not substituted. There is no official 3D file to preserve; the standard and web GLBs are independent reconstructions.

## Face confidence

Front, rear, left, right and top retain exact-model/configuration source locks. No usable identity-bearing exact underside was found after the documented search, so only the bottom is `GENERIC_BOTTOM_FALLBACK`; unsupported underside openings, labels and stampings are omitted.
