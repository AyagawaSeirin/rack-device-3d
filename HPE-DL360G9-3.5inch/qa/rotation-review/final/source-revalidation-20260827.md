# 2026-08-27 source revalidation

## Identity and exact installed configuration

- Product identity remains HPE ProLiant DL360 Gen9 4LFF/3.5-inch, base chassis SKU 755259-B21, 1U.
- Front remains four installed LFF carriers with the 4LFF media/control strip and period-correct HP/HPE/ProLiant marks. SFF/Gen10 fronts are excluded.
- Rear remains three PCIe positions, 4x1GbE FlexibleLOM, two USB 3.0, DB9 serial, dedicated iLO 4, four embedded 1GbE NICs, VGA and two 500 W Flex Slot hot-plug AC PSUs. Alternate two-port FlexibleLOM, missing serial, one-PSU and DC layouts are excluded.

## Current official source check

- HPE's currently indexed `HPE ProLiant DL360 Gen9 Server - Identifying Components` page still explicitly contains the 4 LFF front and lists the rear order: PCIe slots 1-3, PSU 2/1, VGA, NIC 4-1, iLO 4, optional serial, two USB 3.0 and FlexibleLOM.
- HPE's currently indexed specifications page still gives the 4 LFF dimensions as 4.32 x 43.46 x 75.0 cm.
- The official HPE component GIFs, preserved maintenance guide, user configuration lock, exact rear render and exact-device photo set were reread against `identity-manifest.md`, `dimension-ledger.csv`, `face-source-lock.csv`, and all 23 rows in `feature-inventory.csv`.
- A real-browser visit on 2026-08-27 loaded the HPE documentation shell/content scripts but reported ancillary auth/font/telemetry and table-widget errors. The log is preserved in `qa/playwright-research/`; current indexed content and preserved official attachments remain authoritative.

Official URLs rechecked:

- https://support.hpe.com/hpesc/public/docDisplay?docId=c04444501&docLocale=en_US
- https://support.hpe.com/hpesc/public/docDisplay?docId=emr_na-c04443049
- https://www.hpe.com/psnow/doc/c04346229.pdf

## Public exact 3D search

HPE Product Support, PSNow, exact SKU `755259-B21`, HPE media and public indexes were rechecked with GLB, glTF, STEP, CAD, OBJ, FBX, USDZ, AR and 3D terms. No public official exact DL360 Gen9 4LFF 3D/CAD/AR binary was found. No community mesh is substituted or represented as official, so there is no official file to preserve.

## Face confidence

Front, rear, left, right and top retain exact-model/configuration source locks. The documented underside search still yields no usable exact 4LFF bottom. Only the bottom is `GENERIC_BOTTOM_FALLBACK`, limited to a closed galvanized sheet; holes, feet, labels and stampings from the inspected DL120 Gen9 material reference remain expressly forbidden.
